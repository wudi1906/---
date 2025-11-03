import { cleanup, render, screen, waitFor, act } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { axe } from "vitest-axe";
import { useState } from "react";
import { afterAll, beforeAll, vi } from "vitest";
import { Modal } from "./Modal";

afterEach(() => {
  cleanup();
  document.body.innerHTML = "";
});

let rafSpy: ReturnType<typeof vi.spyOn> | undefined;
let cancelRafSpy: ReturnType<typeof vi.spyOn> | undefined;
type User = ReturnType<typeof userEvent.setup>;

async function click(user: User, element: Element | Window) {
  await act(async () => {
    await user.click(element);
  });
}

async function typeKeys(user: User, text: string) {
  await act(async () => {
    await user.keyboard(text);
  });
}

async function tab(user: User) {
  await act(async () => {
    await user.tab();
  });
}

beforeAll(() => {
  rafSpy = vi.spyOn(window, "requestAnimationFrame").mockImplementation((cb: FrameRequestCallback) => {
    const handle = window.setTimeout(() => {
      act(() => cb(performance.now()));
    }, 0);
    return handle as unknown as number;
  });

  cancelRafSpy = vi.spyOn(window, "cancelAnimationFrame").mockImplementation((handle: number) => {
    window.clearTimeout(handle);
  });
});

afterAll(() => {
  rafSpy?.mockRestore();
  cancelRafSpy?.mockRestore();
});

async function flushAsync() {
  await act(async () => {
    await new Promise((resolve) => setTimeout(resolve, 0));
  });
}

function ControlledModal({ initialOpen = false }: { initialOpen?: boolean }) {
  const [open, setOpen] = useState(initialOpen);
  return (
    <div>
      <button type="button" aria-label="trigger" onClick={() => setOpen(true)}>
        Open modal
      </button>
      <Modal
        open={open}
        onOpenChange={setOpen}
        title="Demo modal"
        description="Accessible modal description"
        footer={
          <div className="flex gap-2">
            <button type="button" onClick={() => setOpen(false)}>
              Cancel
            </button>
            <button type="button">Confirm</button>
          </div>
        }
      >
        <div className="space-y-2">
          <button type="button">First action</button>
          <button type="button">Second action</button>
        </div>
      </Modal>
    </div>
  );
}

describe("Modal", () => {
  it("passes axe accessibility audit", async () => {
    const { container } = render(
      <Modal open onOpenChange={vi.fn()} title="Heading" description="Helpful description">
        <p>Content</p>
        <button type="button">Ok</button>
      </Modal>
    );

    const results = await axe(container);
    expect(results.violations).toHaveLength(0);
  });

  it("closes on Escape and restores focus to trigger", async () => {
    const user = userEvent.setup();
    render(<ControlledModal />);

    const trigger = screen.getByLabelText("trigger");
    trigger.focus();
    expect(trigger).toHaveFocus();

    await click(user, trigger);
    await screen.findByText("First action");
    await flushAsync();

    await typeKeys(user, "{Escape}");
    await flushAsync();

    await waitFor(() => {
      expect(trigger).toHaveFocus();
    });
  });

  it("traps focus within the modal when open", async () => {
    const user = userEvent.setup();
    render(<ControlledModal />);

    const trigger = screen.getByLabelText("trigger");
    await click(user, trigger);
    await flushAsync();

    const closeButton = screen.getByLabelText("Close dialog");
    const firstButton = await screen.findByText("First action");
    const secondButton = await screen.findByText("Second action");
    const cancelButton = await screen.findByText("Cancel");
    const confirmButton = await screen.findByText("Confirm");

    expect(closeButton).toHaveFocus();

    await tab(user);
    await flushAsync();
    expect(firstButton).toHaveFocus();

    await tab(user);
    await flushAsync();
    expect(secondButton).toHaveFocus();

    await tab(user);
    await flushAsync();
    expect(cancelButton).toHaveFocus();

    await tab(user);
    await flushAsync();
    expect(confirmButton).toHaveFocus();

    await tab(user);
    await flushAsync();
    expect(closeButton).toHaveFocus();
  });
});

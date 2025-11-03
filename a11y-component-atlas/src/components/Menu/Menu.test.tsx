import { render, screen, cleanup, waitFor, act } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { axe } from "vitest-axe";
import { afterAll, beforeAll, vi } from "vitest";
import { Menu, type MenuItemData } from "./Menu";

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

function buildItems(onSelectSpy?: () => void): MenuItemData[] {
  return [
    { id: "new", label: "New", onSelect: onSelectSpy },
    { id: "open", label: "Open" },
    { id: "save", label: "Save", disabled: true },
    { id: "export", label: "Export" },
  ];
}

describe("Menu", () => {
  it("is accessible when open", async () => {
    const user = userEvent.setup();
    const { container } = render(<Menu triggerLabel="Actions" items={buildItems()} />);
    const trigger = screen.getByRole("button", { name: /actions/i });
    await click(user, trigger);
    await flushAsync();
    const list = await screen.findByRole("menu");
    expect(list).toBeVisible();
    const results = await axe(container);
    expect(results.violations).toHaveLength(0);
  });

  it("opens, focuses first item, Escape closes and returns focus", async () => {
    const user = userEvent.setup();
    render(<Menu triggerLabel="More" items={buildItems()} />);
    const trigger = screen.getByRole("button", { name: /more/i });

    await tab(user);
    expect(trigger).toHaveFocus();

    await click(user, trigger);
    await flushAsync();
    const items = await screen.findAllByRole("menuitem");
    await waitFor(() => {
      expect(items[0]).toHaveFocus();
    });

    await typeKeys(user, "{Escape}");
    await flushAsync();
    await waitFor(() => {
      expect(trigger).toHaveFocus();
    });
  });

  it("navigates with arrow keys and wraps", async () => {
    const user = userEvent.setup();
    render(<Menu triggerLabel="Options" items={buildItems()} />);
    const trigger = screen.getByRole("button", { name: /options/i });
    await click(user, trigger);
    await flushAsync();
    const items = await screen.findAllByRole("menuitem");

    // initial focus on first (focus is scheduled asynchronously)
    await waitFor(() => {
      expect(items[0]).toHaveFocus();
    });

    await typeKeys(user, "{ArrowDown}");
    await flushAsync();
    expect(items[1]).toHaveFocus();

    // skip disabled (index 2)
    await typeKeys(user, "{ArrowDown}");
    await flushAsync();
    expect(items[3]).toHaveFocus();

    // wrap to first
    await typeKeys(user, "{ArrowDown}");
    await flushAsync();
    expect(items[0]).toHaveFocus();

    // up wraps to last enabled
    await typeKeys(user, "{ArrowUp}");
    await flushAsync();
    expect(items[3]).toHaveFocus();
  });

  it("home/end moves to first/last", async () => {
    const user = userEvent.setup();
    render(<Menu triggerLabel="Menu" items={buildItems()} />);
    const trigger = screen.getByRole("button", { name: /menu/i });
    await click(user, trigger);
    await flushAsync();
    const items = await screen.findAllByRole("menuitem");

    await waitFor(() => {
      expect(items[0]).toHaveFocus();
    });

    await typeKeys(user, "{End}");
    await flushAsync();
    await waitFor(() => {
      expect(items[3]).toHaveFocus();
    });

    await typeKeys(user, "{Home}");
    await flushAsync();
    await waitFor(() => {
      expect(items[0]).toHaveFocus();
    });
  });

  it("enter selects and closes", async () => {
    const user = userEvent.setup();
    const onSelect = vi.fn();
    render(<Menu triggerLabel="Action" items={buildItems(onSelect)} />);
    const trigger = screen.getByRole("button", { name: /action/i });
    await click(user, trigger);
    await flushAsync();
    const items = await screen.findAllByRole("menuitem");

    // ensure focus on first item before pressing Enter
    await waitFor(() => {
      expect(items[0]).toHaveFocus();
    });
    await typeKeys(user, "{Enter}");
    await flushAsync();
    expect(onSelect).toHaveBeenCalledTimes(1);

    // menu closed and focus back to trigger
    await waitFor(() => {
      expect(trigger).toHaveFocus();
    });
  });

  it("click outside closes", async () => {
    const user = userEvent.setup();
    render(
      <div>
        <Menu triggerLabel="Outside" items={buildItems()} />
        <button type="button">Another Button</button>
      </div>
    );
    const trigger = screen.getByRole("button", { name: /outside/i });
    await click(user, trigger);
    await flushAsync();
    const list = await screen.findByRole("menu");
    expect(list).toBeVisible();

    await click(user, document.body);
    await flushAsync();
    await waitFor(() => {
      expect(trigger).toHaveFocus();
    });
  });
});



import { afterAll, afterEach, beforeAll, describe, expect, it, vi } from "vitest";
import { cleanup, render, screen, act } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { axe } from "vitest-axe";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "./Tabs";

afterEach(() => {
  cleanup();
});

describe("Tabs", () => {
  let rafSpy: ReturnType<typeof vi.spyOn> | undefined;
  let cancelRafSpy: ReturnType<typeof vi.spyOn> | undefined;
  type User = ReturnType<typeof userEvent.setup>;

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

  const renderTabs = () =>
    render(
      <Tabs defaultValue="one">
        <TabsList>
          <TabsTrigger value="one">One</TabsTrigger>
          <TabsTrigger value="two">Two</TabsTrigger>
          <TabsTrigger value="three">Three</TabsTrigger>
        </TabsList>
        <TabsContent value="one">
          <p>Panel one</p>
        </TabsContent>
        <TabsContent value="two">
          <p>Panel two</p>
        </TabsContent>
        <TabsContent value="three">
          <p>Panel three</p>
        </TabsContent>
      </Tabs>
    );

  async function flushAsync() {
    await act(async () => {
      await new Promise((resolve) => setTimeout(resolve, 0));
    });
  }

  it("is accessible", async () => {
    const { container } = renderTabs();
    const results = await axe(container);
    expect(results.violations).toHaveLength(0);
  });

  it("navigates with arrow keys", async () => {
    renderTabs();
    const user = userEvent.setup();
    const tabOne = screen.getByRole("tab", { name: "One" });
    const tabTwo = screen.getByRole("tab", { name: "Two" });
    const tabThree = screen.getByRole("tab", { name: "Three" });

    await click(user, tabOne);
    await flushAsync();
    expect(tabOne).toHaveAttribute("aria-selected", "true");

    await typeKeys(user, "{ArrowRight}");
    await flushAsync();
    expect(tabTwo).toHaveFocus();
    await typeKeys(user, "{ArrowRight}");
    await flushAsync();
    expect(tabThree).toHaveFocus();
    await typeKeys(user, "{ArrowRight}");
    await flushAsync();
    expect(tabOne).toHaveFocus();

    await typeKeys(user, "{ArrowLeft}");
    await flushAsync();
    expect(tabThree).toHaveFocus();
  });

  it("activates tab with space or enter", async () => {
    renderTabs();
    const user = userEvent.setup();
    const tabOne = screen.getByRole("tab", { name: "One" });
    const tabTwo = screen.getByRole("tab", { name: "Two" });

    await click(user, tabOne);
    await flushAsync();
    await typeKeys(user, "{ArrowRight}");
    await flushAsync();
    expect(tabTwo).toHaveFocus();

    await typeKeys(user, "{Space}");
    await flushAsync();
    expect(tabTwo).toHaveAttribute("aria-selected", "true");
    expect(screen.getByText("Panel two")).toBeVisible();
  });

  it("home/end moves to first/last tab", async () => {
    renderTabs();
    const user = userEvent.setup();
    const tabOne = screen.getByRole("tab", { name: "One" });
    const tabThree = screen.getByRole("tab", { name: "Three" });

    await click(user, tabOne);
    await flushAsync();
    await typeKeys(user, "{End}");
    await flushAsync();
    expect(tabThree).toHaveFocus();

    await typeKeys(user, "{Home}");
    await flushAsync();
    expect(tabOne).toHaveFocus();
  });
});

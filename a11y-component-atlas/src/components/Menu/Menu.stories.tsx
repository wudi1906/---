import type { Meta, StoryObj } from "@storybook/react";
import { useState } from "react";
import { Menu, type MenuItemData } from "./Menu";

const meta: Meta<typeof Menu> = {
  title: "A11y/Menu",
  component: Menu,
};

export default meta;
type Story = StoryObj<typeof Menu>;

function Demo() {
  const [count, setCount] = useState<number>(0);
  const items: MenuItemData[] = [
    { id: "new", label: "New File", onSelect: () => setCount((c) => c + 1) },
    { id: "open", label: "Open..." },
    { id: "save", label: "Save", disabled: true },
    { id: "export", label: "Export" },
  ];

  return (
    <div className="p-6">
      <div className="mb-4 text-sm text-slate-600 dark:text-slate-300">Selected count: {count}</div>
      <Menu triggerLabel="Menu" items={items} />
    </div>
  );
}

export const Basic: Story = {
  render: () => <Demo />,
};



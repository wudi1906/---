import type { Meta, StoryObj } from "@storybook/react";
import { useState } from "react";
import { Menu, type MenuItemData } from "./Menu";
import { useI18n } from "@/i18n";

const meta: Meta<typeof Menu> = {
  title: "A11y/Menu",
  component: Menu,
};

export default meta;
type Story = StoryObj<typeof Menu>;

function Demo() {
  const [count, setCount] = useState<number>(0);
  const { t } = useI18n();
  const items: MenuItemData[] = [
    { id: "new", label: t("menu.items.new"), onSelect: () => setCount((c) => c + 1) },
    { id: "open", label: t("menu.items.open") },
    { id: "save", label: t("menu.items.save"), disabled: true },
    { id: "export", label: t("menu.items.export") },
  ];

  return (
    <div className="p-6">
      <div className="mb-4 text-sm text-slate-600 dark:text-slate-300">{t("menu.selectedCount", undefined, { count })}</div>
      <Menu triggerLabel={t("menu.trigger")} items={items} />
    </div>
  );
}

export const Basic: Story = {
  render: () => <Demo />,
};



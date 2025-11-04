import { useMemo, useState } from "react";
import type { Meta, StoryObj } from "@storybook/react";
import { Tabs, TabsList, TabsTrigger, TabsContent, TabsProps } from "./Tabs";
import { useI18n } from "@/i18n";

const meta: Meta<typeof Tabs> = {
  title: "Tabs",
  component: Tabs,
  parameters: {
    layout: "centered",
    docs: {
      description: {
        component: "Keyboard accessible tab system supporting controlled and uncontrolled usage.",
      },
    },
  },
  argTypes: {
    value: {
      control: "text",
      description: "Controlled tab value. When provided, `defaultValue` is ignored.",
    },
    defaultValue: {
      control: "text",
      description: "Initial tab for uncontrolled mode.",
    },
    onValueChange: {
      table: { disable: true },
    },
    children: {
      table: { disable: true },
    },
  },
};

export default meta;

type Story = StoryObj<typeof Tabs>;

function BasicStoryComponent(args: TabsProps) {
  const [current, setCurrent] = useState(args.value ?? args.defaultValue ?? "overview");
  const controlled = args.value !== undefined;
  const { t } = useI18n();
  const pricingItems = useMemo(
    () => t("tabs.basic.plan.items").split("\n").filter(Boolean),
    [t]
  );
  return (
    <Tabs
      {...args}
      value={controlled ? current : undefined}
      onValueChange={(next) => {
        setCurrent(next);
        args.onValueChange?.(next);
      }}
      defaultValue={controlled ? undefined : args.defaultValue}
      className="w-[420px]"
    >
      <TabsList>
        <TabsTrigger value="overview">{t("tabs.basic.overview.label")}</TabsTrigger>
        <TabsTrigger value="plan">{t("tabs.basic.plan.label", t("tabs.basic.plan.heading"))}</TabsTrigger>
        <TabsTrigger value="usage">{t("tabs.basic.usage.label")}</TabsTrigger>
      </TabsList>
      <TabsContent value="overview">
        <h3 className="text-sm font-semibold text-slate-900 dark:text-white">{t("tabs.basic.overview.heading")}</h3>
        <p className="mt-2 text-sm text-slate-600 dark:text-slate-300">{t("tabs.basic.overview.body")}</p>
      </TabsContent>
      <TabsContent value="plan">
        <h3 className="text-sm font-semibold text-slate-900 dark:text-white">{t("tabs.basic.plan.heading")}</h3>
        <ul className="mt-2 space-y-2 text-sm text-slate-600 dark:text-slate-300">
          {pricingItems.map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ul>
      </TabsContent>
      <TabsContent value="usage">
        <h3 className="text-sm font-semibold text-slate-900 dark:text-white">{t("tabs.basic.usage.heading")}</h3>
        <p className="mt-2 text-sm text-slate-600 dark:text-slate-300">{t("tabs.basic.usage.body")}</p>
      </TabsContent>
    </Tabs>
  );
}

export const Basic: Story = {
  render: (args) => <BasicStoryComponent {...args} />,
  args: {
    defaultValue: "overview",
  },
};

export const DefaultValue: Story = {
  render: () => {
    const { t } = useI18n();
    return (
      <Tabs defaultValue="reports" className="w-[420px]">
        <TabsList>
          <TabsTrigger value="dashboard">{t("tabs.default.dashboard.label")}</TabsTrigger>
          <TabsTrigger value="reports">{t("tabs.default.reports.label")}</TabsTrigger>
          <TabsTrigger value="notifications">{t("tabs.default.notifications.label")}</TabsTrigger>
        </TabsList>
        <TabsContent value="dashboard">
          <p className="text-sm text-slate-600 dark:text-slate-300">{t("tabs.default.dashboard.body")}</p>
        </TabsContent>
        <TabsContent value="reports">
          <p className="text-sm text-slate-600 dark:text-slate-300">{t("tabs.default.reports.body")}</p>
        </TabsContent>
        <TabsContent value="notifications">
          <p className="text-sm text-slate-600 dark:text-slate-300">{t("tabs.default.notifications.body")}</p>
        </TabsContent>
      </Tabs>
    );
  },
};

export const WithDisabledTab: Story = {
  render: () => {
    const { t } = useI18n();
    return (
      <Tabs defaultValue="details" className="w-[420px]">
        <TabsList>
          <TabsTrigger value="details">{t("tabs.disabled.details.label")}</TabsTrigger>
          <TabsTrigger value="insights">{t("tabs.disabled.insights.label")}</TabsTrigger>
          <TabsTrigger value="history" disabled>
            {[t("tabs.disabled.history.label"), t("tabs.disabled.history.suffix")]
              .filter((part) => part && part.length > 0)
              .join(" ")}
          </TabsTrigger>
        </TabsList>
        <TabsContent value="details">
          <p className="text-sm text-slate-600 dark:text-slate-300">{t("tabs.disabled.details.body")}</p>
        </TabsContent>
        <TabsContent value="insights">
          <p className="text-sm text-slate-600 dark:text-slate-300">{t("tabs.disabled.insights.body")}</p>
        </TabsContent>
        <TabsContent value="history">
          <p className="text-sm text-slate-600 dark:text-slate-300">{t("tabs.disabled.history.body")}</p>
        </TabsContent>
      </Tabs>
    );
  },
};

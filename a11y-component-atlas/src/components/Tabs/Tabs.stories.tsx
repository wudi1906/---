import { useState } from "react";
import type { Meta, StoryObj } from "@storybook/react";
import { Tabs, TabsList, TabsTrigger, TabsContent, TabsProps } from "./Tabs";

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
        <TabsTrigger value="overview">Overview</TabsTrigger>
        <TabsTrigger value="plan">Pricing Plan</TabsTrigger>
        <TabsTrigger value="usage">Usage</TabsTrigger>
      </TabsList>
      <TabsContent value="overview">
        <h3 className="text-sm font-semibold text-slate-900 dark:text-white">Overview</h3>
        <p className="mt-2 text-sm text-slate-600 dark:text-slate-300">
          Provide a quick summary of product or feature. Keep content concise and actionable.
        </p>
      </TabsContent>
      <TabsContent value="plan">
        <h3 className="text-sm font-semibold text-slate-900 dark:text-white">Pricing</h3>
        <ul className="mt-2 space-y-2 text-sm text-slate-600 dark:text-slate-300">
          <li>Starter – $29/mo</li>
          <li>Growth – $79/mo</li>
          <li>Enterprise – Contact us</li>
        </ul>
      </TabsContent>
      <TabsContent value="usage">
        <h3 className="text-sm font-semibold text-slate-900 dark:text-white">Usage</h3>
        <p className="mt-2 text-sm text-slate-600 dark:text-slate-300">
          Analytics and retention metrics appear here. Use tabs to separate logical sections of data.
        </p>
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
  render: () => (
    <Tabs defaultValue="reports" className="w-[420px]">
      <TabsList>
        <TabsTrigger value="dashboard">Dashboard</TabsTrigger>
        <TabsTrigger value="reports">Reports</TabsTrigger>
        <TabsTrigger value="notifications">Notifications</TabsTrigger>
      </TabsList>
      <TabsContent value="dashboard">
        <p className="text-sm text-slate-600 dark:text-slate-300">Current month metrics at a glance.</p>
      </TabsContent>
      <TabsContent value="reports">
        <p className="text-sm text-slate-600 dark:text-slate-300">Generate weekly and monthly PDF reports.</p>
      </TabsContent>
      <TabsContent value="notifications">
        <p className="text-sm text-slate-600 dark:text-slate-300">Manage email and in-app notification preferences.</p>
      </TabsContent>
    </Tabs>
  ),
};

export const WithDisabledTab: Story = {
  render: () => (
    <Tabs defaultValue="details" className="w-[420px]">
      <TabsList>
        <TabsTrigger value="details">Details</TabsTrigger>
        <TabsTrigger value="insights">Insights</TabsTrigger>
        <TabsTrigger value="history" disabled>
          History (coming soon)
        </TabsTrigger>
      </TabsList>
      <TabsContent value="details">
        <p className="text-sm text-slate-600 dark:text-slate-300">General information about the selected record.</p>
      </TabsContent>
      <TabsContent value="insights">
        <p className="text-sm text-slate-600 dark:text-slate-300">Derived insights and recommended actions.</p>
      </TabsContent>
      <TabsContent value="history">
        <p className="text-sm text-slate-600 dark:text-slate-300">Audit logs will be available soon.</p>
      </TabsContent>
    </Tabs>
  ),
};

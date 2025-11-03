import { useState } from "react";
import type { Meta, StoryObj } from "@storybook/react";
import { Modal, ModalProps } from "./Modal";

const meta: Meta<typeof Modal> = {
  title: "Modal",
  component: Modal,
  parameters: {
    layout: "centered",
    docs: {
      description: {
        component:
          "Accessible modal dialog with focus trapping, keyboard support, and multiple size presets.",
      },
    },
  },
  argTypes: {
    open: {
      table: { disable: true },
    },
    onOpenChange: {
      table: { disable: true },
    },
    title: {
      control: "text",
      description: "Modal heading or title",
    },
    description: {
      control: "text",
      description: "Short description that appears under the heading.",
    },
    size: {
      control: "radio",
      options: ["sm", "md", "lg"],
    },
  },
};

export default meta;

type Story = StoryObj<typeof Modal>;

const Template = (args: Omit<ModalProps, "open" | "onOpenChange">) => {
  const [open, setOpen] = useState(false);
  return (
    <div className="space-y-4">
      <button
        type="button"
        className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
        onClick={() => setOpen(true)}
      >
        Open modal
      </button>
      <Modal
        {...args}
        open={open}
        onOpenChange={(next) => {
          setOpen(next);
        }}
      />
    </div>
  );
};

export const Basic: Story = {
  render: () => (
    <Template
      title="Invite teammates"
      description="Share access to analytics with your colleagues."
      footer={
        <div className="flex gap-2">
          <button className="rounded-lg border border-slate-200 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2">
            Cancel
          </button>
          <button className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2">
            Send invite
          </button>
        </div>
      }
    >
      <p className="text-sm text-slate-600 dark:text-slate-300">
        Add teammates to collaborate on your dashboards. Invited users will receive an email with access
        instructions.
      </p>
      <form className="mt-4 space-y-3">
        <label className="block text-sm font-medium text-slate-700 dark:text-slate-200">
          Email
          <input
            type="email"
            className="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2 text-sm text-slate-900 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
            placeholder="name@example.com"
          />
        </label>
        <label className="block text-sm font-medium text-slate-700 dark:text-slate-200">
          Role
          <select className="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2 text-sm text-slate-900 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2">
            <option>Viewer</option>
            <option>Editor</option>
            <option>Admin</option>
          </select>
        </label>
      </form>
    </Template>
  ),
};

export const WithLongContent: Story = {
  render: () => (
    <Template
      title="Terms of service"
      description="Review and accept the updated policy."
      footer={
        <div className="flex gap-2">
          <button className="rounded-lg bg-slate-200 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-300 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2">
            Decline
          </button>
          <button className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2">
            Accept
          </button>
        </div>
      }
    >
      <div className="space-y-3 text-sm text-slate-600 dark:text-slate-300">
        {Array.from({ length: 8 }).map((_, index) => (
          <p key={index}>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer nec odio. Praesent libero. Sed cursus
            ante dapibus diam. Sed nisi. Nulla quis sem at nibh elementum imperdiet. Duis sagittis ipsum. Praesent
            mauris. Fusce nec tellus sed augue semper porta.
          </p>
        ))}
      </div>
    </Template>
  ),
};

export const Sizes: Story = {
  render: () => {
    const [openSize, setOpenSize] = useState<"sm" | "md" | "lg" | null>(null);
    return (
      <div className="flex gap-3">
        {(["sm", "md", "lg"] as const).map((size) => (
          <button
            key={size}
            type="button"
            onClick={() => setOpenSize(size)}
            className="rounded-lg bg-slate-200 px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-300 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
          >
            Open {size} modal
          </button>
        ))}
        {openSize ? (
          <Modal
            open={Boolean(openSize)}
            onOpenChange={(next) => {
              if (!next) {
                setOpenSize(null);
              }
            }}
            size={openSize}
            title={`Modal (${openSize})`}
            description="Each size changes the maximum width while keeping padding and typography consistent."
            footer={
              <button
                type="button"
                onClick={() => setOpenSize(null)}
                className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
              >
                Close
              </button>
            }
          >
            <p className="text-sm text-slate-600 dark:text-slate-300">
              Choose the size that best matches your content density. Smaller dialogs increase focus, larger ones are
              suited for forms or tables.
            </p>
          </Modal>
        ) : null}
      </div>
    );
  },
};

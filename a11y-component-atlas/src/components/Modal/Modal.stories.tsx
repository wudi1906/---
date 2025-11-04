import { useCallback, useMemo, useState } from "react";
import type { Meta, StoryObj } from "@storybook/react";
import { Modal, ModalProps } from "./Modal";
import { useI18n } from "@/i18n";

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

const Template = ({ triggerLabel, ...modalProps }: Omit<ModalProps, "open" | "onOpenChange"> & { triggerLabel?: string }) => {
  const [open, setOpen] = useState(false);
  const { t } = useI18n();
  return (
    <div className="space-y-4">
      <button
        type="button"
        className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
        onClick={() => setOpen(true)}
      >
        {triggerLabel ?? t("modal.trigger")}
      </button>
      <Modal
        {...modalProps}
        open={open}
        onOpenChange={(next) => {
          setOpen(next);
        }}
      />
    </div>
  );
};

export const Basic: Story = {
  render: () => {
    const { t } = useI18n();
    const roleOptions = useMemo(
      () => (["viewer", "editor", "admin"] as const).map((role) => ({
        value: role,
        label: t(`modal.invite.roles.${role}`),
      })),
      [t]
    );

    return (
      <Template
        title={t("modal.invite.title")}
        description={t("modal.invite.description")}
        footer={
          <div className="flex gap-2">
            <button className="rounded-lg border border-slate-200 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2">
              {t("modal.common.cancel")}
            </button>
            <button className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2">
              {t("modal.common.sendInvite")}
            </button>
          </div>
        }
      >
        <p className="text-sm text-slate-600 dark:text-slate-300">{t("modal.invite.body")}</p>
        <form className="mt-4 space-y-3">
          <label className="block text-sm font-medium text-slate-700 dark:text-slate-200">
            {t("modal.invite.emailLabel")}
            <input
              type="email"
              className="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2 text-sm text-slate-900 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
              placeholder={t("modal.invite.emailPlaceholder")}
            />
          </label>
          <label className="block text-sm font-medium text-slate-700 dark:text-slate-200">
            {t("modal.invite.roleLabel")}
            <select className="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2 text-sm text-slate-900 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2">
              {roleOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </label>
        </form>
      </Template>
    );
  },
};

export const WithLongContent: Story = {
  render: () => {
    const { t } = useI18n();
    const paragraphs = useMemo(
      () => t("modal.terms.paragraphs").split("\n").filter(Boolean),
      [t]
    );

    return (
      <Template
        title={t("modal.terms.title")}
        description={t("modal.terms.description")}
        footer={
          <div className="flex gap-2">
            <button className="rounded-lg bg-slate-200 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-300 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2">
              {t("modal.common.decline")}
            </button>
            <button className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2">
              {t("modal.common.accept")}
            </button>
          </div>
        }
      >
        <div className="space-y-3 text-sm text-slate-600 dark:text-slate-300">
          {paragraphs.map((paragraph, index) => (
            <p key={index}>{paragraph}</p>
          ))}
        </div>
      </Template>
    );
  },
};

export const Sizes: Story = {
  render: () => {
    const [openSize, setOpenSize] = useState<"sm" | "md" | "lg" | null>(null);
    const { t } = useI18n();
    const labelFor = useCallback(
      (size: "sm" | "md" | "lg") => t(`modal.sizes.sizes.${size}`),
      [t]
    );
    return (
      <div className="flex gap-3">
        {(["sm", "md", "lg"] as const).map((size) => (
          <button
            key={size}
            type="button"
            onClick={() => setOpenSize(size)}
            className="rounded-lg bg-slate-200 px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-300 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
          >
            {t("modal.sizes.openButton", undefined, { size: labelFor(size) })}
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
            title={t("modal.sizes.title", undefined, { size: labelFor(openSize) })}
            description={t("modal.sizes.description")}
            footer={
              <button
                type="button"
                onClick={() => setOpenSize(null)}
                className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
              >
                {t("modal.common.close")}
              </button>
            }
          >
            <p className="text-sm text-slate-600 dark:text-slate-300">{t("modal.sizes.body")}</p>
          </Modal>
        ) : null}
      </div>
    );
  },
};

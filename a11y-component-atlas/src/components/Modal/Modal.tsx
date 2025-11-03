import { useCallback, useEffect, useId, useMemo, useRef } from "react";
import type { ReactNode } from "react";
import { createPortal } from "react-dom";

export type ModalSize = "sm" | "md" | "lg";

export interface ModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  title: string | ReactNode;
  description?: string | ReactNode;
  children: ReactNode;
  footer?: ReactNode;
  size?: ModalSize;
}

const SIZE_MAP: Record<ModalSize, string> = {
  sm: "max-w-sm",
  md: "max-w-lg",
  lg: "max-w-2xl",
};

const FOCUSABLE_SELECTOR = [
  "a[href]",
  "button:not([disabled])",
  "textarea:not([disabled])",
  "input:not([disabled])",
  "select:not([disabled])",
  "[tabindex]:not([tabindex='-1'])",
].join(",");

function getFocusableElements(node: HTMLElement | null) {
  if (!node) return [] as HTMLElement[];
  return Array.from(node.querySelectorAll<HTMLElement>(FOCUSABLE_SELECTOR)).filter(
    (el) => !el.hasAttribute("disabled") && !el.getAttribute("aria-hidden")
  );
}

export function Modal({
  open,
  onOpenChange,
  title,
  description,
  children,
  footer,
  size = "md",
}: ModalProps) {
  const titleId = useId();
  const descriptionId = useId();
  const overlayRef = useRef<HTMLDivElement | null>(null);
  const dialogRef = useRef<HTMLDivElement | null>(null);
  const previouslyFocused = useRef<HTMLElement | null>(null);

  const portalTarget = typeof document !== "undefined" ? document.body : null;

  const closeModal = useCallback(() => {
    onOpenChange(false);
  }, [onOpenChange]);

  const handleBackdropMouseDown = useCallback(
    (event: React.MouseEvent) => {
      if (event.target === overlayRef.current) {
        closeModal();
      }
    },
    [closeModal]
  );

  const handleKeyDown = useCallback(
    (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        event.stopPropagation();
        closeModal();
      }

      if (event.key === "Tab") {
        const focusable = getFocusableElements(dialogRef.current);
        if (!focusable.length) {
          event.preventDefault();
          dialogRef.current?.focus();
          return;
        }

        const currentIndex = focusable.indexOf(document.activeElement as HTMLElement);
        let nextIndex = currentIndex;

        if (event.shiftKey) {
          nextIndex = currentIndex <= 0 ? focusable.length - 1 : currentIndex - 1;
        } else {
          nextIndex = currentIndex === focusable.length - 1 ? 0 : currentIndex + 1;
        }

        if (nextIndex !== currentIndex) {
          event.preventDefault();
          focusable[nextIndex].focus();
        }
      }
    },
    [closeModal]
  );

  useEffect(() => {
    if (!open) {
      const node = previouslyFocused.current;
      if (node && typeof node.focus === "function") {
        const focusNode = () => {
          node.focus();
        };
        if (typeof requestAnimationFrame === "function") {
          requestAnimationFrame(() => {
            requestAnimationFrame(focusNode);
          });
        } else {
          setTimeout(focusNode, 0);
        }
      }
      return;
    }

    previouslyFocused.current = document.activeElement as HTMLElement;

    const focusable = getFocusableElements(dialogRef.current);
    if (focusable.length) {
      focusable[0].focus();
    } else {
      dialogRef.current?.focus();
    }

    const handleKey = (event: KeyboardEvent) => handleKeyDown(event);
    document.addEventListener("keydown", handleKey, true);
    return () => document.removeEventListener("keydown", handleKey, true);
  }, [open, handleKeyDown]);

  const sizeClass = useMemo(() => SIZE_MAP[size], [size]);

  if (!open || !portalTarget) {
    return null;
  }

  return createPortal(
    <div
      ref={overlayRef}
      className="fixed inset-0 z-[999] flex items-center justify-center bg-slate-900/70 px-4 py-6"
      onMouseDown={handleBackdropMouseDown}
    >
      <div
        ref={dialogRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby={titleId}
        aria-describedby={description ? descriptionId : undefined}
        tabIndex={-1}
        className={`relative max-h-full w-full overflow-hidden rounded-2xl bg-white shadow-2xl dark:bg-slate-900 focus:outline-none ${sizeClass}`}
      >
        <header className="flex items-start justify-between gap-4 border-b border-slate-100 p-6 dark:border-slate-800">
          <div className="space-y-1">
            <h2 id={titleId} className="text-lg font-semibold text-slate-900 dark:text-slate-100">
              {title}
            </h2>
            {description ? (
              <p id={descriptionId} className="text-sm text-slate-600 dark:text-slate-400">
                {description}
              </p>
            ) : null}
          </div>
          <button
            type="button"
            onClick={closeModal}
            aria-label="Close dialog"
            className="rounded-full border border-transparent p-2 text-slate-500 transition hover:border-slate-200 hover:text-slate-900 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 dark:text-slate-300 dark:hover:text-slate-100"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </svg>
          </button>
        </header>
        <div className="max-h-[60vh] overflow-y-auto px-6 py-4 text-slate-700 dark:text-slate-200">
          {children}
        </div>
        {footer ? (
          <footer className="flex items-center justify-end gap-3 border-t border-slate-100 bg-slate-50 px-6 py-4 dark:border-slate-800 dark:bg-slate-900">
            {footer}
          </footer>
        ) : null}
      </div>
    </div>,
    portalTarget
  );
}

export default Modal;

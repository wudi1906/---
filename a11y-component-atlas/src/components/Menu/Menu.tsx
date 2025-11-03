import { useCallback, useEffect, useId, useMemo, useRef, useState } from "react";
import type { ReactNode } from "react";

export interface MenuItemData {
  id: string;
  label: ReactNode;
  disabled?: boolean;
  onSelect?: () => void;
}

export interface MenuProps {
  items: MenuItemData[];
  triggerLabel: string;
  open?: boolean;
  defaultOpen?: boolean;
  onOpenChange?: (open: boolean) => void;
}

function findNextEnabledIndex(items: MenuItemData[], start: number, direction: 1 | -1): number {
  const len = items.length;
  let i = start;
  for (let step = 0; step < len; step++) {
    i = (i + direction + len) % len;
    if (!items[i]?.disabled) return i;
  }
  return start;
}

export function Menu({ items, triggerLabel, open, defaultOpen = false, onOpenChange }: MenuProps) {
  const triggerId = useId();
  const menuId = useId();

  const rootRef = useRef<HTMLDivElement | null>(null);
  const menuRef = useRef<HTMLUListElement | null>(null);
  const triggerRef = useRef<HTMLButtonElement | null>(null);
  const previouslyFocused = useRef<HTMLElement | null>(null);

  const [internalOpen, setInternalOpen] = useState<boolean>(defaultOpen);
  const isOpen = open ?? internalOpen;

  const [activeIndex, setActiveIndex] = useState<number>(() => {
    const firstEnabled = items.findIndex((it) => !it.disabled);
    return firstEnabled === -1 ? 0 : firstEnabled;
  });

  const setOpen = useCallback(
    (next: boolean) => {
      if (onOpenChange) onOpenChange(next);
      if (open === undefined) setInternalOpen(next);
    },
    [onOpenChange, open]
  );

  const focusItemByIndex = useCallback(
    (index: number) => {
      const list = menuRef.current;
      if (!list) return;
      const buttons = list.querySelectorAll<HTMLButtonElement>('[role="menuitem"]');
      const btn = buttons[index];
      if (btn) btn.focus();
    },
    []
  );

  const closeMenu = useCallback(() => {
    setOpen(false);
  }, [setOpen]);

  const handleTriggerClick = useCallback(() => {
    setOpen(!isOpen);
  }, [isOpen, setOpen]);

  const handleOutsidePointerDown = useCallback(
    (event: MouseEvent) => {
      const root = rootRef.current;
      if (isOpen && root && event.target instanceof Node && !root.contains(event.target)) {
        closeMenu();
      }
    },
    [isOpen, closeMenu]
  );

  // Manage focus when opening/closing
  useEffect(() => {
    if (!isOpen) {
      const node = previouslyFocused.current || triggerRef.current;
      if (node && typeof node.focus === "function") {
        const focusNode = () => node.focus();
        if (typeof requestAnimationFrame === "function") {
          requestAnimationFrame(() => requestAnimationFrame(focusNode));
        } else {
          setTimeout(focusNode, 0);
        }
      }
      return;
    }

    previouslyFocused.current = (document.activeElement as HTMLElement) ?? null;

    const firstEnabled = items.findIndex((it) => !it.disabled);
    const nextIndex = firstEnabled === -1 ? 0 : firstEnabled;
    setActiveIndex(nextIndex);

    const focusFirst = () => focusItemByIndex(nextIndex);
    if (typeof requestAnimationFrame === "function") {
      requestAnimationFrame(() => requestAnimationFrame(focusFirst));
    } else {
      setTimeout(focusFirst, 0);
    }
  }, [isOpen, items, focusItemByIndex]);

  // Outside click to close
  useEffect(() => {
    if (!isOpen) return;
    document.addEventListener("mousedown", handleOutsidePointerDown, true);
    return () => document.removeEventListener("mousedown", handleOutsidePointerDown, true);
  }, [isOpen, handleOutsidePointerDown]);

  const onMenuKeyDown = useCallback(
    (event: React.KeyboardEvent<HTMLUListElement>) => {
      if (!isOpen) return;

      if (event.key === "Escape") {
        event.stopPropagation();
        closeMenu();
        return;
      }

      if (event.key === "ArrowDown") {
        event.preventDefault();
        const next = findNextEnabledIndex(items, activeIndex, 1);
        setActiveIndex(next);
        focusItemByIndex(next);
      } else if (event.key === "ArrowUp") {
        event.preventDefault();
        const prev = findNextEnabledIndex(items, activeIndex, -1);
        setActiveIndex(prev);
        focusItemByIndex(prev);
      } else if (event.key === "Home") {
        event.preventDefault();
        const first = items.findIndex((it) => !it.disabled);
        const idx = first === -1 ? 0 : first;
        setActiveIndex(idx);
        focusItemByIndex(idx);
      } else if (event.key === "End") {
        event.preventDefault();
        let idx = items.length - 1;
        while (idx > 0 && items[idx]?.disabled) idx -= 1;
        setActiveIndex(idx);
        focusItemByIndex(idx);
      } else if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        const item = items[activeIndex];
        if (item && !item.disabled) {
          item.onSelect?.();
          closeMenu();
        }
      } else if (event.key === "Tab") {
        // Keep focus within the menu while open
        event.preventDefault();
      }
    },
    [isOpen, items, activeIndex, focusItemByIndex, closeMenu]
  );

  const onItemClick = useCallback(
    (index: number) => {
      const item = items[index];
      if (!item || item.disabled) return;
      item.onSelect?.();
      closeMenu();
    },
    [items, closeMenu]
  );

  const menuItems = useMemo(() => items, [items]);

  useEffect(() => {
    if (!isOpen) return;
    focusItemByIndex(activeIndex);
  }, [isOpen, activeIndex, focusItemByIndex]);

  return (
    <div ref={rootRef} className="relative inline-block align-middle">
      <button
        id={triggerId}
        ref={triggerRef}
        type="button"
        aria-haspopup="menu"
        aria-expanded={isOpen}
        aria-controls={menuId}
        onClick={handleTriggerClick}
        className="rounded-md border border-slate-200 bg-white px-3 py-1.5 text-sm font-medium text-slate-700 shadow-sm hover:bg-slate-50 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-200"
      >
        {triggerLabel}
      </button>

      {isOpen ? (
        <ul
          ref={menuRef}
          role="menu"
          id={menuId}
          aria-labelledby={triggerId}
          onKeyDown={onMenuKeyDown}
          className="absolute left-0 z-[1000] mt-2 min-w-[12rem] overflow-hidden rounded-md border border-slate-200 bg-white p-1 shadow-lg outline-none dark:border-slate-700 dark:bg-slate-900"
        >
          {menuItems.map((item, index) => (
            <li key={item.id} role="none">
              <button
                role="menuitem"
                type="button"
                aria-disabled={item.disabled || undefined}
                tabIndex={index === activeIndex ? 0 : -1}
                onClick={() => onItemClick(index)}
                className={
                  "flex w-full cursor-default select-none items-center gap-2 rounded px-3 py-1.5 text-left text-sm transition focus:outline-none focus-visible:bg-slate-100 disabled:cursor-not-allowed disabled:opacity-50 dark:focus-visible:bg-slate-800"
                }
              >
                {item.label}
              </button>
            </li>
          ))}
        </ul>
      ) : null}
    </div>
  );
}

export default Menu;



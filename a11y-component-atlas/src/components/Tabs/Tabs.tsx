import {
  Children,
  KeyboardEvent,
  cloneElement,
  forwardRef,
  isValidElement,
  useCallback,
  useEffect,
  useId,
  useMemo,
  useRef,
  useState,
  createContext,
  useContext,
} from "react";
import type { ComponentPropsWithoutRef, ReactElement, ReactNode } from "react";
import { cx } from "class-variance-authority";

interface TabsContextValue {
  selected: string | null;
  setSelected: (value: string) => void;
  register: (value: string, ref: HTMLButtonElement | null, disabled: boolean) => void;
  unregister: (value: string) => void;
  getPanelId: (value: string) => string;
  getTriggerId: (value: string) => string;
}

const TabsContext = createContext<TabsContextValue | undefined>(undefined);

function useTabsContext(component: string): TabsContextValue {
  const ctx = useContext(TabsContext);
  if (!ctx) {
    throw new Error(`${component} must be used within <Tabs>`);
  }
  return ctx;
}

export interface TabsProps {
  value?: string;
  defaultValue?: string;
  onValueChange?: (value: string) => void;
  children: ReactNode;
  className?: string;
}

interface TabRegistration {
  value: string;
  ref: HTMLButtonElement | null;
  disabled: boolean;
}

export function Tabs({ value, defaultValue, onValueChange, children, className }: TabsProps) {
  const baseId = useId();
  const isControlled = value !== undefined;
  const [internalValue, setInternalValue] = useState<string | null>(defaultValue ?? null);
  const selected = isControlled ? value ?? null : internalValue;
  const registry = useRef<Map<string, TabRegistration>>(new Map());

  const setSelected = useCallback(
    (next: string) => {
      if (!isControlled) {
        setInternalValue(next);
      }
      onValueChange?.(next);
    },
    [isControlled, onValueChange]
  );

  const register = useCallback((tabValue: string, ref: HTMLButtonElement | null, disabled: boolean) => {
    registry.current.set(tabValue, { value: tabValue, ref, disabled });
  }, []);

  const unregister = useCallback((tabValue: string) => {
    registry.current.delete(tabValue);
  }, []);

  const getPanelId = useCallback((tabValue: string) => `${baseId}-panel-${tabValue}`, [baseId]);
  const getTriggerId = useCallback((tabValue: string) => `${baseId}-trigger-${tabValue}`, [baseId]);

  const contextValue = useMemo(
    () => ({
      selected: selected ?? null,
      setSelected,
      register,
      unregister,
      getPanelId,
      getTriggerId,
    }),
    [selected, setSelected, register, unregister, getPanelId, getTriggerId]
  );

  return (
    <TabsContext.Provider value={contextValue}>
      <div className={cx("flex w-full flex-col gap-4", className)}>{children}</div>
    </TabsContext.Provider>
  );
}

export interface TabsListProps extends ComponentPropsWithoutRef<"div"> {}

const getFocusableTabs = (registry: Map<string, TabRegistration>) =>
  Array.from(registry.values()).filter((entry) => !entry.disabled && entry.ref);

export const TabsList = forwardRef<HTMLDivElement, TabsListProps>(function TabsList(
  { className, children, ...props },
  ref
) {
  const { selected, register, unregister, setSelected, getPanelId, getTriggerId } = useTabsContext("Tabs.List");
  const localRegistry = useRef<Map<string, TabRegistration>>(new Map());

  useEffect(() => {
    localRegistry.current.forEach((entry) => register(entry.value, entry.ref, entry.disabled));
    return () => {
      localRegistry.current.forEach((entry) => unregister(entry.value));
    };
  }, [register, unregister]);

  const handleKeyDown = useCallback(
    (event: KeyboardEvent<HTMLDivElement>) => {
      const focusableTabs = getFocusableTabs(localRegistry.current);
      if (!focusableTabs.length) return;

      const currentIndex = focusableTabs.findIndex((entry) => entry.value === selected);
      const first = focusableTabs[0];
      const last = focusableTabs[focusableTabs.length - 1];

      let nextEntry: TabRegistration | undefined;

      switch (event.key) {
        case "ArrowRight":
        case "ArrowDown": {
          const nextIndex = currentIndex === -1 || currentIndex === focusableTabs.length - 1 ? 0 : currentIndex + 1;
          nextEntry = focusableTabs[nextIndex];
          break;
        }
        case "ArrowLeft":
        case "ArrowUp": {
          const nextIndex = currentIndex <= 0 ? focusableTabs.length - 1 : currentIndex - 1;
          nextEntry = focusableTabs[nextIndex];
          break;
        }
        case "Home": {
          nextEntry = first;
          break;
        }
        case "End": {
          nextEntry = last;
          break;
        }
        default:
          return;
      }

      if (nextEntry && nextEntry.ref) {
        event.preventDefault();
        nextEntry.ref.focus({ preventScroll: true });
        setSelected(nextEntry.value);
      }
    },
    [selected, setSelected]
  );

  const decoratedChildren = Children.map(children, (child) => {
    if (!isValidElement(child)) return child;
    return cloneElement(child as ReactElement, {
      register,
      unregister,
      tabsRegistry: localRegistry,
      getPanelId,
      getTriggerId,
      setSelected,
      selected,
    });
  });

  return (
    <div
      role="tablist"
      ref={ref}
      className={cx("inline-flex items-center gap-1 rounded-xl bg-slate-100 p-1 dark:bg-slate-800", className)}
      onKeyDown={handleKeyDown}
      {...props}
    >
      {decoratedChildren}
    </div>
  );
});

interface TabsTriggerProps extends ComponentPropsWithoutRef<"button"> {
  value: string;
  disabled?: boolean;
  register?: TabsContextValue["register"];
  unregister?: TabsContextValue["unregister"];
  tabsRegistry?: React.MutableRefObject<Map<string, TabRegistration>>;
  getPanelId?: TabsContextValue["getPanelId"];
  getTriggerId?: TabsContextValue["getTriggerId"];
  setSelected?: TabsContextValue["setSelected"];
  selected?: string | null;
}

export const TabsTrigger = forwardRef<HTMLButtonElement, TabsTriggerProps>(function TabsTrigger(
  {
    value,
    disabled = false,
    className,
    children,
    register,
    unregister,
    tabsRegistry,
    getPanelId,
    getTriggerId,
    setSelected,
    selected,
    ...props
  },
  ref
) {
  const innerRef = useRef<HTMLButtonElement | null>(null);

  const composedRef = useCallback(
    (node: HTMLButtonElement | null) => {
      innerRef.current = node;
      if (typeof ref === "function") {
        ref(node);
      } else if (ref) {
        (ref as React.MutableRefObject<HTMLButtonElement | null>).current = node;
      }
      tabsRegistry?.current.set(value, { value, ref: node, disabled });
      register?.(value, node, disabled);
    },
    [disabled, ref, register, tabsRegistry, value]
  );

  useEffect(
    () => () => {
      unregister?.(value);
      tabsRegistry?.current.delete(value);
    },
    [unregister, tabsRegistry, value]
  );

  const isSelected = selected === value;

  return (
    <button
      type="button"
      role="tab"
      ref={composedRef}
      className={cx(
        "rounded-lg px-3 py-2 text-sm font-medium transition focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2",
        disabled && "cursor-not-allowed opacity-40",
        isSelected
          ? "bg-white text-slate-900 shadow-sm dark:bg-slate-700 dark:text-white"
          : "text-slate-600 hover:text-slate-900 dark:text-slate-300 dark:hover:text-white"
      )}
      aria-selected={isSelected}
      aria-controls={getPanelId?.(value)}
      id={getTriggerId?.(value)}
      tabIndex={isSelected ? 0 : -1}
      disabled={disabled}
      onClick={() => {
        if (!disabled) {
          setSelected?.(value);
        }
      }}
      {...props}
    >
      {children}
    </button>
  );
});

interface TabsContentProps extends ComponentPropsWithoutRef<"div"> {
  value: string;
}

export const TabsContent = forwardRef<HTMLDivElement, TabsContentProps>(function TabsContent(
  { value, className, children, ...props },
  ref
) {
  const { selected, getPanelId, getTriggerId } = useTabsContext("Tabs.Content");
  const isSelected = selected === value;

  return (
    <div
      ref={ref}
      role="tabpanel"
      tabIndex={0}
      hidden={!isSelected}
      aria-labelledby={getTriggerId(value)}
      id={getPanelId(value)}
      className={cx(
        "rounded-xl border border-slate-200 bg-white p-6 text-slate-700 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-200",
        !isSelected && "hidden",
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
});

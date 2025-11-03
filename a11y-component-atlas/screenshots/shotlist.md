# Screenshot Checklist — A11y Component Atlas

## Required Screenshots (5 images)

### 1. storybook-home.png (1280x720)
**What to capture**: Storybook interface at http://localhost:8505  
**Key elements**:
- Storybook sidebar navigation
- Component list (Button, Input, Modal, Tabs, Menu)
- Welcome/intro page content
- Theme toggle in toolbar
- Accessibility addon tab

**How to capture**:
1. Open http://localhost:8505
2. Wait for Storybook to fully load
3. Expand component folders in sidebar
4. Capture showing sidebar + main content
5. Save as `storybook-home.png`

---

### 2. button-variants.png (1280x720)
**What to capture**: Button component variants  
**Key elements**:
- All button variants (primary, secondary, outline, ghost)
- All sizes (sm, md, lg)
- Disabled states
- Focus indicators (keyboard navigation)
- Props controls panel

**How to capture**:
1. Navigate to Button component in Storybook
2. Select "All Variants" story (or create a view showing all)
3. Capture grid of button variations
4. Save as `button-variants.png`

---

### 3. modal-component.png (1280x720)
**What to capture**: Modal component demo  
**Key elements**:
- Open modal with overlay
- Modal title and content
- Close button (X)
- Action buttons (Cancel/Confirm)
- Focus trap indicator
- Backdrop blur effect

**How to capture**:
1. Navigate to Modal component
2. Click "Open" button in story
3. Capture modal in open state
4. Save as `modal-component.png`

---

### 4. keyboard-navigation.png (1280x720)
**What to capture**: Keyboard focus indicators  
**Key elements**:
- Component with visible focus ring (blue outline)
- Tab key sequence illustration
- ARIA live region announcements
- Focus trap demonstration (e.g., in Modal)

**How to capture**:
1. Navigate to any interactive component
2. Press Tab key to show focus ring
3. Capture with focus indicator visible
4. Save as `keyboard-navigation.png`

---

### 5. theme-toggle.gif (800x600, <5MB)
**What to capture**: Light/dark theme switching  
**Steps to record**:
1. Open Storybook at http://localhost:8505
2. Navigate to Button or Input component
3. Click theme toggle in Storybook toolbar (moon/sun icon)
4. Show components switching from light → dark theme
5. Toggle back to light theme
6. Show smooth transition

**Duration**: 10-15 seconds  
**Save as**: `theme-toggle.gif`

---

## Placeholder Files

```bash
cd a11y-component-atlas/screenshots
touch storybook-home.png
touch button-variants.png
touch modal-component.png
touch keyboard-navigation.png
touch theme-toggle.gif
```

---

*Last Updated: 2025-11-03*


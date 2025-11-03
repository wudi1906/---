# Screenshots & Visual Assets

This directory contains screenshots, GIFs, and visual assets for all portfolio projects, used in:
- Fiverr/Upwork gig listings
- README documentation
- Demo presentations
- Marketing materials

## 📸 Screenshot Checklist

### Global Price Sentinel (Project 1)
**Location**: `global-price-sentinel/screenshots/`

- [ ] `hero-dashboard.png` (1280x720) — Main portal showing 6 projects
- [ ] `price-monitor-settings.png` (1280x720) — Monitor configuration page
- [ ] `price-report.png` (1280x720) — HTML price trend report
- [ ] `api-docs.png` (1280x720) — FastAPI Swagger UI
- [ ] `demo-workflow.gif` (800x600, <5MB) — Import demo → view report loop

**Key Elements to Capture**:
- Gradient background, white cards
- Monitor settings with proxy/alert config
- Price chart with trend lines
- Alert logs table

---

### Event Relay Hub (Project 2)
**Location**: `event-relay-hub/screenshots/`

- [ ] `landing-page.png` (1280x720) — English landing page with 4 feature cards
- [ ] `events-console.png` (1280x720) — Events console with filters
- [ ] `signature-settings.png` (1280x720) — Signature templates management
- [ ] `dlq-management.png` (1280x720) — Dead-letter queue interface
- [ ] `webhook-workflow.gif` (800x600) — Receive event → forward → DLQ → replay

**Key Elements to Capture**:
- Events list with source/type badges
- Signature config form (GitHub/Stripe/Custom)
- DLQ batch operations (replay/delete/clear)
- Success rate stats

---

### SaaS Northstar Dashboard (Project 3)
**Location**: `saas-northstar-dashboard/screenshots/`

- [ ] `dashboard-home.png` (1280x720) — Main dashboard with MRR/ARR/Churn cards
- [ ] `csv-import-wizard.png` (1280x720) — Multi-step import interface
- [ ] `trend-charts.png` (1280x720) — Chart.js trend visualizations
- [ ] `mobile-view.png` (375x812) — Mobile responsive layout
- [ ] `import-workflow.gif` (800x600) — Upload CSV → field mapping → see charts

**Key Elements to Capture**:
- KPI metric cards with trend arrows
- Interactive charts (line/bar)
- CSV import step-by-step flow
- Export PNG/PDF buttons

---

### Doc Knowledge Forge (Project 4)
**Location**: `doc-knowledge-forge/screenshots/`

- [ ] `upload-interface.png` (1280x720) — Document upload zone
- [ ] `search-results.png` (1280x720) — Full-text search with highlighting
- [ ] `markdown-viewer.png` (1280x720) — Online Markdown viewer
- [ ] `stats-dashboard.png` (1280x720) — Document stats (total/size/recent)
- [ ] `upload-workflow.gif` (800x600) — Upload PDF → search → view Markdown

**Key Elements to Capture**:
- Drag-and-drop upload zone
- Search results with keyword highlights
- Tag chips and file type badges
- Markdown preview with syntax highlighting

---

### A11y Component Atlas (Project 5)
**Location**: `a11y-component-atlas/screenshots/`

- [ ] `storybook-home.png` (1280x720) — Storybook sidebar and welcome page
- [ ] `button-variants.png` (1280x720) — Button component variants
- [ ] `modal-component.png` (1280x720) — Modal with focus trap demo
- [ ] `keyboard-navigation.png` (1280x720) — Tab key focus indicators
- [ ] `theme-toggle.gif` (800x600) — Switch light/dark theme

**Key Elements to Capture**:
- Storybook controls panel
- Component variants grid
- Focus ring on keyboard navigation
- axe accessibility addon panel (all green)

---

### Insight Viz Studio (Project 6)
**Location**: `insight-viz-studio/screenshots/`

- [ ] `upload-interface.png` (1280x720) — CSV upload and feature cards
- [ ] `chart-preview.png` (1280x720) — ECharts interactive chart
- [ ] `export-options.png` (1280x720) — Export PNG/PDF buttons
- [ ] `data-preview.png` (1280x720) — CSV data preview table
- [ ] `chart-workflow.gif` (800x600) — Upload data → generate chart → export

**Key Elements to Capture**:
- File upload zone with sample data
- ECharts line/bar/pie charts
- Interactive tooltips
- Export success confirmation

---

## 📐 Screenshot Specifications

### Image Requirements
- **Resolution**: 1280x720 pixels minimum (1920x1080 preferred for Fiverr)
- **Format**: PNG (lossless) or JPG (85%+ quality)
- **File Size**: <2MB per image
- **Naming**: kebab-case, descriptive (e.g., `price-report-dashboard.png`)

### GIF Requirements
- **Resolution**: 800x600 or 1280x720
- **Duration**: 10-30 seconds
- **File Size**: <5MB (use optimization tools)
- **Frame Rate**: 15-20 fps
- **Loop**: Yes (infinite loop)

### Content Guidelines
- **Clean Data**: Use realistic but anonymized data
- **No Personal Info**: No real emails, names, sensitive data
- **Branding**: Keep placeholder logos/colors
- **UI State**: Show success states, not errors
- **Call-to-Action**: Highlight key buttons/features

## 🛠️ Tools for Creating Assets

### Screenshot Tools
- **Windows**: Snipping Tool, ShareX, Greenshot
- **Mac**: Cmd+Shift+4, CleanShot X
- **Browser**: Chrome DevTools device toolbar (for responsive)

### GIF Recording Tools
- **ScreenToGif** (Windows, free)
- **LICEcap** (Windows/Mac, free)
- **Kap** (Mac, free)
- **Gifox** (Mac, paid)

### Image Optimization
- **TinyPNG**: https://tinypng.com/ (compress PNG/JPG)
- **Squoosh**: https://squoosh.app/ (advanced compression)
- **ezgif**: https://ezgif.com/ (GIF optimization)

## 📋 Capture Process

1. **Start all services**: Run `.\start-all.ps1`
2. **Wait for ready**: Run `.\TEST_ALL.bat`, confirm all [OK]
3. **Import demo data**: Click "Import Demo" in Portal for each project
4. **Open each project**: Navigate to localhost:8101, 8202, etc.
5. **Set browser zoom**: 100% (Cmd/Ctrl + 0)
6. **Hide browser chrome**: F11 (fullscreen) or use browser screenshot tools
7. **Capture screenshots**: Follow checklist above
8. **Record GIFs**: Focus on key workflows (3-5 clicks max)
9. **Optimize files**: Compress images to <2MB, GIFs to <5MB
10. **Organize**: Save to respective `screenshots/` directories

## 📊 Asset Status Tracking

| Project | Screenshots | GIFs | Status |
|---------|-------------|------|--------|
| Global Price Sentinel | 0/5 | 0/1 | 🔴 Not Started |
| Event Relay Hub | 0/5 | 0/1 | 🔴 Not Started |
| SaaS Northstar Dashboard | 0/5 | 0/1 | 🔴 Not Started |
| Doc Knowledge Forge | 0/5 | 0/1 | 🔴 Not Started |
| A11y Component Atlas | 0/5 | 0/1 | 🔴 Not Started |
| Insight Viz Studio | 0/5 | 0/1 | 🔴 Not Started |

**Total Progress**: 0/30 screenshots, 0/6 GIFs

---

## 🎯 Next Steps

1. **Capture screenshots**: Follow checklist, one project at a time
2. **Create GIFs**: Record key workflows (10-30 seconds each)
3. **Optimize assets**: Compress to meet size requirements
4. **Update READMEs**: Link screenshots in README.en.md files
5. **Upload to Fiverr**: Use in gig galleries when publishing

---

**Note**: These are placeholders. You'll need to capture actual screenshots once you're ready to publish on Fiverr.

*Last Updated: 2025-11-03*


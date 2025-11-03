# Screenshot Checklist — SaaS Northstar Dashboard

## Required Screenshots (5 images)

### 1. dashboard-home.png (1280x720)
**What to capture**: Main dashboard at http://localhost:8303  
**Key elements**:
- KPI metric cards (MRR, ARR, Churn Rate, LTV)
- Trend arrows (up/down indicators)
- Time range selector (7d/30d/90d)
- Interactive charts below metrics

**How to capture**:
1. Import demo data first (Portal → Import Demo for P3)
2. Open http://localhost:8303
3. Wait for charts to load
4. Capture full dashboard view
5. Save as `dashboard-home.png`

---

### 2. csv-import-wizard.png (1280x720)
**What to capture**: CSV import interface at http://localhost:8303/import  
**Key elements**:
- Template selector dropdown
- File upload zone
- Field mapping interface
- Preview data table
- Import button

**How to capture**:
1. Open http://localhost:8303/import
2. Select a template (B2B SaaS or B2C Growth)
3. Show upload zone ready state
4. Capture the import wizard
5. Save as `csv-import-wizard.png`

---

### 3. trend-charts.png (1280x720)
**What to capture**: Chart.js visualizations  
**Key elements**:
- MRR trend line chart
- Churn rate area chart
- Interactive tooltips (hover state)
- Chart legend
- Time period labels

**How to capture**:
1. Ensure demo data is imported
2. Scroll to charts section on main page
3. Hover over chart to show tooltip
4. Capture chart area
5. Save as `trend-charts.png`

---

### 4. mobile-view.png (375x812)
**What to capture**: Mobile responsive layout  
**Key elements**:
- Stacked metric cards
- Responsive charts
- Touch-friendly buttons
- Hamburger menu (if applicable)

**How to capture**:
1. Open http://localhost:8303
2. Press F12, enable device toolbar
3. Select iPhone 13 Pro (375x812)
4. Capture full mobile view
5. Save as `mobile-view.png`

---

### 5. import-workflow.gif (800x600, <5MB)
**What to capture**: CSV import process  
**Steps to record**:
1. Open http://localhost:8303/import
2. Select template
3. Upload sample CSV
4. Show field mapping
5. Click Import
6. Navigate back to dashboard
7. Show updated metrics/charts

**Duration**: 20-30 seconds  
**Save as**: `import-workflow.gif`

---

## Placeholder Files

```bash
cd saas-northstar-dashboard/screenshots
touch dashboard-home.png
touch csv-import-wizard.png
touch trend-charts.png
touch mobile-view.png
touch import-workflow.gif
```

---

*Last Updated: 2025-11-03*


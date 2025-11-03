# Screenshot Checklist — Insight Viz Studio

## Required Screenshots (5 images)

### 1. upload-interface.png (1280x720)
**What to capture**: Main page at http://localhost:8606  
**Key elements**:
- Hero title "Insight Viz Studio — Data to Charts in Minutes"
- 4 feature cards (Upload, Recommendations, Themes, Export)
- Upload dropzone with file chooser
- Sample ECharts visualization
- CTA buttons (API Docs, View Datasets, Import/Reset Demo)

**How to capture**:
1. Open http://localhost:8606
2. Ensure page fully loaded
3. Capture showing hero + features + chart
4. Save as `upload-interface.png`

---

### 2. chart-preview.png (1280x720)
**What to capture**: Interactive ECharts visualization  
**Key elements**:
- Chart title "Sample Data Visualization"
- Line chart with data points
- Interactive tooltip (hover state)
- Legend
- Axis labels with values

**How to capture**:
1. Open http://localhost:8606
2. Scroll to chart section
3. Hover mouse over chart to trigger tooltip
4. Capture chart area with tooltip visible
5. Save as `chart-preview.png`

---

### 3. export-options.png (1280x720)
**What to capture**: Export and action buttons  
**Key elements**:
- API Docs button
- View Datasets button
- Import Demo button (secondary style)
- Reset Demo button (secondary style)
- Chart export functionality (if available in UI)

**How to capture**:
1. Scroll to buttons section
2. Capture showing all 4 buttons
3. Save as `export-options.png`

---

### 4. data-preview.png (1280x720)
**What to capture**: Datasets API response  
**Key elements**:
- JSON response showing dataset list
- File names, sizes, created dates
- Sample data preview (rows/columns)

**How to capture**:
1. Import demo data (Portal → Import Demo for P6)
2. Visit http://localhost:8606/api/datasets
3. Capture JSON response
4. Or use Postman screenshot
5. Save as `data-preview.png`

---

### 5. chart-workflow.gif (800x600, <5MB)
**What to capture**: Complete chart generation flow  
**Steps to record**:
1. Open http://localhost:8606
2. Click "Import Demo"
3. Wait for success alert
4. Click "View Datasets"
5. Navigate back to main page
6. Scroll to chart
7. Hover over chart to show tooltip
8. Scroll to buttons
9. Highlight "API Docs" button

**Duration**: 20-25 seconds  
**Save as**: `chart-workflow.gif`

---

## Placeholder Files

```bash
cd insight-viz-studio/screenshots
touch upload-interface.png
touch chart-preview.png
touch export-options.png
touch data-preview.png
touch chart-workflow.gif
```

---

*Last Updated: 2025-11-03*

# Screenshot Checklist — Doc Knowledge Forge

## Required Screenshots (5 images)

### 1. upload-interface.png (1280x720)
**What to capture**: Document upload page at http://localhost:8404  
**Key elements**:
- Hero title "Doc Knowledge Forge"
- Search bar
- Upload dropzone with drag-and-drop
- Import Demo / Reset Data buttons
- Stats cards (Total Docs, Storage, Recent 24h)

**How to capture**:
1. Open http://localhost:8404
2. Ensure page is fully loaded
3. Capture full view showing all 3 sections
4. Save as `upload-interface.png`

---

### 2. search-results.png (1280x720)
**What to capture**: Search results with highlighting  
**Key elements**:
- Search input with keyword
- Search results cards
- Keyword highlighting (yellow background)
- Relevance scores
- "View Online" / "Preview Chunk" buttons

**How to capture**:
1. Import demo data first (Portal → Import Demo for P4)
2. Enter search keyword (e.g., "policy")
3. Press Search button
4. Wait for results to appear
5. Capture showing highlighted results
6. Save as `search-results.png`

---

### 3. markdown-viewer.png (1280x720)
**What to capture**: Online Markdown viewer  
**Key elements**:
- Document title
- Markdown rendered content
- Code syntax highlighting (if present)
- Table of contents (if available)
- Download/export options

**How to capture**:
1. From search results or document list
2. Click "View Online" on any document
3. Capture the viewer page
4. Save as `markdown-viewer.png`

---

### 4. stats-dashboard.png (1280x720)
**What to capture**: Statistics section  
**Key elements**:
- Total documents count
- Storage size (formatted)
- Recent uploads (24h)
- Document type breakdown (if available)

**How to capture**:
1. Import multiple demo docs
2. Scroll to stats section on main page
3. Capture stats cards showing non-zero values
4. Save as `stats-dashboard.png`

---

### 5. upload-workflow.gif (800x600, <5MB)
**What to capture**: Complete upload and search flow  
**Steps to record**:
1. Open http://localhost:8404
2. Click "Import Demo"
3. Wait for success notification
4. Enter search keyword
5. Click Search
6. Show results with highlights
7. Click "View Online" on one result
8. Show Markdown preview

**Duration**: 20-30 seconds  
**Save as**: `upload-workflow.gif`

---

## Placeholder Files

```bash
cd doc-knowledge-forge/screenshots
touch upload-interface.png
touch search-results.png
touch markdown-viewer.png
touch stats-dashboard.png
touch upload-workflow.gif
```

---

*Last Updated: 2025-11-03*


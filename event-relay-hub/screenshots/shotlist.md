# Screenshot Checklist — Event Relay Hub

## Required Screenshots (5 images)

### 1. landing-page.png (1280x720)
**What to capture**: English landing page at http://localhost:8202  
**Key elements**:
- Hero title "Event Relay Hub — Unified Webhook Management"
- 4 feature cards (Multi-source, Signature, Replay & DLQ, Visual console)
- CTA buttons (API Docs, Events Console, Import/Reset Demo)
- Webhook endpoints list

**How to capture**:
1. Open http://localhost:8202
2. Ensure all content is visible
3. Capture full page
4. Save as `landing-page.png`

---

### 2. events-console.png (1280x720)
**What to capture**: Events console at http://localhost:8202/console/events  
**Key elements**:
- Recent events table with source/type/timestamp
- Filter controls (source, event type, date range)
- Pagination controls
- Batch action buttons (Replay selected, Delete, Clear DLQ)
- Event count statistics

**How to capture**:
1. Import demo data first (Portal → Import Demo for P2)
2. Open http://localhost:8202/console/events
3. Ensure table shows sample events
4. Capture full page
5. Save as `events-console.png`

---

### 3. signature-settings.png (1280x720)
**What to capture**: Signature templates at http://localhost:8202/console/signatures  
**Key elements**:
- GitHub/Stripe/Custom signature cards
- Enable/disable toggles
- Secret key input fields (masked)
- Test signature button
- Example curl command

**How to capture**:
1. Open http://localhost:8202/console/signatures
2. Enable at least one source (GitHub or Stripe)
3. Capture showing the config interface
4. Save as `signature-settings.png`

---

### 4. dlq-management.png (1280x720)
**What to capture**: Dead-letter queue view  
**Key elements**:
- DLQ list with failed events
- Retry count badges
- Last error messages
- Batch replay buttons
- Clear all button

**How to capture**:
1. Create some DLQ entries (or use Postman to simulate failures)
2. Visit console/events or use API /api/dlq
3. Capture DLQ interface showing retry options
4. Save as `dlq-management.png`

---

### 5. webhook-workflow.gif (800x600, <5MB)
**What to capture**: Complete webhook flow  
**Steps to record**:
1. Open http://localhost:8202
2. Click "Import Demo"
3. Click "Events Console"
4. Show events list populating
5. Click on one event to expand
6. Click "Replay" button
7. Show success/failure notification

**Duration**: 15-25 seconds  
**Save as**: `webhook-workflow.gif`

---

## Placeholder Files

```bash
cd event-relay-hub/screenshots
touch landing-page.png
touch events-console.png
touch signature-settings.png
touch dlq-management.png
touch webhook-workflow.gif
```

---

*Last Updated: 2025-11-03*


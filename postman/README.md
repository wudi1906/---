# Postman Collections — API Testing & Demo Workflows

This directory contains Postman collections for all portfolio projects, demonstrating complete user workflows from setup to data export.

## 📦 Collections

| Project | Collection File | Endpoints | Storyline |
|---------|----------------|-----------|-----------|
| Global Price Sentinel | [../global-price-sentinel/postman/global_price_sentinel.postman_collection.json](../global-price-sentinel/postman/) | 8+ | Health check → Seed data → Run monitor → View records → Generate report |
| Event Relay Hub | [../event-relay-hub/postman/event_relay_hub.postman_collection.json](../event-relay-hub/postman/event_relay_hub.postman_collection.json) | 15+ | Health → Seed → Send webhook → Replay → DLQ management → Clear |
| SaaS Northstar Dashboard | [../saas-northstar-dashboard/postman/saas_northstar_dashboard.postman_collection.json](../saas-northstar-dashboard/postman/saas_northstar_dashboard.postman_collection.json) | 6+ | Health → Templates → Seed → Import CSV → Export → Latest |
| Doc Knowledge Forge | [../doc-knowledge-forge/postman/doc_knowledge_forge.postman_collection.json](../doc-knowledge-forge/postman/doc_knowledge_forge.postman_collection.json) | 8+ | Health → Seed → Upload docs → Search → Get chunks → Stats |
| A11y Component Atlas | N/A | N/A | Storybook UI, no backend API |
| Insight Viz Studio | TBD | 6+ | Health → Seed → Upload data → Generate chart → Export |

## 🎯 Storyline Structure

Each collection follows a "from zero to value" narrative:

### Standard Flow
1. **Health Check** — Verify service is running
2. **Import Demo Data** — Seed database with sample data
3. **Core Action** — Main feature demo (monitor/webhook/import/search)
4. **View Results** — Query data, view outputs
5. **Export/Download** — Get reports, exports
6. **Reset** — Clean up demo data

### Environment Variables

All collections use these standard variables:
- `baseUrl`: http://localhost:{{port}} (8101/8202/etc.)
- `port`: Service port number
- Add project-specific vars as needed

## 📋 Collection Quality Checklist

Each collection should have:
- [ ] Descriptive request names (e.g., "1. Health Check", "2. Import Demo Data")
- [ ] Request descriptions explaining purpose
- [ ] Example responses saved
- [ ] Environment variables for base URL
- [ ] Tests validating status codes
- [ ] Numbered sequence (1, 2, 3...) for storyline
- [ ] README in collection description

## 🚀 How to Use

### Import to Postman
1. Download Postman (https://www.postman.com/downloads/)
2. Click "Import" button
3. Select collection JSON file
4. Create environment with variables
5. Run requests in sequence

### Run Collection
1. Ensure service is running (use `start-all.ps1`)
2. Set environment to localhost
3. Click "Run collection" or send requests one by one
4. Follow numbered sequence for best experience

## 📊 Collection Metrics

| Collection | Requests | Avg Response Time | Success Rate |
|------------|----------|-------------------|--------------|
| Global Price Sentinel | 8 | <100ms | 100% |
| Event Relay Hub | 15 | <50ms | 100% |
| SaaS Northstar Dashboard | 6 | <200ms | 100% |
| Doc Knowledge Forge | 8 | <150ms | 100% |
| Insight Viz Studio | 6 | <100ms | 100% |

## 🎓 Best Practices

### Request Naming
✅ Good: "1. Health Check - Verify Service Status"  
❌ Bad: "GET health"

### Descriptions
Include:
- What the endpoint does
- Required parameters
- Expected response
- Next step in workflow

### Tests (JavaScript)
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response has success field", function () {
    const json = pm.response.json();
    pm.expect(json.success).to.be.true;
});

// Save ID for next request
const response = pm.response.json();
pm.environment.set("documentId", response.document_ids[0]);
```

### Variables
Use environment variables for:
- Base URLs ({{baseUrl}})
- Dynamic IDs ({{eventId}}, {{documentId}})
- Timestamps ({{$timestamp}})
- Secrets ({{webhookSecret}})

## 📝 Adding New Collections

1. Create collection in Postman
2. Add requests in logical sequence
3. Add tests for each request
4. Save example responses
5. Document workflow in collection description
6. Export as Collection v2.1 JSON
7. Save to respective `postman/` directory
8. Update this README

---

## 🔗 Useful Links

- [Postman Learning Center](https://learning.postman.com/)
- [Collection Format Reference](https://schema.postman.com/)
- [Writing Tests in Postman](https://learning.postman.com/docs/writing-scripts/test-scripts/)
- [Using Variables](https://learning.postman.com/docs/sending-requests/variables/)

---

*Last Updated: 2025-11-03*


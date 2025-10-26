============================================
  QUICK START GUIDE
============================================

METHOD 1: Batch File (RECOMMENDED - No encoding issues)
---------------------------------------------------------

1. Stop all services:
   Double-click: STOP_ALL.bat

2. Start all projects:
   Double-click: START_ALL.bat

3. Wait 30 seconds, then visit:
   http://localhost:8101



METHOD 2: PowerShell Commands (Manual)
---------------------------------------------------------

1. Open PowerShell and run:

cd "E:\Program Files\cursorproject\作品集"
、
# Stop all
.\STOP_ALL.ps1

# Fix Project 2
cd event-relay-hub
if (Test-Path .env) { Remove-Item .env }
"DEBUG=False`nHOST=0.0.0.0`nPORT=8202`nDATABASE_URL=sqlite:///./event_hub.db`nRATE_LIMIT_PER_MINUTE=60`nRATE_LIMIT_ENABLED=True" | Out-File .env -Encoding ASCII
cd ..

# Start Project 1
cd global-price-sentinel
start powershell {.\start.ps1}
cd ..

# Start Project 2  
cd event-relay-hub
start powershell {.\start.ps1}
cd ..

# Start Project 3
cd saas-northstar-dashboard
start powershell {npm run dev}
cd ..


METHOD 3: Manual Step by Step
---------------------------------------------------------

Window 1 - Project 1:
  cd "E:\Program Files\cursorproject\作品集\global-price-sentinel"
  .\start.ps1

Window 2 - Project 2:
  cd "E:\Program Files\cursorproject\作品集\event-relay-hub"
  Remove-Item .env -ErrorAction SilentlyContinue
  "DEBUG=False`nHOST=0.0.0.0`nPORT=8202`nDATABASE_URL=sqlite:///./event_hub.db" | Out-File .env -Encoding ASCII
  .\start.ps1

Window 3 - Project 3:
  cd "E:\Program Files\cursorproject\作品集\saas-northstar-dashboard"
  npm run dev


TROUBLESHOOTING
---------------------------------------------------------

If Project 2 fails with PostgreSQL error:
  1. Delete event-relay-hub\.env file
  2. Run FIX_PROJECT2.ps1
  3. Try again

If ports are occupied:
  1. Run STOP_ALL.bat
  2. Wait 5 seconds
  3. Try START_ALL.bat again


ACCESS URLS AFTER STARTUP
---------------------------------------------------------

Main Portal:     http://localhost:8101
Project 1 API:   http://localhost:8101/api/docs
Project 1 Report: http://localhost:8101/reports/latest.html

Project 2 Home:  http://localhost:8202
Project 2 API:   http://localhost:8202/api/docs
Project 2 Events: http://localhost:8202/api/events

Project 3 Dashboard: http://localhost:8303


SUPPORT
---------------------------------------------------------

For detailed documentation, see:
- 运行指南.md
- 功能详解.md
- 项目完成总结.md


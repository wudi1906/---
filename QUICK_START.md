# Quick Start Guide — Launch All Projects in 60 Seconds

[English](#english) | [中文](#中文)

---

## English

### 🚀 Fastest Way to See All Projects

1. **Open PowerShell** in this directory
2. **Run the start script**:
   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\start-all.ps1
   ```
3. **Wait 30-60 seconds**
4. **Open browser**: http://localhost:8101
5. **See all 6 projects** in the portal with real-time health status

### ✅ Verify All Services

```powershell
.\TEST_ALL.bat
```

You should see:
```
[1/6] Testing Project 1 (Port 8101)... [OK]
[2/6] Testing Project 2 (Port 8202)... [OK]
[3/6] Testing Project 3 (Port 8303)... [OK]
[4/6] Testing Project 4 (Port 8404)... [OK]
[5/6] Testing Project 5 (Port 8505)... [OK]
[6/6] Testing Project 6 (Port 8606)... [OK]
```

### 🎯 Try Demo Data

Once at http://localhost:8101:
1. Click **"Import Demo"** for any project (P2/P3/P4/P6)
2. Wait for success message
3. Click **"Live Demo"** to see the project with sample data
4. Explore features, API docs, and functionality

### 🛑 Stop All Services

```powershell
.\stop-all.ps1
```

---

## 中文

### 🚀 最快速启动方式

1. **在此目录打开 PowerShell**
2. **运行启动脚本**：
   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\start-all.ps1
   ```
3. **等待 30-60 秒**
4. **打开浏览器**：http://localhost:8101
5. **查看全部 6 个项目**，带实时健康状态

### ✅ 验证所有服务

```powershell
.\TEST_ALL.bat
```

应该看到：
```
[1/6] Testing Project 1 (Port 8101)... [OK]
[2/6] Testing Project 2 (Port 8202)... [OK]
[3/6] Testing Project 3 (Port 8303)... [OK]
[4/6] Testing Project 4 (Port 8404)... [OK]
[5/6] Testing Project 5 (Port 8505)... [OK]
[6/6] Testing Project 6 (Port 8606)... [OK]
```

### 🎯 试用示例数据

访问 http://localhost:8101 后：
1. 点击任意项目的 **"Import Demo"** 按钮（P2/P3/P4/P6）
2. 等待成功提示
3. 点击 **"Live Demo"** 查看带示例数据的项目
4. 浏览功能、API 文档和各项特性

### 🛑 停止所有服务

```powershell
.\stop-all.ps1
```

---

## 🌐 Access URLs

After startup, you can access:

| Service | URL | Description |
|---------|-----|-------------|
| **Main Portal** | http://localhost:8101 | Entry point, shows all 6 projects |
| **Project 1** | http://localhost:8101 | Global Price Sentinel |
| **Project 2** | http://localhost:8202 | Event Relay Hub |
| **Project 3** | http://localhost:8303 | SaaS Northstar Dashboard |
| **Project 4** | http://localhost:8404 | Doc Knowledge Forge |
| **Project 5** | http://localhost:8505 | A11y Component Atlas (Storybook) |
| **Project 6** | http://localhost:8606 | Insight Viz Studio |

---

## 🔧 Troubleshooting

### PowerShell Execution Policy Error

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### Port Already in Use

```powershell
.\stop-all.ps1
# Wait 5 seconds
.\start-all.ps1
```

### Service Not Starting

Check individual project directories for detailed logs:
- Project 1: `global-price-sentinel/start.ps1`
- Project 2: `event-relay-hub/start.ps1`
- Project 3: `cd saas-northstar-dashboard && npm run dev`
- Project 4: `doc-knowledge-forge/start.bat`
- Project 5: `cd a11y-component-atlas && npm run storybook`
- Project 6: `insight-viz-studio/start.bat`

### Missing Dependencies

**Python projects** (P1/P2/P4/P6):
```powershell
cd <project-directory>
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Node.js projects** (P3/P5):
```powershell
cd <project-directory>
npm install
```

---

## 📚 More Information

- **Detailed guide**: [运行指南.md](./运行指南.md) (Chinese)
- **Feature overview**: [功能详解.md](./功能详解.md) (Chinese)
- **Fiverr packages**: [fiverr-listings/](./fiverr-listings/)
- **English READMEs**: Each project has `README.en.md`
- **Progress report**: [FIVERR_READY_REPORT.md](./FIVERR_READY_REPORT.md)

---

## ⚡ That's It!

You should now have all 6 projects running and accessible through the main portal.

**Happy exploring! 🎉**

---

*Last Updated: 2025-11-03*


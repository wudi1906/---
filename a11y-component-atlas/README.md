# A11y Component Atlas

[English Version](./README.en.md) | 中文版本

可访问性组件库 - 符合 WCAG 2.1 AA 标准的 React 组件集合。

---

## 1. 背景与痛点 · Background & Pain
- 团队需要符合 WCAG 2.1 AA 的组件，但从零实现键盘/ARIA/焦点管理成本高。
- 多语言/RTL/主题需求复杂，设计/开发/测试周期被拉长。
- 市场交付需要 Storybook 文档、自动化测试、可审计流程，难以快速上线。

## 2. 解决方案 · Solution & Value
- 提供 Button/Input/Modal/Tabs/Menu 等核心组件，内置无障碍支持与键盘导航。
- 亮暗主题、RTL、国际化就绪，可快速匹配欧美/东南亚/中东市场设计要求。
- Storybook 文档 + Vitest-axe 自动化测试，确保交付即上线，易于扩展新组件。

## 3. 交付清单 · Deliverables
- 🖥️ **Storybook Demo**：`http://localhost:8505`（含交互文档与示例代码）。
- 📦 **源代码**：React + TypeScript 组件、Tailwind 主题、Radix 基础样式。
- 📕 **文档**：使用指南、主题定制、可访问性清单、贡献规范。
- 🧪 **测试脚本**：Vitest + Testing Library + axe 检查、Chromatic 配置。
- 🛠️ **工具脚本**：`npm run storybook`、`npm test`、`npm run chromatic`、`npm run build-storybook`。

## 4. 实施流程与周期 · Process & Timeline
1. **需求澄清（Day 0）**：确认组件范围、品牌主题、语种/RTL 要求、交付渠道。
2. **设计映射（Day 1-2）**：对齐 UI/UX、可访问性要求，输出组件蓝图。
3. **开发验证（Day 3-6）**：实现组件、写 Storybook & 测试、执行 axe/Lighthouse 扫描。
4. **交付上线（Day 7+）**：交付 Storybook、npm 包或源码，支持 CI/CD 接入。

## 5. SLA 与质量保证 · SLA & Quality
- < 1 小时响应；按套餐提供 7~30 天远程支持、缺陷修复。
- 所有组件通过 WCAG 2.1 AA 检查：语义标签 + ARIA + 焦点环 + 对比度 ≥ 4.5:1。
- 提供结构化日志/测试报告、Lighthouse 报告、axe 扫描结果。
- 兼容现代浏览器与移动端，保证触控目标 ≥ 44px，动效 150-250ms。

## 6. KPI / 成功指标占位 · KPI & Outcomes
- 1 天集成核心组件至现有项目，UI/UX 修复成本下降 40%。
- axe/Lighthouse 评分 ≥ 95，客户可通过审计或企业合规验收。
- 组件复用率提升 3×，设计/开发协同效率显著提升。

## 7. 常见问题 · FAQ
**Q1：如何定制主题与品牌？**  
A：提供 Tailwind Token、CSS 变量、Figma 样板，可在 `tailwind.config.js` 快速配置品牌色。

**Q2：支持哪些框架集成？**  
A：默认 React，亦可输出 Web Component 或与 Next.js/Vite/CRA 集成，保留无头模式供自定义。

**Q3：如何保证测试覆盖？**  
A：所有组件附带单元/交互测试，提供 `npm test`、`npm run lighthouse`、`npm run chromatic`。

## 8. CTA · 下一步行动
- 🔵 [Upwork · 立即咨询](https://www.upwork.com/fl/yourname)
- 🟢 [Fiverr · 套餐下单](https://www.fiverr.com/yourname)
- 📧 [Email · 预约演示](mailto:you@example.com?subject=A11y%20Component%20Atlas%20Consultation)
- 🚀 [Storybook Demo · 立即体验](http://localhost:8505)

---

### 快速开始 · Quick Start

```powershell
chcp 65001
Set-Location "E:\Program Files\cursorproject\作品集\a11y-component-atlas"

npm install
npm run storybook
```

> 📌 项目采用 Storybook **8.6.x** + Vite 5。首次启动若出现 `npx storybook@latest upgrade` 提示，可按需执行迁移脚本；若暂不需要，可直接关闭提示继续使用。

### 主题定制 · Theming

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: '#2563EB',
        secondary: '#64748B'
      }
    }
  }
}
```

### 使用示例 · Usage Example

```tsx
import { Button, Input, Modal } from '@/components'

function App() {
  return (
    <div>
      <Button variant="primary" size="lg">Click Me</Button>
      <Input label="Email" type="email" required aria-describedby="email-help" />
      <Modal title="Confirm Action" onClose={() => {}}>
        <p>Are you sure?</p>
      </Modal>
    </div>
  )
}
```

---

## 9. 开发指南 · Dev Guide

| 步骤 | PowerShell 命令 | 说明 |
| --- | --- | --- |
| **环境准备** | `chcp 65001`<br>`Set-Location "E:\Program Files\cursorproject\作品集\a11y-component-atlas"` | 切换至 UTF-8 代码页，避免中文路径导致的 ENOENT；确保 Node ≥ 18。 |
| **依赖安装** | `npm install` | Storybook 8 升级会刷新锁文件；提交前注意 `package-lock.json` 变更。 |
| **代码质量** | `npm run lint` | 检查 TypeScript/React 语法及 A11y 规范。 |
| **单测 & axe** | `npm test` | Vitest + Testing Library + `vitest-axe`。Button/Input/Menu/Modal/Tabs 均包含 `await axe(container)` 检查；若有异步渲染，需先 `await screen.findBy...` 再运行 axe，避免误报。 |
| **Storybook 预览** | `npm run storybook` | 默认端口 `8505`。若端口被占用，可通过 `npm run storybook -- --port 8600` 临时调整。控制台的 “Vite CJS Node API deprecated” 为兼容提示，可忽略。 |
| **Storybook 打包** | `npm run build-storybook` | 生成静态站点用于部署或销售演示。 |

### 9.1 常见问题 · Troubleshooting

- **Storybook 提示执行 `npx storybook@latest upgrade`？** 这是 8.x 版本的自动迁移提醒，可按提示检查建议变更；若当前配置已兼容，可暂不执行。
- **PowerShell 报路径或编码错误？** 确认已切换 UTF-8；如仍受限，可创建临时驱动器：
  ```powershell
  New-PSDrive -Name atlas -PSProvider FileSystem -Root "E:\Program Files\cursorproject\作品集"
  Set-Location atlas:\a11y-component-atlas
  ```
- **`npm audit` 显示 4 个中等风险**：与 Storybook 传递依赖相关。可运行 `npm audit` 查看详情；若需自动修复，先评估 `npm audit fix --force` 对构建的影响。
- **axe 测试失败或提示异步元素缺失？** 检查测试中是否已经等待组件渲染。例如使用 `await screen.findByRole('button')` 确保 DOM ready 后再执行 `axe`。
- **Vite CJS Node API 警告**：目前仅为警告，不影响开发。若需消除可按照 [Vite 文档](https://vite.dev/guide/troubleshooting.html#vite-cjs-node-api-deprecated) 使用 ESM API（当前配置已使用 ESM，无需额外处理）。

---

## 10. 变更日志 · Recent Highlights

- **2025-11**：Storybook 升级至 8.6.14，统一 `@/` 别名，新增 Button/Input 的 Vitest-axe 覆盖，并更新 README 开发指南与常见问题。
- **2025-09**：补齐 Tabs/Menu/Modal 组件及 Storybook 文档，完善多语言与主题支持。


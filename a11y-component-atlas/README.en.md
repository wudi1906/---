# A11y Component Atlas | 可访问性组件库

## Pain | 客户痛点
- Teams need WCAG 2.1 AA compliant components but building keyboard/ARIA/focus handling from scratch is expensive.  /  团队需要符合 WCAG 2.1 AA 的组件，自行实现键盘、ARIA、焦点管理成本高。
- Multi-language/RTL/themes expand scope, leading to long design/dev/test cycles.  /  多语言、RTL 与主题适配增加设计开发测试周期。
- Delivery requires Storybook docs, automated tests, and auditability to satisfy enterprise buyers.  /  企业客户要求 Storybook 文档、自动化测试与可审计流程。

## Solution | 解决方案
- Ship Button/Input/Modal/Tabs/Menu foundations with built-in keyboard navigation and screen-reader labels.  /  提供 Button/Input/Modal/Tabs/Menu 核心组件，内建键盘导航与读屏标签。
- Theme tokens support light/dark/RTL/i18n, quickly aligning brand palettes across regions.  /  主题 Token 覆盖明暗、RTL、国际化，快速匹配不同市场的品牌风格。
- Storybook 8 + Vitest-axe pipeline ensures WCAG compliance, snapshot regression, and CI-friendly reports.  /  Storybook 8 + Vitest-axe 流程保证 WCAG 合规、快照回归与 CI 报告。

## Deliverables | 交付清单
- **Storybook Demo | 演示文档**: `http://localhost:8505`（含互动 Docs/Canvas 与多语言切换）。
- **Source & Theming | 源码与主题**: React + TypeScript 组件、Tailwind Token、CVA 配置、Radix 基础样式。 / React + TypeScript codebase with theme tokens and Radix primitives.
- **Tests & Tooling | 测试与工具**: Vitest + Testing Library + vitest-axe、Chromatic 配置、Lighthouse 脚本。 / Automated accessibility + visual testing assets.
- **Playbooks | 操作指南**: 可访问性检查清单、主题扩展手册、协作流程模板。 / Accessibility checklist, theming playbook, collaboration workflow.
- **Quick Start | 快速开始**:
  ```bash
  cd a11y-component-atlas
  npm install
  npm run storybook
  ```
  Visit `http://localhost:8505` after 20 seconds. / 约 20 秒后访问 `http://localhost:8505`。

## Timeline | 交付周期
1. **Discovery (Day 0)** — Confirm component scope, branding rules, language/RTL matrix.  /  明确组件范围、品牌规范与语言/RTL 需求。
2. **Design Mapping (Day 1-2)** — Align UI tokens, accessibility checklists, acceptance metrics.  /  对齐 UI Token、无障碍检查项与验收指标。
3. **Build & Validate (Day 3-6)** — 实现组件、补齐 Storybook 文档、执行 axe/Lighthouse 测试。 / Implement components, docs, automated scans.
4. **Launch & Handover (Day 7+)** — Deliver源码、npm/CI配置、培训与回滚预案。 / Ship code, CI recipes, training, rollback plan.

## SLA | 服务保障
- <1 hour initial response, 7/14/30 day remote warranty by package tier.  / 首次响应 <1 小时，提供 7/14/30 天远程质保。
- Components pass WCAG 2.1 AA: semantics, focus rings, contrast ≥4.5:1, skip links, screen reader hints.  / 组件通过 WCAG 2.1 AA，包含语义标签、焦点指示、对比度 ≥4.5:1、跳转链接与读屏提示。
- Automated tests with vitest-axe, Storybook docs, Chromatic snapshots for regression safety.  / vitest-axe、Storybook Docs、Chromatic 快照保障回归安全。
- Compatible with modern browsers/mobile, touch targets ≥44px, motion reduced for prefers-reduced-motion.  / 适配主流浏览器与移动端，触控目标 ≥44px，并尊重减少动画偏好。

## KPI | 成功指标
- Integrate core components into existing project within 1 day, reduce accessibility fixes by 40%.  / 1 天内接入项目，后续无障碍修复成本降低 40%。
- Axe/Lighthouse 得分 ≥95，交付即可通过合规审查。 / Axe/Lighthouse scores ≥95, ready for compliance reviews.
- Component reuse rate ×3, design & dev collaboration效率显著提升。 / Triple reuse rate, improve design-dev velocity.

## FAQ | 常见问题
- **主题与品牌如何自定义？ / How do we customize themes?**  \
  Tailwind Token + CSS 变量 + Figma 模板帮助快速换肤；配置集中在 `tailwind.config.ts`。 / Theme tokens & CSS vars + Figma kits expedite branding updates.
- **支持哪些框架集成？ / Which frameworks are supported?**  \
  默认 React，亦可导出 headless Web Components，适配 Next.js/Vite/CRA。 / React-first with optional headless wrappers for other setups.
- **测试覆盖如何保证？ / How do we ensure test coverage?**  \
  提供 `npm test`、`npm run lighthouse`、`npm run chromatic`，覆盖交互与视觉回归。 / Shipping unit, interaction, and visual regression scripts.

## CTA | 行动指引
- 📧 [Email – Book a Demo](mailto:you@example.com?subject=A11y%20Component%20Atlas%20Consultation) / 邮件预约演示
- 🗂 [Portal Overview](http://localhost:8101) / 门户导航与实时状态
- 📑 [Test Playbook](../PORTFOLIO_TEST_GUIDE.zh.md) / 验证剧本（中英对照）
- 🚀 [Storybook Demo](http://localhost:8505) / 本地体验入口

**Last Updated | 最近更新**：2025-11-03


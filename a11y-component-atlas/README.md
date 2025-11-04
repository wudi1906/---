# A11y Component Atlas | 可访问性组件库

> 当前文档已双语呈现，便于跨境团队共同评估。

## Pain | 客户痛点
- Teams need WCAG 2.1 AA compliant components but building keyboard/ARIA/focus handling from scratch is expensive.  /  团队需要符合 WCAG 2.1 AA 的组件，自行实现键盘、ARIA、焦点管理成本高。
- Multi-language/RTL/themes add complexity and stretch design–development cycles.  /  多语言、RTL 与主题适配增加设计与开发测试周期。
- Enterprise buyers expect Storybook docs, automated tests, audit-friendly delivery.  /  企业级客户要求 Storybook 文档、自动化测试与可审计交付。

## Solution | 解决方案
- Ship Button/Input/Modal/Tabs/Menu foundations with built-in keyboard navigation and screen-reader labels.  /  提供 Button/Input/Modal/Tabs/Menu 核心组件，内建键盘导航与读屏标签。
- Theme tokens cover light/dark/RTL/i18n for rapid branding across regions.  /  主题 Token 覆盖明暗、RTL、国际化需求，快速适配不同市场品牌。
- Storybook 8 + Vitest-axe pipeline guarantees WCAG compliance, regression safety, and CI-ready reports.  /  通过 Storybook 8 + Vitest-axe 流程确保 WCAG 合规、回归安全与 CI 对接。

## Deliverables | 交付清单
- **Storybook Demo | 演示文档**: `http://localhost:8505`，包含 Docs/Canvas、语言切换与可访问性示例。
- **Source & Theming | 源码与主题**: React + TypeScript 组件、Tailwind Token、CVA 配置、Radix UI 基础样式。 / Complete codebase with theming tokens and Radix primitives.
- **Tests & Tooling | 测试与工具**: Vitest + Testing Library + vitest-axe、Chromatic 配置、Lighthouse 脚本。 / Automated accessibility & visual tests ready for CI。
- **Playbooks | 操作手册**: 可访问性检查清单、主题扩展指南、协作流程模板。 / Accessibility checklist, theming playbook, collaboration templates。
- **Quick Start | 快速开始**:
  ```bash
  cd a11y-component-atlas
  npm install
  npm run storybook
  ```
  Visit `http://localhost:8505` after ~20 seconds. / 约 20 秒后访问 `http://localhost:8505`。

## Timeline | 交付周期
1. **Discovery (Day 0)** — Confirm component scope, branding tokens, language/RTL matrix.  /  明确组件范围、品牌 Token 与语言/RTL 需求。
2. **Design Mapping (Day 1-2)** — Align UI tokens, accessibility checklists, acceptance metrics.  /  对齐 UI Token、无障碍检查与验收指标。
3. **Build & Validate (Day 3-6)** — Implement components, Storybook docs, axe/Lighthouse 扫描。 / Build components, docs, and run automated scans。
4. **Launch & Handover (Day 7+)** — Deliver 源码、npm/CI 配置、培训与回滚预案。 / Ship code, CI recipes, training, rollback plan。

## SLA | 服务保障
- <1 hour initial response, 7/14/30 day remote warranty by package tier.  / 首次响应 <1 小时，提供 7/14/30 天远程质保。
- Components pass WCAG 2.1 AA (semantics, focus ring, contrast ≥4.5:1, skip links, screenreader hints).  / 组件通过 WCAG 2.1 AA，含语义标签、焦点指示、对比度 ≥4.5:1、跳转链接与读屏提示。
- Automated vitest-axe suites + Chromatic snapshots + Storybook Docs for audit readiness.  / vitest-axe 套件、Chromatic 快照、Storybook Docs，满足审计要求。
- Modern browser/mobile support with ≥44px touch targets, reduced motion preferences honored.  / 适配现代浏览器与移动端，触控目标 ≥44px，尊重减少动画偏好。

## KPI | 成功指标
- Integrate core components in 1 day, reduce accessibility fixes by 40%.  / 1 天内接入项目，无障碍返修成本降低 40%。
- Axe/Lighthouse scores ≥95, ready for enterprise compliance reviews.  / Axe/Lighthouse 得分 ≥95，可通过企业合规审查。
- Component reuse rate ×3, design/development collaboration速度显著提升。 / Reuse ×3, boost design-dev velocity。

## FAQ | 常见问题
- **How to customize themes? / 如何自定义主题？**  \
  Tailwind Token + CSS 变量 + Figma 模板；主要配置集中在 `tailwind.config.ts`。 / Theme tokens & CSS vars streamline branding updates。
- **Which frameworks are supported? / 支持哪些框架？**  \
  默认 React，可输出 headless Web Components，兼容 Next.js/Vite/CRA。 / React-first with optional headless wrappers。
- **How is test coverage ensured? / 如何保证测试覆盖？**  \
  提供 `npm test`、`npm run lighthouse`、`npm run chromatic`，覆盖交互与视觉回归。 / Shipping unit, interaction, and visual regression scripts。

## CTA | 行动指引
- 📧 [Email – Book a Demo](mailto:you@example.com?subject=A11y%20Component%20Atlas%20Consultation) / 邮件预约演示
- 🗂 [Portal Overview](http://localhost:8101) / 门户导航与实时状态
- 📑 [Test Playbook](../PORTFOLIO_TEST_GUIDE.zh.md) / 验证剧本（中英对照）
- 🚀 [Storybook Demo](http://localhost:8505) / 本地体验入口

**Last Updated | 最近更新**：2025-11-03


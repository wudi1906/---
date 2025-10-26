# A11y Component Atlas

可访问性组件库 - 符合 WCAG 2.1 AA 标准的 React 组件集合。

## 功能特性

- ♿ **完全可访问**: 符合 WCAG 2.1 AA 标准
- ⌨️ **键盘导航**: 完整的键盘操作支持
- 🎨 **主题系统**: 亮/暗主题，支持自定义
- 📱 **响应式**: 移动优先设计
- 📖 **Storybook**: 交互式文档
- ✅ **单元测试**: 高覆盖率测试
- 🎭 **视觉测试**: Chromatic 快照测试

## 快速开始

```bash
npm install
npm run storybook
```

访问: http://localhost:8505

## 组件列表

### 表单组件
- **Button**: 按钮（主要/次要/危险）
- **Input**: 输入框（文本/邮箱/密码）
- **Select**: 下拉选择器
- **Checkbox**: 复选框
- **Radio**: 单选按钮
- **Switch**: 开关切换

### 反馈组件
- **Toast**: 提示通知
- **Modal**: 对话框
- **Alert**: 警告信息
- **Progress**: 进度条

### 数据展示
- **Table**: 数据表格
- **Card**: 卡片容器
- **Tabs**: 标签页
- **Accordion**: 手风琴

## 技术栈

- **React 18** + TypeScript
- **Radix UI** (无头组件)
- **Tailwind CSS 3**
- **Storybook 8**
- **Vitest** + React Testing Library

## 可访问性检查清单

✅ 语义化 HTML  
✅ ARIA 属性完整  
✅ 键盘可操作  
✅ 焦点可见（2px outline）  
✅ 对比度 ≥ 4.5:1  
✅ 触控目标 ≥ 44px  
✅ 屏幕阅读器友好  
✅ 无闪烁动画  

## 使用示例

```tsx
import { Button, Input, Modal } from '@/components'

function App() {
  return (
    <div>
      <Button variant="primary" size="lg">
        Click Me
      </Button>
      
      <Input 
        label="Email"
        type="email"
        required
        aria-describedby="email-help"
      />
      
      <Modal 
        title="Confirm Action"
        onClose={() => {}}
      >
        <p>Are you sure?</p>
      </Modal>
    </div>
  )
}
```

## 测试

```bash
# 单元测试
npm test

# Lighthouse 可访问性测试
npm run lighthouse

# 视觉回归测试
npm run chromatic
```

## 部署 Storybook

```bash
npm run build-storybook
# 部署 storybook-static/ 到任意静态托管
```

## 主题定制

编辑 `tailwind.config.js`：

```js
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

## 扩展方向

- 更多组件（DataGrid, DatePicker）
- 多语言支持
- RTL 布局支持
- 动画库集成
- Figma 设计资源


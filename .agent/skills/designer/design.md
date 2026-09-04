# design.md — FPT CMS Hub Design System

> Mục đích: dùng file này như **design source of truth** cho Antigravity khi áp dụng / refactor / mở rộng file HTML của dự án FPT CMS Hub. Tài liệu ưu tiên khả năng **đồng bộ UI**, **scale theo quy mô dự án**, dễ thêm module mới và hạn chế phát sinh style rời rạc.

---

## 1. Tóm tắt giao diện gốc

File HTML hiện tại là một web app CMS quản trị nội dung theo phong cách **Untitled UI / SaaS Admin Dashboard**. Tổng thể dùng nền sáng, card trắng, viền xám mảnh, khoảng cách thoáng, bo góc mềm, typography Inter, hệ token CSS variables và có hỗ trợ dark mode.

Các vùng chính:

- **Sidebar trái**: logo FPT CMS, search nội bộ, navigation theo nhóm, trạng thái active, badge số lượng, tag “Chưa có”, user footer.
- **Topbar**: breadcrumb, search toàn cục, help, notification, toggle dark/light, avatar.
- **Main content**: page header, metric cards, toolbar search/filter, data table, pagination, form sections, modal, drawer, toast, audit timeline.
- **Module quản trị**: Dashboard, Pages, Sections, Blocks, Landing Page, Banner, Popup, News, FAQ, Menu, Display Settings, Permissions.

Mục tiêu khi mở rộng: mọi màn hình mới phải giống cùng một sản phẩm, không tạo UI riêng lẻ theo từng page.

---

## 2. Nguyên tắc thiết kế cốt lõi

### 2.1 Tone & visual direction

- **Clean enterprise SaaS**: rõ ràng, ít trang trí, ưu tiên khả năng quản trị dữ liệu.
- **FPT brand accent**: dùng cam FPT làm màu hành động chính, không lạm dụng xanh/tím nếu không thuộc semantic state.
- **Density vừa phải**: bảng dữ liệu cần gọn nhưng vẫn đủ khoảng thở.
- **Hierarchy rõ**: tiêu đề đậm, mô tả nhẹ, metadata xám, CTA nổi bật.
- **Không hard-code style mới**: luôn dùng token `var(--...)` để dễ thay theme/scale.

### 2.2 Quy tắc mở rộng

Khi Antigravity thêm module hoặc component mới:

1. Reuse token hiện có trước khi tạo token mới.
2. Reuse component pattern hiện có: `PageHeader`, `Card`, `Toolbar`, `Table`, `Drawer`, `Modal`, `Toast`.
3. Không dùng shadow mạnh hoặc gradient trang trí trong khu vực admin, trừ brand mark / banner preview.
4. Không tự đổi font; toàn bộ app dùng Inter/system sans.
5. Không tạo nhiều màu primary khác nhau; primary mặc định là `--brand-600`.
6. Dữ liệu dạng list phải ưu tiên table hoặc card grid có cấu trúc nhất quán.
7. Form dài phải chia section theo meta trái + input phải, giống pattern hiện tại.

---

## 3. Design Tokens

### 3.1 Color tokens

#### Base

```css
--white: #ffffff;
--black: #000000;
--transparent: transparent;
```

#### Gray scale

Dùng cho nền, text, border, icon, disabled, table header.

```css
--gray-25:  #fcfcfd;
--gray-50:  #f9fafb;
--gray-100: #f2f4f7;
--gray-200: #e4e7ec;
--gray-300: #d0d5dd;
--gray-400: #98a2b3;
--gray-500: #667085;
--gray-600: #475467;
--gray-700: #344054;
--gray-800: #1d2939;
--gray-900: #101828;
--gray-950: #0c111d;
```

#### Brand / FPT orange

```css
--brand-25:  #fff9f5;
--brand-50:  #fff1e7;
--brand-100: #ffd4b3;
--brand-200: #ffbf8e;
--brand-300: #ffa15b;
--brand-400: #ff8f3b;
--brand-500: #ff730a;
--brand-600: #e86909; /* primary */
--brand-700: #b55207;
--brand-800: #8c3f06;
--brand-900: #6b3004;
--brand-950: #4a2002;
```

#### Semantic colors

Use only for system state, not decoration.

```css
/* Success */
--success-50: #ecfdf3;
--success-600: #039855;
--success-700: #027a48;

/* Warning */
--warning-50: #fffaeb;
--warning-600: #dc6803;
--warning-700: #b54708;

/* Error */
--error-50: #fef3f2;
--error-600: #d92d20;
--error-700: #b42318;
```

### 3.2 Semantic token mapping

Luôn viết UI bằng semantic token khi có thể:

```css
--text-primary: var(--gray-900);
--text-secondary: var(--gray-700);
--text-tertiary: var(--gray-600);
--text-quaternary: var(--gray-500);
--text-placeholder: var(--gray-400);
--text-on-brand: var(--white);
--text-brand-primary: var(--brand-700);
--text-brand-secondary: var(--brand-600);

--bg-primary: var(--white);
--bg-secondary: var(--gray-50);
--bg-tertiary: var(--gray-100);
--bg-active: var(--gray-50);
--bg-overlay: rgba(12, 17, 29, 0.7);
--bg-brand-primary: var(--brand-600);
--bg-brand-primary-hover: var(--brand-700);

--border-primary: var(--gray-300);
--border-secondary: var(--gray-200);
--border-brand: var(--brand-600);

--fg-primary: var(--gray-900);
--fg-secondary: var(--gray-700);
--fg-tertiary: var(--gray-500);
--fg-brand-primary: var(--brand-600);
```

---

## 4. Typography system

### 4.1 Font

```css
--font-sans: "Inter", system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
--font-mono: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
```

### 4.2 Type scale

| Use case | Size | Line height | Weight | Letter spacing |
|---|---:|---:|---:|---:|
| Page title | 30px | 38px | 600 | -0.02em |
| Card title | 18px | 28px | 600 | -0.01em |
| Body | 16px | 24px | 400 | 0 |
| Table/body small | 14px | 20px | 400/500 | 0 |
| Metadata | 13px | 18px | 400/500 | 0 |
| Label / badge | 12px | 18px | 500/600 | optional uppercase 0.06em |

### 4.3 Typography rules

- Page heading: `font: 600 30px/38px var(--font-sans)`.
- Card heading: `font: 600 18px/28px var(--font-sans)`.
- Body/sub text: `14px/20px` or `16px/24px` depending density.
- Table header: `12px/18px`, medium, uppercase only if needed.
- Avoid using font weight above 700 except brand mark.

---

## 5. Spacing, radius, shadow

### 5.1 Spacing scale

Base scale is 4px. Do not create arbitrary spacing values unless required by layout.

```css
--space-1: 4px;
--space-2: 8px;
--space-3: 12px;
--space-4: 16px;
--space-5: 20px;
--space-6: 24px;
--space-8: 32px;
--space-10: 40px;
--space-12: 48px;
--space-16: 64px;
--space-20: 80px;
--space-24: 96px;
--space-32: 128px;
```

### 5.2 Radius scale

```css
--radius-sm: 6px;
--radius-md: 8px;   /* button/input */
--radius-lg: 10px;
--radius-xl: 12px;  /* cards */
--radius-2xl: 16px;
--radius-4xl: 24px;
--radius-full: 9999px;
```

### 5.3 Shadows

Use subtle elevation only:

```css
--shadow-xs: 0 1px 2px 0 rgba(16,24,40,0.05);
--shadow-sm: 0 1px 2px 0 rgba(16,24,40,0.06), 0 1px 3px 0 rgba(16,24,40,0.10);
--shadow-md: 0 2px 4px -2px rgba(16,24,40,0.06), 0 4px 8px -2px rgba(16,24,40,0.10);
--shadow-lg: 0 4px 6px -2px rgba(16,24,40,0.03), 0 12px 16px -4px rgba(16,24,40,0.08);
--shadow-xl: 0 8px 8px -4px rgba(16,24,40,0.03), 0 20px 24px -4px rgba(16,24,40,0.08);
--shadow-2xl: 0 24px 48px -12px rgba(16,24,40,0.18);
```

### 5.4 Focus rings

```css
--ring-focus: 0 0 0 4px rgba(232,105,9,0.24);
--ring-focus-gray: 0 0 0 4px rgba(152,162,179,0.14);
--ring-focus-error: 0 0 0 4px rgba(240,68,56,0.24);
```

---

## 6. App layout rules

### 6.1 Root app shell

```css
.app {
  display: grid;
  grid-template-columns: 272px 1fr;
  min-height: 100vh;
}
.app.sidebar-collapsed {
  grid-template-columns: 68px 1fr;
}
.main {
  padding: 32px;
  max-width: 1600px;
  width: 100%;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 24px;
}
```

Responsive rule:

```css
@media (max-width: 1024px) {
  .app { grid-template-columns: 1fr; }
  .sidebar { display: none; }
}
```

### 6.2 Sidebar

- Width expanded: `272px`.
- Width collapsed: `68px`.
- Background: `#fff` / dark `#0f1422`.
- Border right: `1px solid var(--gray-200)`.
- Padding expanded: `24px 16px`.
- Sticky full height: `position: sticky; top: 0; height: 100vh`.
- Navigation item: height from padding `8px 12px`, radius `6px`, gap `12px`.
- Active state: `background: var(--brand-50); color: var(--brand-700)`.

### 6.3 Topbar

- Height is content-driven; padding `14px 32px`.
- Sticky top: `position: sticky; top: 0; z-index: 5`.
- Contains breadcrumb left, search middle/right, actions right.
- Top search width: `320px`, max `40vw`.

### 6.4 Main page rhythm

Recommended order for every module:

```html
<main class="main">
  <section class="page-header">...</section>
  <section class="metrics">...</section> <!-- optional -->
  <section class="card">
    <div class="card-head">...</div>
    <div class="toolbar">...</div> <!-- optional -->
    <div class="table-wrap">...</div> hoặc form/body
    <div class="table-foot">...</div> <!-- optional -->
  </section>
</main>
```

---

## 7. Component specifications

### 7.1 Button

Variants:

- `primary`: main CTA, save, create, confirm.
- `secondary`: default neutral action.
- `tertiary`: low emphasis action.
- `destructive`: delete/remove.
- `link`: inline navigation.

Rules:

```css
.btn-primary {
  background: var(--brand-600);
  color: #fff;
  box-shadow: var(--shadow-xs), var(--ring-button-primary);
}
.btn-primary:hover { background: var(--brand-700); }
.btn-secondary {
  background: #fff;
  color: var(--gray-700);
  box-shadow: var(--shadow-xs), var(--ring-button-secondary);
}
```

Button sizing:

| Size | Height | Padding | Font |
|---|---:|---:|---|
| sm | 32px | 8–12px | 14/20 medium |
| md | 40px | 10–16px | 14/20 semibold |
| lg | 44–48px | 12–20px | 16/24 semibold |

### 7.2 Input / Search

- Height: `40px`.
- Border: `1px solid var(--gray-300)`.
- Radius: `8px`.
- Focus: `border-color: var(--brand-300)` + `--ring-focus`.
- Placeholder: `var(--gray-500)`.
- Search input pattern uses `.input-group` with icon left and optional keyboard hint right.

### 7.3 Badge

Use badges for status and short metadata only.

| Status | Badge kind | Usage |
|---|---|---|
| Published / Active | success | Đang hoạt động, đã publish |
| Draft | gray | Nháp |
| Hidden / Pending | warning | Tạm ẩn, chờ xử lý |
| Error / Failed | error | Lỗi, xóa, nguy hiểm |
| Featured / Brand | brand | Ưu tiên, nổi bật |

### 7.4 Card

```css
.card {
  background: #fff;
  border: 1px solid var(--gray-200);
  border-radius: 12px;
  box-shadow: var(--shadow-xs);
  overflow: hidden;
}
.card-head {
  padding: 20px 24px;
  border-bottom: 1px solid var(--gray-200);
}
```

Rules:

- Card không dùng gradient nền trong dashboard admin.
- Card head luôn có title và optional description/action.
- Nội dung card phải dùng padding đồng bộ `20px/24px`.

### 7.5 Metric card

```css
.metrics {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}
.metric {
  background: #fff;
  border: 1px solid var(--gray-200);
  border-radius: 12px;
  padding: 20px;
  box-shadow: var(--shadow-xs);
}
```

Responsive:

```css
@media (max-width: 1100px) {
  .metrics { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 640px) {
  .metrics { grid-template-columns: 1fr; }
}
```

### 7.6 Table

- Table min-width: `980px` for dense admin data.
- Header background: `var(--gray-50)`.
- Header font: `500 12px/18px`.
- Cell padding: `16px 24px` multiplied by density if needed.
- Row hover: `var(--gray-25)`.
- Actions right-aligned using icon buttons.

Table should include:

1. Checkbox column when multi-select exists.
2. Primary cell with title + optional subtext.
3. Badge/status column.
4. Updated/date metadata.
5. Row actions at end.
6. Pagination in `.table-foot`.

### 7.7 Toolbar

```css
.toolbar {
  padding: 16px 24px;
  display: flex;
  gap: 12px;
  align-items: center;
  border-bottom: 1px solid var(--gray-200);
  flex-wrap: wrap;
}
.toolbar > .input-group {
  flex: 1;
  min-width: 240px;
}
```

Toolbar order:

1. Search field.
2. Filter chips/dropdown.
3. Sort/export secondary action.
4. Primary create action should usually stay in page header, not toolbar.

### 7.8 Form sections

Use this for create/edit/detail pages:

```css
.section {
  padding: 24px;
  border-bottom: 1px solid var(--gray-200);
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 32px;
}
.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px 24px;
}
.form-row.full { grid-column: 1 / -1; }
```

Rules:

- Left meta: section title + short explanation.
- Right content: form grid.
- For long text/SEO/media: full-width row.
- Footer sticky optional for long form; default `.form-foot`.

### 7.9 Modal

Use modal for confirmation or short focused tasks only.

- Max width: `400px` for confirm.
- Use icon type: warning/error/brand.
- Footer actions right aligned.
- Destructive action must use `btn-destructive`.

### 7.10 Drawer

Use drawer for quick detail view or side edit.

- Width: `480px`.
- Position right, full height.
- Header: title + sub.
- Body: detail rows / compact forms.
- Footer: secondary + primary actions.

### 7.11 Toast

Use toast for result feedback after save/delete/create.

- Position: bottom-right.
- Width: min `320px`, max `400px`.
- Contains featured icon + title + body + close.

### 7.12 Icons

- Style: Untitled UI stroke icon.
- Default size: `20px`.
- Stroke: `2px`, rounded cap/join.
- Use `var(--gray-500)` for inactive icons and `var(--brand-600)` for active.
- Avoid mixing filled icons into the admin UI.

---

## 8. Module patterns

### 8.1 Dashboard

Use dashboard for overview only:

- Page header with title and short description.
- 4 metric cards.
- Quick actions card/list.
- Recent activity timeline.
- Attention rows for warnings / pending content.

### 8.2 List module pattern

Applies to Pages, Sections, Blocks, Banner, Popup, News, FAQ, Menu, Permissions.

Recommended structure:

```html
<PageHeader title="..." sub="..." actions=[CreateButton] />
<Metrics optional />
<Card>
  <CardHead title="Danh sách ..." description="..." />
  <Toolbar search filters />
  <Table rows />
  <TableFoot pagination />
</Card>
```

### 8.3 Editor module pattern

Applies to Pages form, Landing editor, News editor, Popup form, Banner form.

Recommended flow:

1. `PageHeader` with back/cancel action.
2. `Card` wrapper.
3. Optional tabs for large forms: General, SEO, Media, Sections, Audit.
4. Section-based form layout.
5. Footer with `Hủy`, `Lưu nháp`, `Xuất bản`.

### 8.4 Detail module pattern

Use detail drawer when user needs quick view without losing list context:

- Drawer title = entity name.
- Sub = status/date/path.
- Detail rows use label/value grid.
- Include audit activity if relevant.
- Include primary edit action in drawer footer.

---

## 9. Navigation information architecture

Keep sidebar structure consistent:

```txt
Dashboards

Quản lý sản phẩm
- SKUs

Quản lý nội dung (CMS)
- Cấu trúc trang
  - Quản lý Menu
  - Quản lý Trang (Pages)
  - Quản lý Sections
  - Quản lý Blocks
  - Landing Page (LDP)
- Media & quảng bá
  - Quản lý Banner
  - Quản lý Popup
- Bài viết & nội dung
  - Quản lý Tin tức
  - Quản lý FAQ
- Cài đặt hiển thị

Quản lý hệ thống
- Phân quyền
  - Vai trò
  - Người dùng
  - Phân quyền màn hình
```

Rules:

- Module mới phải được đặt vào đúng nhóm.
- Không tạo quá 2 cấp con trong sidebar; nếu cần sâu hơn, dùng tabs trong page.
- Count badge chỉ dùng cho số lượng item thật.
- “Chưa có” chỉ dùng cho module placeholder chưa hoàn thiện.

---

## 10. Dark mode rules

Dark mode đã có trong file nhưng cần tuân thủ các nguyên tắc sau khi mở rộng:

- Surface chính: `#0f1422`.
- Page background: `#0a0e1a`.
- Elevated background: `#131a2c`.
- Input background: `#0b1020`.
- Border: `#1f2740`.
- Text chính: `#ffffff` hoặc `var(--gray-700)` sau khi gray scale được override.
- Text phụ không được dùng `#475467` trực tiếp trên nền tối; dùng `var(--gray-400)` hoặc sáng hơn.
- Active brand trong dark: `brand-950` background + `brand-200/300` text/icon.

Implementation guardrail:

```css
body.dark .new-card,
body.dark .new-panel {
  background: #0f1422;
  border-color: #1f2740;
}
body.dark .new-muted-text {
  color: var(--gray-400);
}
body.dark .new-active-state {
  background: var(--brand-950);
  color: var(--brand-200);
}
```

---

## 11. Responsive behavior

### Breakpoints

```css
/* Desktop default */
/* 1100px: reduce metrics grid */
/* 1024px: hide sidebar */
/* 980px: form section becomes single column */
/* 760px: form grid becomes single column */
/* 640px: card/table actions stack */
```

### Rules

- Data tables may scroll horizontally via `.table-wrap`.
- Main padding on tablet/mobile should reduce from `32px` to `20px/16px`.
- Metrics: `4 columns → 2 columns → 1 column`.
- Forms: meta and fields stack vertically.
- Sidebar can be hidden on tablet, but do not duplicate full nav inside topbar unless required.

Recommended addition:

```css
@media (max-width: 640px) {
  .main { padding: 20px 16px; gap: 20px; }
  .page-header { flex-direction: column; gap: 16px; }
  .page-header .actions { width: 100%; }
  .page-header .actions .btn { flex: 1; justify-content: center; }
  .top-search { display: none; }
  .table-foot { flex-direction: column; align-items: stretch; }
}
```

---

## 12. Accessibility requirements

- All icon-only buttons must have `title` and ideally `aria-label`.
- Inputs must have visible label or `aria-label`.
- Focus state must be visible using `--ring-focus`.
- Modal/drawer must trap focus if converted to production React.
- Toast should not block main content.
- Table actions should be keyboard reachable.
- Status must not rely on color only; badge text is required.
- Dark mode text contrast must meet WCAG AA.

---

## 13. Antigravity implementation instructions

Paste this section as the main instruction when asking Antigravity to modify the HTML.

```txt
You are editing an existing FPT CMS Hub HTML app. Preserve the current Untitled UI / SaaS admin dashboard style. Use the design tokens from :root and do not create arbitrary colors, spacing, radius, shadows, or font styles.

When adding or refactoring screens:
1. Keep the app shell: sidebar 272px, collapsed 68px, topbar sticky, main max-width 1600px with 32px padding.
2. Use semantic CSS variables: --text-primary, --text-secondary, --bg-primary, --border-secondary, --brand-600.
3. Reuse existing components/patterns: PageHeader, card, card-head, toolbar, table-wrap, table, table-foot, form-grid, section, modal, drawer, toast, badge, chip, icon-btn.
4. New list screens must follow: PageHeader → optional Metrics → Card → CardHead → Toolbar → Table → Pagination.
5. New edit screens must follow: PageHeader → Card → Tabs optional → Section-based form → Form footer.
6. Support dark mode by adding body.dark overrides for any new hard-coded surfaces.
7. Keep icons stroke-based, 20px default, gray inactive, brand active.
8. Use Vietnamese admin copy consistent with existing CMS modules.
9. Avoid visual redesign. Improve consistency, scalability, accessibility, and code organization only.
10. Before finalizing, check light mode, dark mode, responsive widths, and repeated component consistency.
```

---

## 14. Recommended improvements to apply

### 14.1 Token cleanup

Current file already has a good token foundation. Improve by centralizing any newly added raw values into tokens.

Avoid:

```css
color: #475467;
padding: 17px 23px;
border-radius: 11px;
```

Prefer:

```css
color: var(--text-tertiary);
padding: var(--space-4) var(--space-6);
border-radius: var(--radius-xl);
```

### 14.2 Reduce hard-coded dark mode patches

Current dark mode contains many selector-specific fixes. Future changes should avoid creating more one-off overrides. Prefer semantic variables on components first, then only add dark overrides for truly custom surfaces.

### 14.3 Add mobile polish

The original app is desktop-admin first. Add mobile/tablet refinements:

- Reduce `.main` padding below 640px.
- Stack `.page-header` actions.
- Hide `.top-search` or convert to icon search.
- Ensure `.metrics` has 1-column mobile state.
- Keep tables horizontally scrollable.

### 14.4 Make density configurable

The table uses density-like behavior. Standardize with:

```css
:root { --density: 1; }
body.compact { --density: .75; }
body.comfortable { --density: 1.15; }
```

Then table rows and form spacing can scale without rewriting every component.

### 14.5 Separate module patterns from data

For production scale:

- Keep UI primitives in `components/atoms`.
- Keep layout shell in `components/layout`.
- Keep modules in `modules/<module-name>`.
- Keep mock data/API mapping separate from view components.
- Keep design tokens in `styles/tokens.css`.

Suggested structure:

```txt
/src
  /styles
    tokens.css
    base.css
    components.css
    dark.css
  /components
    /atoms
      Button.jsx
      Badge.jsx
      Input.jsx
      IconButton.jsx
    /layout
      Sidebar.jsx
      Topbar.jsx
      PageHeader.jsx
    /data-display
      Table.jsx
      Pagination.jsx
      MetricCard.jsx
    /feedback
      Modal.jsx
      Drawer.jsx
      Toast.jsx
  /modules
    dashboard/
    pages/
    sections/
    blocks/
    landing/
    banner/
    popup/
    news/
    faq/
    permissions/
```

---

## 15. Quality checklist before accepting generated HTML

### Visual consistency

- [ ] Primary color is still FPT orange `--brand-600`.
- [ ] No random new blue/purple primary color is introduced.
- [ ] Card radius remains `12px`.
- [ ] Button/input radius remains `8px`.
- [ ] Table header and row spacing match existing screens.
- [ ] All new icons match 20px stroke style.
- [ ] Page header style is consistent across modules.

### Scalability

- [ ] New components use CSS variables.
- [ ] No repeated inline style blocks for reusable patterns.
- [ ] New module follows list/editor/detail pattern.
- [ ] Sidebar navigation remains max 2 levels.
- [ ] Data/state is separated from presentational UI where possible.

### Accessibility

- [ ] Icon-only buttons have accessible labels.
- [ ] Inputs have labels/placeholders that make sense.
- [ ] Status badges include readable text.
- [ ] Keyboard focus is visible.
- [ ] Dark mode contrast is readable.

### Responsive

- [ ] 1440px desktop looks like original design.
- [ ] 1024px does not break shell layout.
- [ ] 768px forms stack correctly.
- [ ] 375px mobile still readable with horizontal table scroll.

---

## 16. Final design direction

Use the current file as a strong foundation, but treat it as a **scalable CMS product system**, not a one-off HTML mockup. The key improvements are:

1. Keep tokens as the only source of visual truth.
2. Standardize every module into list/editor/detail patterns.
3. Reduce one-off styles and hard-coded values.
4. Improve responsive behavior below tablet width.
5. Maintain dark mode contrast through semantic tokens.
6. Keep admin UI restrained, clear, and production-ready.

When in doubt, choose consistency over novelty.

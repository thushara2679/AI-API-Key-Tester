# UI/UX Patterns Document

## 📋 Document Overview

**Project Name:** Advanced AI Agent System for Enterprise Automation
**Version:** 1.0
**Document Type:** UI/UX Design Patterns & Best Practices
**Focus:** Component patterns, interactions, accessibility

---

## 🎨 Design System Components

### Button Patterns

```tsx
// Size variants
<Button size="sm" variant="primary">Small</Button>
<Button size="md" variant="primary">Medium</Button>
<Button size="lg" variant="primary">Large</Button>

// State variants
<Button variant="primary" disabled>Disabled</Button>
<Button variant="primary" isLoading>Loading...</Button>
<Button variant="primary" icon={<IconPlus />}>Create</Button>

// Color variants
<Button variant="primary">Primary</Button>
<Button variant="secondary">Secondary</Button>
<Button variant="danger">Delete</Button>
<Button variant="success">Save</Button>
```

### Input Components

```tsx
// Text input
<TextField
  label="Feature Name"
  placeholder="Enter name"
  value={name}
  onChange={setName}
  error={error}
  helpText="2-255 characters"
/>

// Textarea
<TextArea
  label="Description"
  placeholder="Describe the feature"
  rows={5}
  maxLength={2000}
  showCharCount
/>

// Select
<Select
  label="Priority"
  options={[
    { value: 'low', label: 'Low' },
    { value: 'high', label: 'High' }
  ]}
  value={priority}
  onChange={setPriority}
/>

// Multi-select
<MultiSelect
  label="Assignees"
  options={users}
  value={selectedUsers}
  onChange={setSelectedUsers}
  isSearchable
/>

// Checkbox group
<CheckboxGroup
  label="Features"
  options={features}
  value={selected}
  onChange={setSelected}
/>

// Radio group
<RadioGroup
  label="Status"
  options={[
    { value: 'active', label: 'Active' },
    { value: 'inactive', label: 'Inactive' }
  ]}
  value={status}
  onChange={setStatus}
/>
```

### Table Component

```tsx
<DataTable
  columns={[
    { header: 'Name', accessor: 'name', sortable: true },
    { header: 'Priority', accessor: 'priority' },
    { header: 'Status', accessor: 'status' },
    { header: 'Actions', render: (row) => (
      <div>
        <Button size="sm">Edit</Button>
        <Button size="sm" variant="danger">Delete</Button>
      </div>
    )}
  ]}
  data={features}
  paginated
  pageSize={10}
  sortable
  selectable
  onSelectionChange={setSelected}
/>
```

---

## 🎯 Layout Patterns

### Responsive Grid

```css
/* Mobile-first approach */
.grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

@media (min-width: 768px) {
  .grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

### Sidebar Layout

```tsx
<Layout>
  <Sidebar>
    <Nav items={navItems} />
  </Sidebar>
  <Main>
    <Header>
      <PageTitle>Features</PageTitle>
    </Header>
    <Content>
      {children}
    </Content>
  </Main>
</Layout>
```

---

## ✨ Animation & Transition

### Loading States

```tsx
// Skeleton loader
<Skeleton height={40} count={3} />

// Spinner
<Spinner size="lg" />

// Progress bar
<ProgressBar value={75} />

// Pulse animation
<div className="animate-pulse bg-gray-200 h-12 w-full" />
```

### Transitions

```tsx
// Page transition
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  exit={{ opacity: 0, y: -20 }}
  transition={{ duration: 0.3 }}
>
  {children}
</motion.div>

// Hover effect
<motion.button
  whileHover={{ scale: 1.05 }}
  whileTap={{ scale: 0.95 }}
>
  Click me
</motion.button>
```

---

## ♿ Accessibility

### Semantic HTML

```html
<!-- Use semantic elements -->
<header role="banner">
  <nav aria-label="Main navigation">...</nav>
</header>

<main role="main">
  <article>
    <h1>Feature Title</h1>
    <p>Content</p>
  </article>
</main>

<footer role="contentinfo">...</footer>
```

### ARIA Attributes

```tsx
// Form validation
<input
  aria-label="Email"
  aria-required="true"
  aria-invalid={hasError}
  aria-describedby="email-error"
/>
<span id="email-error" role="alert">Invalid email</span>

// Live regions
<div aria-live="polite" aria-atomic="true">
  {statusMessage}
</div>

// Buttons
<button aria-label="Close dialog" aria-pressed={isOpen}>
  ×
</button>
```

### Keyboard Navigation

```tsx
// Focus management
useEffect(() => {
  if (isOpen) {
    firstButtonRef.current?.focus();
  }
}, [isOpen]);

// Keyboard events
<input
  onKeyDown={(e) => {
    if (e.key === 'Enter') {
      submit();
    } else if (e.key === 'Escape') {
      close();
    }
  }}
/>
```

---

## 📱 Responsive Design

### Mobile-First Breakpoints

```css
/* Mobile (default) */
.container { width: 100%; }

/* Tablet */
@media (min-width: 768px) {
  .container { width: 750px; }
}

/* Desktop */
@media (min-width: 1024px) {
  .container { width: 970px; }
}

/* Large Desktop */
@media (min-width: 1280px) {
  .container { width: 1170px; }
}
```

### Responsive Typography

```css
/* Scale font based on viewport */
h1 {
  font-size: clamp(1.5rem, 5vw, 3rem);
  line-height: 1.2;
}

p {
  font-size: clamp(0.875rem, 2vw, 1.125rem);
  line-height: 1.6;
}
```

---

## 🎓 Best Practices

1. **Consistency** - Use design tokens
2. **Contrast** - WCAG AA minimum
3. **Feedback** - Immediate response to actions
4. **Error Prevention** - Clear validation
5. **Recovery** - Easy error correction
6. **Efficiency** - Keyboard shortcuts
7. **Learnability** - Intuitive interface
8. **Aesthetics** - Whitespace, typography

---

## 📚 Related Documents

- React Patterns (react_patterns.md)
- Tailwind Utility Classes (tailwind_utility_classes.md)
- Performance (performance.md)

---

**END OF UI/UX PATTERNS DOCUMENT**

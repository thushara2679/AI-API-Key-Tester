# Tailwind CSS Utility Classes Document

## 📋 Document Overview

**Project Name:** Advanced AI Agent System for Enterprise Automation
**Version:** 1.0
**Document Type:** Tailwind CSS Quick Reference
**Tailwind Version:** 3.3+
**Focus:** 150+ commonly used utility classes

---

## 🎨 Layout & Spacing

### Display

```html
<!-- Display types -->
<div class="block">Block element</div>
<div class="inline">Inline element</div>
<div class="inline-block">Inline-block</div>
<div class="flex">Flex container</div>
<div class="grid">Grid container</div>
<div class="hidden">Hidden element</div>
<div class="flex md:hidden">Hidden on md+</div>

<!-- Visibility -->
<div class="visible">Visible</div>
<div class="invisible">Invisible (takes space)</div>
```

### Flexbox

```html
<!-- Direction -->
<div class="flex flex-row">Row (default)</div>
<div class="flex flex-col">Column</div>
<div class="flex flex-row-reverse">Reverse row</div>
<div class="flex flex-col-reverse">Reverse column</div>

<!-- Justify Content -->
<div class="flex justify-start">Start</div>
<div class="flex justify-center">Center</div>
<div class="flex justify-end">End</div>
<div class="flex justify-between">Space between</div>
<div class="flex justify-around">Space around</div>
<div class="flex justify-evenly">Space evenly</div>

<!-- Align Items -->
<div class="flex items-start">Start</div>
<div class="flex items-center">Center</div>
<div class="flex items-end">End</div>
<div class="flex items-baseline">Baseline</div>
<div class="flex items-stretch">Stretch</div>

<!-- Flex Grow/Shrink -->
<div class="flex">
  <div class="flex-1">Grow</div>
  <div class="flex-none">No grow</div>
  <div class="flex-initial">Initial</div>
</div>

<!-- Gap -->
<div class="flex gap-0">No gap</div>
<div class="flex gap-2">Small gap</div>
<div class="flex gap-4">Medium gap</div>
<div class="flex gap-8">Large gap</div>
```

### Grid

```html
<!-- Grid setup -->
<div class="grid grid-cols-1">1 column</div>
<div class="grid grid-cols-2">2 columns</div>
<div class="grid grid-cols-3">3 columns</div>
<div class="grid grid-cols-12">12 columns</div>
<div class="grid grid-cols-none">No columns</div>

<!-- Responsive grid -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
  Responsive
</div>

<!-- Grid gap -->
<div class="grid grid-cols-3 gap-2">Small gap</div>
<div class="grid grid-cols-3 gap-4">Medium gap</div>
<div class="grid grid-cols-3 gap-8">Large gap</div>

<!-- Grid row -->
<div class="grid grid-rows-4">4 rows</div>
<div class="grid grid-rows-none">Auto rows</div>

<!-- Auto flow -->
<div class="grid auto-cols-max">Auto columns</div>
<div class="grid auto-rows-max">Auto rows</div>
```

### Padding & Margin

```html
<!-- Padding (p-{0-96}) -->
<div class="p-0">No padding</div>
<div class="p-2">0.5rem</div>
<div class="p-4">1rem</div>
<div class="p-6">1.5rem</div>
<div class="p-8">2rem</div>
<div class="p-12">3rem</div>

<!-- Directional padding -->
<div class="pt-4">Padding top</div>
<div class="pr-4">Padding right</div>
<div class="pb-4">Padding bottom</div>
<div class="pl-4">Padding left</div>
<div class="px-4">Padding X</div>
<div class="py-4">Padding Y</div>

<!-- Margin (m-{0-96}) -->
<div class="m-0">No margin</div>
<div class="m-2">0.5rem</div>
<div class="m-4">1rem</div>
<div class="m-auto">Auto margin</div>

<!-- Directional margin -->
<div class="mt-4">Margin top</div>
<div class="mr-4">Margin right</div>
<div class="mb-4">Margin bottom</div>
<div class="ml-4">Margin left</div>
<div class="mx-4">Margin X</div>
<div class="my-4">Margin Y</div>

<!-- Negative margin -->
<div class="-m-4">Negative margin</div>
<div class="-mt-4">Negative margin top</div>
```

---

## 🎨 Colors

### Text Color

```html
<!-- Named colors -->
<p class="text-black">Black</p>
<p class="text-white">White</p>
<p class="text-gray-500">Gray 500</p>
<p class="text-red-500">Red 500</p>
<p class="text-blue-500">Blue 500</p>
<p class="text-green-500">Green 500</p>
<p class="text-yellow-500">Yellow 500</p>
<p class="text-purple-500">Purple 500</p>

<!-- Hover state -->
<p class="text-blue-500 hover:text-blue-600">Link</p>
```

### Background Color

```html
<!-- Background -->
<div class="bg-white">White</div>
<div class="bg-gray-100">Gray 100</div>
<div class="bg-blue-500">Blue 500</div>
<div class="bg-gradient-to-r from-blue-500 to-purple-600">
  Gradient
</div>

<!-- Opacity -->
<div class="bg-blue-500 bg-opacity-50">50% opacity</div>
<div class="bg-blue-500 bg-opacity-25">25% opacity</div>
```

### Border Color

```html
<!-- Border color -->
<div class="border-2 border-gray-300">Gray border</div>
<div class="border-2 border-red-500">Red border</div>
<div class="border-2 border-blue-500">Blue border</div>

<!-- Ring (outline) -->
<button class="ring-2 ring-blue-500">Ring</button>
<button class="ring-offset-2 ring-2 ring-blue-500">Ring offset</button>
```

---

## 🔤 Typography

### Font Size

```html
<p class="text-xs">Extra small</p>
<p class="text-sm">Small</p>
<p class="text-base">Base (default)</p>
<p class="text-lg">Large</p>
<p class="text-xl">X-Large</p>
<p class="text-2xl">2X-Large</p>
<p class="text-3xl">3X-Large</p>
<p class="text-4xl">4X-Large</p>
<p class="text-5xl">5X-Large</p>
<p class="text-6xl">6X-Large</p>
```

### Font Weight

```html
<p class="font-thin">100 weight</p>
<p class="font-light">300 weight</p>
<p class="font-normal">400 weight</p>
<p class="font-medium">500 weight</p>
<p class="font-semibold">600 weight</p>
<p class="font-bold">700 weight</p>
<p class="font-extrabold">800 weight</p>
<p class="font-black">900 weight</p>
```

### Line Height

```html
<p class="leading-tight">1.25</p>
<p class="leading-snug">1.375</p>
<p class="leading-normal">1.5</p>
<p class="leading-relaxed">1.625</p>
<p class="leading-loose">2</p>
```

### Text Alignment

```html
<p class="text-left">Left aligned</p>
<p class="text-center">Center aligned</p>
<p class="text-right">Right aligned</p>
<p class="text-justify">Justified</p>
```

### Text Decoration

```html
<a class="underline">Underline</a>
<a class="line-through">Line-through</a>
<a class="no-underline">No underline</a>
<p class="uppercase">uppercase</p>
<p class="lowercase">LOWERCASE</p>
<p class="capitalize">capitalize each</p>
<p class="italic">Italic</p>
<p class="not-italic">Not italic</p>
```

---

## 📦 Sizing

### Width

```html
<div class="w-0">0%</div>
<div class="w-1/2">50%</div>
<div class="w-1/3">33.333%</div>
<div class="w-2/3">66.666%</div>
<div class="w-1/4">25%</div>
<div class="w-3/4">75%</div>
<div class="w-full">100%</div>
<div class="w-screen">100vw</div>
<div class="w-min">Min content</div>
<div class="w-max">Max content</div>
<div class="w-fit">Fit content</div>

<!-- Fixed width -->
<div class="w-64">16rem</div>
<div class="w-96">24rem</div>
```

### Height

```html
<div class="h-0">0</div>
<div class="h-full">100%</div>
<div class="h-screen">100vh</div>
<div class="h-min">Min content</div>
<div class="h-max">Max content</div>
<div class="h-fit">Fit content</div>

<!-- Fixed height -->
<div class="h-64">16rem</div>
<div class="h-96">24rem</div>
```

### Min/Max

```html
<div class="min-w-0">Min width 0</div>
<div class="max-w-full">Max width 100%</div>
<div class="max-w-screen-lg">Max width container</div>
<div class="min-h-0">Min height 0</div>
<div class="max-h-full">Max height 100%</div>
```

---

## 🎯 Borders & Shadows

### Border

```html
<!-- Border width -->
<div class="border">1px border</div>
<div class="border-2">2px border</div>
<div class="border-4">4px border</div>
<div class="border-8">8px border</div>

<!-- Border radius -->
<div class="rounded">0.25rem</div>
<div class="rounded-md">0.375rem</div>
<div class="rounded-lg">0.5rem</div>
<div class="rounded-xl">0.75rem</div>
<div class="rounded-2xl">1rem</div>
<div class="rounded-full">50%</div>

<!-- Directional -->
<div class="rounded-tl-lg">Top left</div>
<div class="rounded-tr-lg">Top right</div>
<div class="rounded-bl-lg">Bottom left</div>
<div class="rounded-br-lg">Bottom right</div>
```

### Shadow

```html
<div class="shadow-sm">Small shadow</div>
<div class="shadow">Default shadow</div>
<div class="shadow-md">Medium shadow</div>
<div class="shadow-lg">Large shadow</div>
<div class="shadow-xl">X-Large shadow</div>
<div class="shadow-2xl">2X-Large shadow</div>
<div class="shadow-none">No shadow</div>

<!-- Shadow color -->
<div class="shadow-lg shadow-blue-500">Blue shadow</div>
```

---

## 🎬 Effects & Transforms

### Opacity

```html
<div class="opacity-0">0%</div>
<div class="opacity-25">25%</div>
<div class="opacity-50">50%</div>
<div class="opacity-75">75%</div>
<div class="opacity-100">100%</div>
```

### Transform

```html
<!-- Scale -->
<div class="scale-0">Scale 0%</div>
<div class="scale-50">Scale 50%</div>
<div class="scale-100">Scale 100%</div>
<div class="scale-125">Scale 125%</div>
<div class="scale-150">Scale 150%</div>

<!-- Rotate -->
<div class="rotate-0">0 degrees</div>
<div class="rotate-45">45 degrees</div>
<div class="rotate-90">90 degrees</div>
<div class="rotate-180">180 degrees</div>
<div class="-rotate-45">-45 degrees</div>

<!-- Translate -->
<div class="translate-x-0">No X translate</div>
<div class="translate-x-1">0.25rem X</div>
<div class="translate-y-2">0.5rem Y</div>
<div class="-translate-x-4">-1rem X</div>
```

### Cursor

```html
<button class="cursor-pointer">Pointer</button>
<button class="cursor-default">Default</button>
<button class="cursor-not-allowed">Not allowed</button>
<button class="cursor-move">Move</button>
<button class="cursor-wait">Wait</button>
```

---

## 🎭 Hover & State

### Interactive States

```html
<!-- Hover -->
<button class="bg-blue-500 hover:bg-blue-600">Hover</button>
<button class="text-blue-500 hover:text-blue-600">Hover text</button>

<!-- Focus -->
<input class="focus:ring-2 focus:ring-blue-500" />
<button class="focus:outline-none focus:ring-2">Focus</button>

<!-- Active -->
<button class="active:scale-95">Active</button>

<!-- Disabled -->
<button class="disabled:opacity-50 disabled:cursor-not-allowed">
  Disabled
</button>

<!-- Group hover -->
<div class="group hover:bg-gray-100">
  <button class="group-hover:text-blue-500">Button</button>
</div>
```

---

## 📱 Responsive Design

```html
<!-- Mobile first -->
<div class="text-sm md:text-base lg:text-lg">
  Text scales with breakpoint
</div>

<!-- Breakpoints -->
sm: 640px
md: 768px
lg: 1024px
xl: 1280px
2xl: 1536px

<!-- Examples -->
<div class="w-full md:w-1/2 lg:w-1/3">Responsive width</div>
<div class="flex flex-col md:flex-row">Responsive direction</div>
<div class="hidden lg:block">Hidden until lg</div>
<div class="block lg:hidden">Hidden from lg</div>
```

---

## 🎓 Common Patterns

### Centered Container

```html
<div class="container mx-auto px-4">
  <div class="max-w-6xl">Content</div>
</div>
```

### Card

```html
<div class="bg-white rounded-lg shadow-md p-6">
  <h3 class="text-xl font-bold mb-2">Card Title</h3>
  <p class="text-gray-600">Card content</p>
</div>
```

### Button Variants

```html
<!-- Primary -->
<button class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded">
  Primary
</button>

<!-- Secondary -->
<button class="bg-gray-200 hover:bg-gray-300 text-gray-800 px-4 py-2 rounded">
  Secondary
</button>

<!-- Danger -->
<button class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded">
  Delete
</button>
```

### Alert

```html
<!-- Info -->
<div class="bg-blue-100 border border-blue-400 text-blue-700 px-4 py-3 rounded">
  Info message
</div>

<!-- Warning -->
<div class="bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-3 rounded">
  Warning message
</div>

<!-- Error -->
<div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
  Error message
</div>
```

---

## 📚 Related Documents

- UI/UX Patterns (ui_ux_patterns.md)
- React Patterns (react_patterns.md)
- Performance (performance.md)

---

**END OF TAILWIND CSS UTILITY CLASSES DOCUMENT**

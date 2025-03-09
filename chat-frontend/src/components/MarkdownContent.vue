<template>
  <div class="markdown-body prose dark:prose-invert" v-html="renderedContent"></div>
</template>

<script setup>
import { computed } from 'vue'
import MarkdownIt from 'markdown-it'
import hljs from 'highlight.js'

const md = new MarkdownIt({
  linkify: true,
  breaks: true,
  highlight: (str, lang) => {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return `<pre class="hljs"><code>${hljs.highlight(str, { language: lang, ignoreIllegals: true }).value}</code></pre>`
      } catch (e) {}
    }
    return `<pre class="hljs"><code>${md.utils.escapeHtml(str)}</code></pre>`
  }
})

const props = defineProps({
  content: String
})

const renderedContent = computed(() => md.render(props.content || ''))
</script>

<style>
.markdown-body {
  font-size: 14px;
  line-height: 1.6;
}

.markdown-body :deep(p) {
  margin: 1em 0;
  color: inherit;
}

.markdown-body :deep(pre) {
  margin: 1em 0;
  padding: 1em;
  border-radius: 0.5rem;
  background-color: #1a1b26;
  overflow-x: auto;
}

.dark .markdown-body :deep(pre) {
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.markdown-body :deep(pre code) {
  padding: 0;
  background: none;
  border-radius: 0;
  color: #e2e8f0;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
}

.markdown-body :deep(code):not(pre code) {
  color: #7dd3fc;
  background-color: rgba(30, 41, 59, 0.5);
  padding: 0.2em 0.4em;
  border-radius: 0.25rem;
  font-size: 0.875em;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
}

.markdown-body :deep(ul), .markdown-body :deep(ol) {
  margin: 1em 0;
  padding-left: 1.5em;
  color: inherit;
}

.markdown-body :deep(li) {
  margin: 0.5em 0;
  color: inherit;
}

.markdown-body :deep(blockquote) {
  margin: 1em 0;
  padding-left: 1em;
  border-left: 4px solid;
  border-color: #e5e7eb;
  color: inherit;
}

.dark .markdown-body :deep(blockquote) {
  border-color: #374151;
}

.markdown-body :deep(h1),
.markdown-body :deep(h2),
.markdown-body :deep(h3),
.markdown-body :deep(h4),
.markdown-body :deep(h5),
.markdown-body :deep(h6) {
  margin: 1.5em 0 0.5em;
  font-weight: 600;
  line-height: 1.25;
  color: inherit;
}

.markdown-body :deep(h1) { font-size: 2em; }
.markdown-body :deep(h2) { font-size: 1.5em; }
.markdown-body :deep(h3) { font-size: 1.25em; }
.markdown-body :deep(h4) { font-size: 1em; }
.markdown-body :deep(h5) { font-size: 0.875em; }
.markdown-body :deep(h6) { font-size: 0.85em; }

.markdown-body :deep(table) {
  margin: 1em 0;
  border-collapse: collapse;
  width: 100%;
  color: inherit;
}

.markdown-body :deep(th),
.markdown-body :deep(td) {
  padding: 0.5em;
  border: 1px solid;
  border-color: #e5e7eb;
}

.dark .markdown-body :deep(th),
.dark .markdown-body :deep(td) {
  border-color: #374151;
}

.markdown-body :deep(th) {
  background-color: #f3f4f6;
  font-weight: 600;
}

.dark .markdown-body :deep(th) {
  background-color: #374151;
}

/* 链接样式 */
.markdown-body :deep(a) {
  color: #3b82f6;
  text-decoration: none;
  transition: color 0.2s;
}

.markdown-body :deep(a:hover) {
  color: #2563eb;
  text-decoration: underline;
}

.dark .markdown-body :deep(a) {
  color: #60a5fa;
}

.dark .markdown-body :deep(a:hover) {
  color: #93c5fd;
}

/* 图片样式 */
.markdown-body :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 0.5rem;
}

/* 水平线样式 */
.markdown-body :deep(hr) {
  margin: 2em 0;
  border: 0;
  border-top: 1px solid #e5e7eb;
}

.dark .markdown-body :deep(hr) {
  border-color: #374151;
}
</style>

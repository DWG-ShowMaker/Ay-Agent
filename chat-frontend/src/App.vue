<template>
  <el-config-provider>
    <router-view/>
  </el-config-provider>
</template>

<script setup>
</script>

<style>
:root {
  --ai-dark: #202123;
  --ai-sidebar: #202123;
  --ai-chat-bg-dark: #343541;
  --ai-chat-bg-light: #ffffff;
  --ai-assistant-bg: #444654;
  --ai-border: rgba(255,255,255,.1);
  --ai-text: #ececf1;
  --ai-text-dark: #000000;
  --ai-green: #10a37f;
}

html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  font-family: Söhne,ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,Cantarell,Noto Sans,sans-serif;
  background: var(--ai-chat-bg-light);
  color: var(--ai-text-dark);
  -webkit-font-smoothing: antialiased;
}

body.dark {
  background: var(--ai-chat-bg-dark);
  color: var(--ai-text);
}

#app {
  height: 100vh;
}

.markdown-body {
  font-size: 14px;
  line-height: 1.6;
  color: var(--ai-text-dark);
  margin: 0.5em 0;
}

body.dark .markdown-body {
  color: var(--ai-text);
}

.markdown-body pre {
  background: var(--ai-dark);
  border-radius: 6px;
  padding: 1rem;
  overflow: auto;
}

.markdown-body code {
  font-family: ui-monospace, SFMono-Regular, SF Mono, Menlo, monospace;
  font-size: 12px;
  background: var(--ai-dark);
}

.markdown-body h1, .markdown-body h2, .markdown-body h3, .markdown-body h4, .markdown-body h5, .markdown-body h6 {
  margin: 0.5em 0;
  font-weight: bold;
}

.markdown-body ul, .markdown-body ol {
  margin: 0.5em 0;
  padding-left: 1.5em;
}

.markdown-body blockquote {
  margin: 0.5em 0;
  padding-left: 1em;
  border-left: 4px solid var(--ai-border);
  color: var(--ai-text-dark);
}

body.dark .markdown-body blockquote {
  color: var(--ai-text);
}

/* Element Plus主题覆盖 */
.el-button--primary {
  --el-button-bg-color: var(--ai-green);
  --el-button-border-color: var(--ai-green);
  --el-button-hover-bg-color: var(--ai-green);
  --el-button-hover-border-color: var(--ai-green);
  --el-button-active-bg-color: var(--ai-green);
  --el-button-active-border-color: var(--ai-green);
}
</style>

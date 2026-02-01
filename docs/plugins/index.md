---
title: Tous les Plugins
---

# Tous les Plugins

<script setup>
import { data as plugins } from '../.vitepress/data/plugins.data'
</script>

<div v-for="plugin in plugins" :key="plugin.name" class="plugin-card">
  <h2>
    <a :href="'/claude-marketplace/plugins/' + plugin.slug">{{ plugin.name }}</a>
    <Badge type="info" :text="'v' + plugin.version" />
  </h2>
  <p>{{ plugin.description }}</p>
  <div class="meta">
    <Badge type="tip" :text="plugin.skillCount + ' skills'" />
    <span v-for="keyword in plugin.keywords.slice(0, 3)" :key="keyword">
      <Badge type="warning" :text="keyword" />
    </span>
  </div>
</div>

---
title: Plugins par Catégorie
---

# Plugins par Catégorie

<script setup>
import { data as plugins } from '../.vitepress/data/plugins.data'

const categories = {
  'Git & Workflow': ['git', 'github', 'review'],
  'Développement': ['dev', 'framework', 'qa', 'feature-dev'],
  'Framework': ['symfony'],
  'Documentation': ['doc', 'prompt', 'claude'],
  'IA': ['gemini'],
  'Outils': ['customize', 'notifications', 'chrome-ui-test', 'marketing', 'command', 'mlvn']
}

function getPluginsByCategory(category) {
  const slugs = categories[category] || []
  return plugins.filter(p => slugs.includes(p.slug))
}
</script>

## Git & Workflow

<div v-for="plugin in getPluginsByCategory('Git & Workflow')" :key="plugin.slug" class="plugin-card">
  <h3>
    <a :href="'/claude-marketplace/plugins/' + plugin.slug">{{ plugin.name }}</a>
    <Badge type="info" :text="'v' + plugin.version" />
  </h3>
  <p>{{ plugin.description }}</p>
  <div class="meta">
    <Badge type="tip" :text="plugin.skillCount + ' skills'" />
  </div>
</div>

## Développement

<div v-for="plugin in getPluginsByCategory('Développement')" :key="plugin.slug" class="plugin-card">
  <h3>
    <a :href="'/claude-marketplace/plugins/' + plugin.slug">{{ plugin.name }}</a>
    <Badge type="info" :text="'v' + plugin.version" />
  </h3>
  <p>{{ plugin.description }}</p>
  <div class="meta">
    <Badge type="tip" :text="plugin.skillCount + ' skills'" />
  </div>
</div>

## Framework

<div v-for="plugin in getPluginsByCategory('Framework')" :key="plugin.slug" class="plugin-card">
  <h3>
    <a :href="'/claude-marketplace/plugins/' + plugin.slug">{{ plugin.name }}</a>
    <Badge type="info" :text="'v' + plugin.version" />
  </h3>
  <p>{{ plugin.description }}</p>
  <div class="meta">
    <Badge type="tip" :text="plugin.skillCount + ' skills'" />
  </div>
</div>

## Documentation

<div v-for="plugin in getPluginsByCategory('Documentation')" :key="plugin.slug" class="plugin-card">
  <h3>
    <a :href="'/claude-marketplace/plugins/' + plugin.slug">{{ plugin.name }}</a>
    <Badge type="info" :text="'v' + plugin.version" />
  </h3>
  <p>{{ plugin.description }}</p>
  <div class="meta">
    <Badge type="tip" :text="plugin.skillCount + ' skills'" />
  </div>
</div>

## IA

<div v-for="plugin in getPluginsByCategory('IA')" :key="plugin.slug" class="plugin-card">
  <h3>
    <a :href="'/claude-marketplace/plugins/' + plugin.slug">{{ plugin.name }}</a>
    <Badge type="info" :text="'v' + plugin.version" />
  </h3>
  <p>{{ plugin.description }}</p>
  <div class="meta">
    <Badge type="tip" :text="plugin.skillCount + ' skills'" />
  </div>
</div>

## Outils

<div v-for="plugin in getPluginsByCategory('Outils')" :key="plugin.slug" class="plugin-card">
  <h3>
    <a :href="'/claude-marketplace/plugins/' + plugin.slug">{{ plugin.name }}</a>
    <Badge type="info" :text="'v' + plugin.version" />
  </h3>
  <p>{{ plugin.description }}</p>
  <div class="meta">
    <Badge type="tip" :text="plugin.skillCount + ' skills'" />
  </div>
</div>

## Navigation

- [Tous les plugins](/plugins/) - Liste complète
- [Index des commandes](/commands/) - 69 slash commands

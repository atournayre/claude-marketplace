---
title: Use Cases
---

<script setup>
import { data as usecases } from '../.vitepress/data/usecases.data'
import { computed } from 'vue'

const byComplexity = computed(() => {
  const grouped = {}
  for (let i = 1; i <= 5; i++) {
    grouped[i] = usecases.filter(uc => uc.complexity === i)
  }
  return grouped
})

const complexityLabels = {
  1: 'Débutant',
  2: 'Intermédiaire',
  3: 'Avancé',
  4: 'Expert',
  5: 'Complexe'
}
</script>

# Use Cases

Découvre des scénarios concrets d'utilisation des plugins du marketplace.

## Navigation

- [Par catégorie](/usecases/by-category) - Use cases groupés par domaine
- [Par plugin](/usecases/by-plugin) - Use cases groupés par plugin utilisé

## Par Niveau de Complexité

<div v-for="level in [1, 2, 3, 4, 5]" :key="level" class="complexity-section">
  <h3>{{ '★'.repeat(level) }} {{ complexityLabels[level] }}</h3>

  <div v-if="byComplexity[level].length === 0" class="empty-state">
    Aucun use case pour ce niveau
  </div>

  <div v-for="uc in byComplexity[level]" :key="uc.slug" class="usecase-card">
    <h4>
      <a :href="'/claude-marketplace/usecases/' + uc.categorySlug + '/' + uc.slug">
        {{ uc.title }}
      </a>
      <Badge type="tip" :text="'~' + uc.duration + ' min'" />
    </h4>
    <p>{{ uc.description }}</p>
    <div class="meta">
      <Badge type="warning" :text="uc.category" />
      <span v-for="plugin in uc.plugins.slice(0, 2)" :key="plugin.name">
        <Badge type="info" :text="plugin.name" />
      </span>
    </div>
  </div>
</div>

<style scoped>
.complexity-section {
  margin-bottom: 2rem;
}

.usecase-card {
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
  transition: border-color 0.3s;
}

.usecase-card:hover {
  border-color: var(--vp-c-brand);
}

.usecase-card h4 {
  margin-top: 0;
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.usecase-card p {
  margin: 0.5rem 0;
  color: var(--vp-c-text-2);
}

.meta {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.5rem;
  flex-wrap: wrap;
}

.empty-state {
  color: var(--vp-c-text-3);
  font-style: italic;
  padding: 1rem;
}
</style>

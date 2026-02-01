import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'
import matter from 'gray-matter'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const docsDir = path.resolve(__dirname, '..')
const usecasesDir = path.join(docsDir, 'usecases')

interface UseCase {
  title: string
  description: string
  category: string
  categorySlug: string
  slug: string
  plugins: Array<{ name: string; skills: string[] }>
  complexity: number
  duration: number
  keywords: string[]
}

function scanUseCases(): UseCase[] {
  const usecases: UseCase[] = []

  function walkDir(dir: string, category: string = '') {
    // Vérifier que le dossier existe
    if (!fs.existsSync(dir)) {
      console.warn(`⚠️  Dossier inexistant : ${dir}`)
      return
    }

    const entries = fs.readdirSync(dir, { withFileTypes: true })

    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name)

      if (entry.isDirectory()) {
        walkDir(fullPath, entry.name)
      } else if (
        entry.name.endsWith('.md') &&
        !entry.name.startsWith('index') &&
        !entry.name.startsWith('by-')
      ) {
        try {
          const content = fs.readFileSync(fullPath, 'utf-8')
          const { data } = matter(content)

          usecases.push({
            ...data,
            categorySlug: category,
            slug: entry.name.replace('.md', '')
          } as UseCase)
        } catch (error) {
          console.error(`❌ Erreur lors du parsing de ${fullPath}:`, error)
        }
      }
    }
  }

  walkDir(usecasesDir)
  return usecases
}

function generateByCategory() {
  const usecases = scanUseCases()

  if (usecases.length === 0) {
    console.warn('⚠️  Aucun use case trouvé')
    return
  }

  const grouped = usecases.reduce((acc, uc) => {
    if (!acc[uc.category]) acc[uc.category] = []
    acc[uc.category].push(uc)
    return acc
  }, {} as Record<string, UseCase[]>)

  let content = `---
title: Use Cases par Catégorie
description: Tous les use cases organisés par catégorie
---

# Use Cases par Catégorie

`

  const categoryLabels: Record<string, string> = {
    'git-workflow': 'Git & Workflow',
    development: 'Development',
    framework: 'Framework',
    testing: 'Testing',
    advanced: 'Advanced'
  }

  for (const [cat, cases] of Object.entries(grouped).sort()) {
    const label = categoryLabels[cat] || cat
    content += `## ${label}\n\n`

    // Trier par complexité
    cases.sort((a, b) => a.complexity - b.complexity)

    cases.forEach(uc => {
      const stars = '★'.repeat(uc.complexity)
      content += `### [${uc.title}](/usecases/${uc.categorySlug}/${uc.slug}) <Badge type="info" text="${stars}" /> <Badge type="tip" text="~${uc.duration} min" />\n\n`
      content += `${uc.description}\n\n`
      content += `**Plugins :** `
      content += uc.plugins.map(p => `[${p.name}](/plugins/${p.name})`).join(', ')
      content += '\n\n'

      if (uc.keywords && uc.keywords.length > 0) {
        content += `**Mots-clés :** ${uc.keywords.join(', ')}\n\n`
      }

      content += '---\n\n'
    })

    content += '\n'
  }

  const outputPath = path.join(usecasesDir, 'by-category.md')
  fs.writeFileSync(outputPath, content)
  console.log(`✅ ${outputPath} généré (${usecases.length} use cases)`)
}

function generateByPlugin() {
  const usecases = scanUseCases()

  if (usecases.length === 0) {
    console.warn('⚠️  Aucun use case trouvé')
    return
  }

  const grouped: Record<string, UseCase[]> = {}

  usecases.forEach(uc => {
    uc.plugins.forEach(plugin => {
      if (!grouped[plugin.name]) grouped[plugin.name] = []
      grouped[plugin.name].push(uc)
    })
  })

  let content = `---
title: Use Cases par Plugin
description: Tous les use cases organisés par plugin utilisé
---

# Use Cases par Plugin

`

  for (const [plugin, cases] of Object.entries(grouped).sort()) {
    content += `## [${plugin}](/plugins/${plugin})\n\n`

    // Trier par complexité
    cases.sort((a, b) => a.complexity - b.complexity)

    cases.forEach(uc => {
      const stars = '★'.repeat(uc.complexity)
      content += `### [${uc.title}](/usecases/${uc.categorySlug}/${uc.slug}) <Badge type="info" text="${stars}" /> <Badge type="tip" text="~${uc.duration} min" />\n\n`
      content += `${uc.description}\n\n`

      // Afficher les skills utilisés pour ce plugin
      const pluginInfo = uc.plugins.find(p => p.name === plugin)
      if (pluginInfo && pluginInfo.skills && pluginInfo.skills.length > 0) {
        content += `**Skills :** ${pluginInfo.skills.map(s => `\`${s}\``).join(', ')}\n\n`
      }

      content += '---\n\n'
    })

    content += '\n'
  }

  const outputPath = path.join(usecasesDir, 'by-plugin.md')
  fs.writeFileSync(outputPath, content)
  console.log(`✅ ${outputPath} généré (${Object.keys(grouped).length} plugins)`)
}

// Main
console.log('🚀 Génération des index use cases...\n')

try {
  generateByCategory()
  generateByPlugin()
  console.log('\n✨ Terminé !')
} catch (error) {
  console.error('\n❌ Erreur lors de la génération:', error)
  process.exit(1)
}

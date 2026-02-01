import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const rootDir = path.resolve(__dirname, '..')
const docsDir = path.join(rootDir, 'docs')

interface PluginMetadata {
  name: string
  version: string
  description: string
  author: { name: string; email: string }
  keywords: string[]
}

interface Command {
  command: string
  plugin: string
  description: string
}

// Fonction pour trouver tous les dossiers de plugins
function findPluginDirectories(): string[] {
  const entries = fs.readdirSync(rootDir, { withFileTypes: true })
  return entries
    .filter(entry => entry.isDirectory())
    .filter(entry => {
      const pluginJsonPath = path.join(rootDir, entry.name, '.claude-plugin', 'plugin.json')
      return fs.existsSync(pluginJsonPath)
    })
    .map(entry => entry.name)
}

// Fonction pour lire plugin.json
function readPluginJson(pluginDir: string): PluginMetadata {
  const pluginJsonPath = path.join(rootDir, pluginDir, '.claude-plugin', 'plugin.json')
  return JSON.parse(fs.readFileSync(pluginJsonPath, 'utf-8'))
}

// Fonction pour transformer les liens internes
function transformLinks(content: string, pluginDir: string): string {
  // Transformer les liens vers d'autres README
  content = content.replace(/\.\.\/([\w-]+)\/README\.md/g, '/plugins/$1')

  // Transformer les liens vers des skills dans le même plugin
  content = content.replace(/\.\/skills\/([\w-]+)\/SKILL\.md/g, '#$1')

  // Supprimer les badges GitHub Actions qui ne fonctionneront plus
  content = content.replace(/!\[.*?\]\(https:\/\/github\.com\/.*?\/workflows\/.*?\)/g, '')

  // Supprimer les liens vers des fichiers locaux qui n'existent pas dans docs
  content = content.replace(/\[([^\]]+)\]\(\.?\/?(MODELS|CHANGELOG|[A-Z_]+)\.md\)/g, '$1')
  content = content.replace(/\[([^\]]+)\]\((MODELS|CHANGELOG|[A-Z_]+)\.md\)/g, '$1')

  return content
}

// Phase 2.1 : Copier et transformer les README
function copyPluginReadmes() {
  console.log('📄 Copie des README des plugins...')

  const pluginDirs = findPluginDirectories()
  const pluginsDir = path.join(docsDir, 'plugins')

  if (!fs.existsSync(pluginsDir)) {
    fs.mkdirSync(pluginsDir, { recursive: true })
  }

  pluginDirs.forEach(dir => {
    const readmePath = path.join(rootDir, dir, 'README.md')

    if (!fs.existsSync(readmePath)) {
      console.warn(`⚠️  README manquant pour ${dir}`)
      return
    }

    let content = fs.readFileSync(readmePath, 'utf-8')
    const pluginJson = readPluginJson(dir)

    // Transformer les liens
    content = transformLinks(content, dir)

    // Retirer le titre principal s'il existe (on va le remplacer)
    content = content.replace(/^#\s+.+?\n/m, '')

    // Échapper les guillemets et caractères YAML problématiques dans la description
    const escapedDescription = pluginJson.description
      .replace(/"/g, '\\"')
      .replace(/:/g, ' -')

    // Créer le frontmatter et le nouveau contenu
    const frontmatter = `---
title: "${pluginJson.name}"
description: "${escapedDescription}"
version: "${pluginJson.version}"
---

# ${pluginJson.name} <Badge type="info" text="v${pluginJson.version}" />

${content}`

    const outputPath = path.join(pluginsDir, `${dir}.md`)
    fs.writeFileSync(outputPath, frontmatter)
    console.log(`  ✅ ${dir}.md`)
  })

  console.log(`✅ ${pluginDirs.length} fichiers de plugins copiés`)
}

// Phase 2.2 : Générer l'index des commandes
function generateCommandsIndex() {
  console.log('📋 Génération de l\'index des commandes...')

  const allCommands: Command[] = []
  const pluginDirs = findPluginDirectories()

  pluginDirs.forEach(pluginDir => {
    const skillsDir = path.join(rootDir, pluginDir, 'skills')

    if (!fs.existsSync(skillsDir)) {
      return
    }

    // Lire tous les sous-dossiers de skills
    const skillDirs = fs.readdirSync(skillsDir, { withFileTypes: true })
      .filter(entry => entry.isDirectory())

    skillDirs.forEach(skillEntry => {
      const skillPath = path.join(skillsDir, skillEntry.name, 'SKILL.md')

      if (!fs.existsSync(skillPath)) {
        return
      }

      const skillContent = fs.readFileSync(skillPath, 'utf-8')

      // Parser le frontmatter YAML
      const frontmatterMatch = skillContent.match(/^---\n([\s\S]+?)\n---/)
      if (!frontmatterMatch) {
        return
      }

      const frontmatter = frontmatterMatch[1]
      const nameMatch = frontmatter.match(/name:\s*['"]?(.+?)['"]?\s*$/m)
      const descMatch = frontmatter.match(/description:\s*['"]?(.+?)['"]?\s*$/m)

      if (nameMatch && descMatch) {
        allCommands.push({
          command: nameMatch[1],
          plugin: pluginDir,
          description: descMatch[1]
        })
      }
    })
  })

  // Trier par nom de commande
  allCommands.sort((a, b) => a.command.localeCompare(b.command))

  // Générer la table markdown
  const tableRows = allCommands.map(cmd =>
    `| \`/${cmd.command}\` | [${cmd.plugin}](/plugins/${cmd.plugin}) | ${cmd.description} |`
  ).join('\n')

  const content = `---
title: Index des Commandes
---

# Index des Commandes

${allCommands.length} commandes disponibles dans le marketplace.

| Commande | Plugin | Description |
|----------|--------|-------------|
${tableRows}
`

  const commandsDir = path.join(docsDir, 'commands')
  if (!fs.existsSync(commandsDir)) {
    fs.mkdirSync(commandsDir, { recursive: true })
  }

  fs.writeFileSync(path.join(commandsDir, 'index.md'), content)
  console.log(`✅ Index de ${allCommands.length} commandes généré`)
}

// Phase 2.3 : Générer l'index des plugins
function generatePluginIndex() {
  console.log('🔌 Génération de l\'index des plugins...')

  const content = `---
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
`

  const pluginsDir = path.join(docsDir, 'plugins')
  fs.writeFileSync(path.join(pluginsDir, 'index.md'), content)
  console.log('✅ Index des plugins généré')
}

// Exécution principale
function main() {
  console.log('🚀 Génération de la documentation VitePress...\n')

  copyPluginReadmes()
  console.log()

  generateCommandsIndex()
  console.log()

  generatePluginIndex()
  console.log()

  console.log('✨ Génération terminée!')
}

main()

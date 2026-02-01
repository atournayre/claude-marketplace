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

interface Agent {
  name: string
  plugin: string
  description: string
  tools: string
}

interface Hook {
  name: string
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
title: Index des Skills
---

# Index des Skills

${allCommands.length} skills disponibles dans le marketplace.

**Note** : Les skills sont invoquées via slash commands (ex: \`/git:commit\`, \`/dev:feature\`).

| Skill | Plugin | Description |
|-------|--------|-------------|
${tableRows}
`

  const commandsDir = path.join(docsDir, 'commands')
  if (!fs.existsSync(commandsDir)) {
    fs.mkdirSync(commandsDir, { recursive: true })
  }

  fs.writeFileSync(path.join(commandsDir, 'index.md'), content)
  console.log(`✅ Index de ${allCommands.length} commandes généré`)
}

// Phase 2.2b : Générer l'index des agents
function generateAgentsIndex() {
  console.log('🤖 Génération de l\'index des agents...')

  const allAgents: Agent[] = []
  const pluginDirs = findPluginDirectories()

  pluginDirs.forEach(pluginDir => {
    const agentsDir = path.join(rootDir, pluginDir, 'agents')

    if (!fs.existsSync(agentsDir)) {
      return
    }

    // Lire tous les fichiers .md dans agents/
    const agentFiles = fs.readdirSync(agentsDir, { withFileTypes: true })
      .filter(entry => entry.isFile() && entry.name.endsWith('.md'))

    agentFiles.forEach(agentFile => {
      const agentPath = path.join(agentsDir, agentFile.name)
      const agentContent = fs.readFileSync(agentPath, 'utf-8')

      // Parser le frontmatter YAML
      const frontmatterMatch = agentContent.match(/^---\n([\s\S]+?)\n---/)
      if (!frontmatterMatch) {
        return
      }

      const frontmatter = frontmatterMatch[1]
      const nameMatch = frontmatter.match(/name:\s*['"]?(.+?)['"]?\s*$/m)
      const descMatch = frontmatter.match(/description:\s*['"]?(.+?)['"]?\s*$/m)
      const toolsMatch = frontmatter.match(/tools:\s*(.+?)\s*$/m)

      if (nameMatch && descMatch) {
        allAgents.push({
          name: nameMatch[1],
          plugin: pluginDir,
          description: descMatch[1],
          tools: toolsMatch ? toolsMatch[1] : 'N/A'
        })
      }
    })
  })

  // Trier par nom d'agent
  allAgents.sort((a, b) => a.name.localeCompare(b.name))

  // Générer la table markdown
  const tableRows = allAgents.map(agent =>
    `| \`${agent.name}\` | [${agent.plugin}](/plugins/${agent.plugin}) | ${agent.description} | ${agent.tools} |`
  ).join('\n')

  const content = `---
title: Index des Agents
---

# Index des Agents

${allAgents.length} agents disponibles dans le marketplace.

**Note** : Les agents sont des sous-agents spécialisés qui peuvent être invoqués via le Task tool.

| Agent | Plugin | Description | Outils |
|-------|--------|-------------|--------|
${tableRows}
`

  const agentsDir = path.join(docsDir, 'agents')
  if (!fs.existsSync(agentsDir)) {
    fs.mkdirSync(agentsDir, { recursive: true })
  }

  fs.writeFileSync(path.join(agentsDir, 'index.md'), content)
  console.log(`✅ Index de ${allAgents.length} agents généré`)
}

// Phase 2.2c : Générer l'index des hooks
function generateHooksIndex() {
  console.log('🪝 Génération de l\'index des hooks...')

  // Mapping des descriptions par défaut pour les hooks standards
  const hookDefaultDescriptions: Record<string, string> = {
    'pre_tool_use': 'Exécuté avant chaque utilisation d\'outil',
    'post_tool_use': 'Exécuté après chaque utilisation d\'outil',
    'session_start': 'Exécuté au démarrage d\'une session',
    'session_end': 'Exécuté à la fin d\'une session',
    'user_prompt_submit': 'Exécuté lors de la soumission d\'un prompt utilisateur',
    'subagent_start': 'Exécuté au démarrage d\'un sous-agent',
    'subagent_stop': 'Exécuté à l\'arrêt d\'un sous-agent',
    'pre_compact': 'Exécuté avant la compaction du contexte',
    'notification': 'Envoie des notifications système',
    'write_notification': 'Écrit des notifications dans la queue',
    'stop': 'Exécuté à l\'arrêt de Claude Code'
  }

  const allHooks: Hook[] = []
  const pluginDirs = findPluginDirectories()

  pluginDirs.forEach(pluginDir => {
    const hooksDir = path.join(rootDir, pluginDir, 'hooks')

    if (!fs.existsSync(hooksDir)) {
      return
    }

    // Lire tous les fichiers .py dans hooks/ (sauf __init__.py et utils.py)
    const hookFiles = fs.readdirSync(hooksDir, { withFileTypes: true })
      .filter(entry =>
        entry.isFile() &&
        entry.name.endsWith('.py') &&
        !entry.name.startsWith('_') &&
        entry.name !== 'utils.py'
      )

    hookFiles.forEach(hookFile => {
      const hookPath = path.join(hooksDir, hookFile.name)
      const hookContent = fs.readFileSync(hookPath, 'utf-8')

      // Extraire le nom du hook (nom du fichier sans .py)
      const hookName = hookFile.name.replace('.py', '')

      // Extraire la description (priorité : docstring de module > fonction > commentaire > mapping > fallback)
      let description = hookDefaultDescriptions[hookName] || 'Hook personnalisé'

      // 1. Essayer docstring de module (""" en début de fichier, possiblement après shebang/imports)
      const moduleDocstringMatch = hookContent.match(/^\s*(?:#!.*?\n)?[\s\n]*"""([\s\S]+?)"""/)
      if (moduleDocstringMatch) {
        description = moduleDocstringMatch[1].trim().split('\n')[0].trim()
      } else {
        // 2. Essayer docstring de la première fonction
        const functionDocstringMatch = hookContent.match(/def\s+\w+\([^)]*\):[\s\n]+"""([\s\S]+?)"""/)
        if (functionDocstringMatch) {
          description = functionDocstringMatch[1].trim().split('\n')[0].trim()
        } else {
          // 3. Essayer commentaire en début de fichier (après shebang)
          const commentMatch = hookContent.match(/^#!.*?\n#\s*(.+?)$/m)
          if (commentMatch) {
            description = commentMatch[1].trim()
          }
          // Sinon, utiliser le mapping par défaut (déjà défini au début)
        }
      }

      allHooks.push({
        name: hookName,
        plugin: pluginDir,
        description: description
      })
    })
  })

  // Trier par nom de hook
  allHooks.sort((a, b) => a.name.localeCompare(b.name))

  // Générer la table markdown
  const tableRows = allHooks.map(hook =>
    `| \`${hook.name}\` | [${hook.plugin}](/plugins/${hook.plugin}) | ${hook.description} |`
  ).join('\n')

  const content = `---
title: Index des Hooks
---

# Index des Hooks

${allHooks.length} hooks disponibles dans le marketplace.

**Note** : Les hooks sont des scripts Python qui s'exécutent en réponse à des événements (pre_tool_use, post_tool_use, etc.).

| Hook | Plugin | Description |
|------|--------|-------------|
${tableRows}
`

  const hooksDir = path.join(docsDir, 'hooks')
  if (!fs.existsSync(hooksDir)) {
    fs.mkdirSync(hooksDir, { recursive: true })
  }

  fs.writeFileSync(path.join(hooksDir, 'index.md'), content)
  console.log(`✅ Index de ${allHooks.length} hooks généré`)
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
    <Badge v-if="plugin.agentCount > 0" type="tip" :text="plugin.agentCount + ' agents'" />
    <Badge v-if="plugin.hookCount > 0" type="tip" :text="plugin.hookCount + ' hooks'" />
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

  generateAgentsIndex()
  console.log()

  generateHooksIndex()
  console.log()

  generatePluginIndex()
  console.log()

  console.log('✨ Génération terminée!')
}

main()

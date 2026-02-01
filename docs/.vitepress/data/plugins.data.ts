import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

export interface PluginMetadata {
  name: string
  version: string
  description: string
  author: { name: string; email: string }
  keywords: string[]
  skillCount: number
  agentCount: number
  hookCount: number
  readmeLines: number
  slug: string
}

export default {
  async load(): Promise<PluginMetadata[]> {
    const rootDir = path.resolve(__dirname, '../../../')

    // Trouver tous les plugin.json
    const entries = fs.readdirSync(rootDir, { withFileTypes: true })
    const pluginDirs = entries
      .filter(entry => entry.isDirectory())
      .filter(entry => {
        const pluginJsonPath = path.join(rootDir, entry.name, '.claude-plugin', 'plugin.json')
        return fs.existsSync(pluginJsonPath)
      })

    // Charger métadonnées
    const plugins = pluginDirs.map(entry => {
      const dir = entry.name
      const pluginJson = JSON.parse(
        fs.readFileSync(path.join(rootDir, dir, '.claude-plugin', 'plugin.json'), 'utf-8')
      )

      // Compter skills
      const skillsDir = path.join(rootDir, dir, 'skills')
      let skillCount = 0
      if (fs.existsSync(skillsDir)) {
        const skillDirs = fs.readdirSync(skillsDir, { withFileTypes: true })
          .filter(e => e.isDirectory())

        skillDirs.forEach(skillEntry => {
          const skillPath = path.join(skillsDir, skillEntry.name, 'SKILL.md')
          if (fs.existsSync(skillPath)) {
            skillCount++
          }
        })
      }

      // Compter agents (fichiers .md dans agents/)
      const agentsDir = path.join(rootDir, dir, 'agents')
      let agentCount = 0
      if (fs.existsSync(agentsDir)) {
        const agentFiles = fs.readdirSync(agentsDir, { withFileTypes: true })
          .filter(e => e.isFile() && e.name.endsWith('.md'))
        agentCount = agentFiles.length
      }

      // Compter hooks (fichiers .py dans hooks/, hors utils/ et __pycache__)
      const hooksDir = path.join(rootDir, dir, 'hooks')
      let hookCount = 0
      if (fs.existsSync(hooksDir)) {
        const hookFiles = fs.readdirSync(hooksDir, { withFileTypes: true })
          .filter(e =>
            e.isFile() &&
            e.name.endsWith('.py') &&
            !e.name.startsWith('_') && // Exclure __init__.py, __pycache__
            e.name !== 'utils.py'
          )
        hookCount = hookFiles.length
      }

      // Compter lignes README
      const readmePath = path.join(rootDir, dir, 'README.md')
      const readmeLines = fs.existsSync(readmePath)
        ? fs.readFileSync(readmePath, 'utf-8').split('\n').length
        : 0

      return {
        ...pluginJson,
        skillCount,
        agentCount,
        hookCount,
        readmeLines,
        slug: dir
      }
    })

    // Trier par nom
    return plugins.sort((a, b) => a.name.localeCompare(b.name))
  }
}

export declare const data: PluginMetadata[]

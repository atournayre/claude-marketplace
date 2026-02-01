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

      // Compter lignes README
      const readmePath = path.join(rootDir, dir, 'README.md')
      const readmeLines = fs.existsSync(readmePath)
        ? fs.readFileSync(readmePath, 'utf-8').split('\n').length
        : 0

      return {
        ...pluginJson,
        skillCount,
        readmeLines,
        slug: dir
      }
    })

    // Trier par nom
    return plugins.sort((a, b) => a.name.localeCompare(b.name))
  }
}

export declare const data: PluginMetadata[]

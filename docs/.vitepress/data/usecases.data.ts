import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'
import matter from 'gray-matter'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

export interface UseCaseMetadata {
  title: string
  description: string
  category: string
  plugins: Array<{ name: string; skills: string[] }>
  complexity: number
  duration: number
  keywords: string[]
  related: string[]
  slug: string
  categorySlug: string
}

export default {
  async load(): Promise<UseCaseMetadata[]> {
    const usecasesDir = path.resolve(__dirname, '../../usecases')
    const usecases: UseCaseMetadata[] = []

    // Vérifier que le dossier existe
    if (!fs.existsSync(usecasesDir)) {
      return []
    }

    function walkDir(dir: string, category: string = '') {
      const entries = fs.readdirSync(dir, { withFileTypes: true })

      for (const entry of entries) {
        const fullPath = path.join(dir, entry.name)

        if (entry.isDirectory()) {
          walkDir(fullPath, entry.name)
        } else if (entry.name.endsWith('.md') &&
                   !entry.name.startsWith('index') &&
                   !entry.name.startsWith('by-')) {
          const content = fs.readFileSync(fullPath, 'utf-8')
          const { data } = matter(content)

          usecases.push({
            ...data,
            categorySlug: category,
            slug: entry.name.replace('.md', '')
          } as UseCaseMetadata)
        }
      }
    }

    walkDir(usecasesDir)
    return usecases.sort((a, b) => a.complexity - b.complexity)
  }
}

export declare const data: UseCaseMetadata[]

import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'Claude Plugin Marketplace',
  description: 'Marketplace de plugins pour Claude Code',
  base: '/claude-marketplace/',
  appearance: true,

  head: [
    ['link', { rel: 'icon', href: '/claude-marketplace/favicon.ico' }],

    // Open Graph
    ['meta', { property: 'og:type', content: 'website' }],
    ['meta', { property: 'og:title', content: 'Claude Plugin Marketplace' }],
    ['meta', { property: 'og:description', content: 'Écosystème complet de plugins, skills, agents et hooks pour Claude Code' }],
    ['meta', { property: 'og:url', content: 'https://atournayre.github.io/claude-marketplace/' }],
    ['meta', { property: 'og:image', content: 'https://atournayre.github.io/claude-marketplace/og-image.png' }],
    ['meta', { property: 'og:image:width', content: '1200' }],
    ['meta', { property: 'og:image:height', content: '630' }],
    ['meta', { property: 'og:image:alt', content: 'Claude Plugin Marketplace - Plugins, skills, agents & hooks' }],
    ['meta', { property: 'og:locale', content: 'fr_FR' }],

    // Twitter Card
    ['meta', { name: 'twitter:card', content: 'summary_large_image' }],
    ['meta', { name: 'twitter:title', content: 'Claude Plugin Marketplace' }],
    ['meta', { name: 'twitter:description', content: 'Écosystème complet de plugins, skills, agents et hooks pour Claude Code' }],
    ['meta', { name: 'twitter:image', content: 'https://atournayre.github.io/claude-marketplace/og-image.png' }]
  ],

  themeConfig: {
    logo: {
      light: '/logo-light.svg',
      dark: '/logo-dark.svg'
    },

    nav: [
      { text: 'Guide', link: '/guide/getting-started' },
      { text: 'Plugins', link: '/plugins/' },
      { text: 'Skills', link: '/commands/' },
      { text: 'Use Cases', link: '/usecases/' },
      { text: 'GitHub', link: 'https://github.com/atournayre/claude-marketplace' }
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/atournayre/claude-marketplace' }
    ],

    footer: {
      message: 'Publié sous licence MIT',
      copyright: 'Copyright © 2026 Aurélien Tournayre'
    },

    editLink: {
      pattern: 'https://github.com/atournayre/claude-marketplace/edit/main/docs/:path',
      text: 'Modifier cette page sur GitHub'
    },

    sidebar: {
      '/usecases/': [
        {
          text: 'Vue d\'ensemble',
          items: [
            { text: 'Tous les use cases', link: '/usecases/' },
            { text: 'Par catégorie', link: '/usecases/by-category' },
            { text: 'Par plugin', link: '/usecases/by-plugin' }
          ]
        },
        {
          text: 'Git & Workflow',
          collapsed: false,
          items: [
            { text: 'Créer PR avec QA', link: '/usecases/git-workflow/create-pr-with-qa' },
            { text: 'Corriger review PR', link: '/usecases/git-workflow/fix-pr-comments' },
            { text: 'Résoudre conflits', link: '/usecases/git-workflow/resolve-merge-conflicts' },
            { text: 'Release automation', link: '/usecases/git-workflow/release-automation' }
          ]
        },
        {
          text: 'Development',
          collapsed: false,
          items: [
            { text: 'Workflow complet', link: '/usecases/development/full-feature-workflow' },
            { text: 'Auto depuis issue', link: '/usecases/development/auto-feature-from-issue' },
            { text: 'Code review auto', link: '/usecases/development/code-review-automation' },
            { text: 'PHPStan level 9', link: '/usecases/development/phpstan-error-resolution' }
          ]
        },
        {
          text: 'Framework',
          collapsed: true,
          items: [
            { text: 'Stack entité', link: '/usecases/framework/generate-entity-stack' },
            { text: 'Workflow CQRS', link: '/usecases/framework/create-cqrs-workflow' },
            { text: 'Module DDD', link: '/usecases/framework/setup-ddd-module' }
          ]
        },
        {
          text: 'Testing',
          collapsed: true,
          items: [
            { text: 'Test UI E2E', link: '/usecases/testing/e2e-ui-testing' },
            { text: 'Test responsive', link: '/usecases/testing/responsive-testing' }
          ]
        },
        {
          text: 'Advanced',
          collapsed: true,
          items: [
            { text: 'Multi-plugin', link: '/usecases/advanced/multi-plugin-orchestration' },
            { text: 'Worktrees', link: '/usecases/advanced/worktree-parallel-features' }
          ]
        }
      ],
      '/guide/': [
        {
          text: 'Guide utilisateur',
          items: [
            { text: 'Démarrage rapide', link: '/guide/getting-started' },
            { text: 'Installation', link: '/guide/installation' },
            { text: 'Architecture slash commands', link: '/guide/workaround-slash-commands' }
          ]
        },
        {
          text: 'Contribution',
          items: [
            { text: 'Guide de contribution', link: '/guide/contributing' }
          ]
        }
      ],
      '/plugins/': [
        {
          text: 'Vue d\'ensemble',
          items: [
            { text: 'Tous les plugins', link: '/plugins/' },
            { text: 'Par catégorie', link: '/plugins/by-category' }
          ]
        },
        {
          text: 'Git & Workflow',
          collapsed: false,
          items: [
            { text: 'Git', link: '/plugins/git' },
            { text: 'GitHub', link: '/plugins/github' },
            { text: 'Review', link: '/plugins/review' }
          ]
        },
        {
          text: 'Développement',
          collapsed: false,
          items: [
            { text: 'Dev', link: '/plugins/dev' },
            { text: 'Framework', link: '/plugins/framework' },
            { text: 'QA', link: '/plugins/qa' },
            { text: 'Feature Dev', link: '/plugins/feature-dev' }
          ]
        },
        {
          text: 'Framework',
          collapsed: false,
          items: [
            { text: 'Symfony', link: '/plugins/symfony' }
          ]
        },
        {
          text: 'Documentation',
          collapsed: false,
          items: [
            { text: 'Doc', link: '/plugins/doc' },
            { text: 'Prompt', link: '/plugins/prompt' },
            { text: 'Claude', link: '/plugins/claude' }
          ]
        },
        {
          text: 'IA',
          collapsed: false,
          items: [
            { text: 'Gemini', link: '/plugins/gemini' }
          ]
        },
        {
          text: 'Outils',
          collapsed: false,
          items: [
            { text: 'Customize', link: '/plugins/customize' },
            { text: 'Notifications', link: '/plugins/notifications' },
            { text: 'Chrome UI Test', link: '/plugins/chrome-ui-test' },
            { text: 'Marketing', link: '/plugins/marketing' },
            { text: 'Command', link: '/plugins/command' },
            { text: 'MLVN (AIBlueprint)', link: '/plugins/mlvn' }
          ]
        }
      ]
    },

    search: {
      provider: 'local',
      options: {
        locales: {
          root: {
            translations: {
              button: { buttonText: 'Rechercher' },
              modal: {
                noResultsText: 'Aucun résultat',
                footer: {
                  selectText: 'Sélectionner',
                  navigateText: 'Naviguer'
                }
              }
            }
          }
        }
      }
    }
  }
})

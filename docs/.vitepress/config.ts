import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'Claude Plugin Marketplace',
  description: 'Marketplace de plugins pour Claude Code',
  base: '/claude-marketplace/',
  appearance: true,

  head: [
    ['link', { rel: 'icon', href: '/claude-marketplace/favicon.ico' }],
    ['meta', { property: 'og:title', content: 'Claude Plugin Marketplace' }],
    ['meta', { property: 'og:description', content: '16 plugins pour Claude Code' }]
  ],

  themeConfig: {
    logo: {
      light: '/logo-light.svg',
      dark: '/logo-dark.svg'
    },

    nav: [
      { text: 'Guide', link: '/guide/getting-started' },
      { text: 'Plugins', link: '/plugins/' },
      { text: 'Commandes', link: '/commands/' }
    ],

    sidebar: {
      '/guide/': [
        {
          text: 'Guide',
          items: [
            { text: 'Démarrage rapide', link: '/guide/getting-started' },
            { text: 'Installation', link: '/guide/installation' },
            { text: 'Architecture slash commands', link: '/guide/workaround-slash-commands' }
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
            { text: 'Command', link: '/plugins/command' }
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

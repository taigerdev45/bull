// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  modules: [
    '@vite-pwa/nuxt'
  ],
  pwa: {
    manifest: {
      name: 'Bull ASUR',
      short_name: 'BullASUR',
      description: 'Système de Gestion des Notes et Bulletins Académiques',
      theme_color: '#000000',
      background_color: '#ffffff',
      display: 'standalone',
      orientation: 'portrait',
      icons: [
        {
          src: 'icon.png',
          sizes: '192x192',
          type: 'image/png'
        },
        {
          src: 'icon.png',
          sizes: '512x512',
          type: 'image/png'
        }
      ]
    },
    workbox: {
      navigateFallback: '/',
      globPatterns: ['**/*.{js,css,html,png,svg,ico}']
    },
    client: {
      installPrompt: true,
      periodicSyncForUpdates: 3600,
    },
    devOptions: {
      enabled: true,
      type: 'classic',
    }
  },
  app: {
    head: {
      title: 'Bull ASUR - Excellence Académique',
      meta: [
        { name: 'description', content: 'Modern SaaS platform for academic grading and bulletin generation.' },
        { name: 'theme-color', content: '#000000' }
      ],
      link: [
        { rel: 'icon', type: 'image/png', href: '/icon.png' },
        { rel: 'apple-touch-icon', href: '/icon.png' }
      ]
    }
  },
  css: ['~/assets/css/main.css'],
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'https://bull-api.onrender.com/api'
    }
  },
  vite: {
    optimizeDeps: {
      include: [
        '@vue/devtools-core',
        '@vue/devtools-kit',
      ]
    }
  }
})

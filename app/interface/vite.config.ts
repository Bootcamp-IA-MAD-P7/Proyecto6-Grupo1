import tailwindcss from '@tailwindcss/vite'
import react from '@vitejs/plugin-react'
import path from 'node:path'
import { defineConfig } from 'vite'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  plugins: [
    react(),
    tailwindcss(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['app-mark.svg'],
      manifest: {
        name: 'Complaint Routing Workspace',
        short_name: 'Complaint Routing',
        description: 'Decision-support interface for complaint classification.',
        theme_color: '#102925',
        background_color: '#f4f1e8',
        display: 'standalone',
        start_url: '/',
        scope: '/',
        icons: [
          {
            src: 'app-mark.svg',
            sizes: 'any',
            type: 'image/svg+xml',
            purpose: 'any maskable',
          },
        ],
      },
      // 🔥 CAMBIO 1: Estrategia injectManifest
      strategies: 'injectManifest',

      // 🔥 CAMBIO 2: Ruta al SW personalizado
      srcDir: 'src',
      filename: 'sw.ts',

      // 🔥 CAMBIO 3: Workbox (se mantiene tu lógica)
      workbox: {
        globPatterns: ['**/*.{js,css,html,svg}'],
        navigateFallbackDenylist: [/^\/api\//],
        cleanupOutdatedCaches: true,
      },

      // 🔥 CAMBIO 4: Activar PWA en desarrollo
      devOptions: {
        enabled: true,
        type: 'module',
        navigateFallback: 'index.html',
        suppressWarnings: true,
      },
    }),
  ],
})

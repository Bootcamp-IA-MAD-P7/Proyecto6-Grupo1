import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { QueryProvider } from '@/providers/QueryProvider'
import './index.css'
import App from './App'

const root = document.getElementById('root')

if (!root) {
  throw new Error('Application root is missing.')
}

createRoot(root).render(
  <StrictMode>
    <QueryProvider>
      <App />
    </QueryProvider>
  </StrictMode>,
)

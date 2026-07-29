const narrative = document.querySelector('#narrative')
const count = document.querySelector('#character-count')
const form = document.querySelector('#guidance-form')
const result = document.querySelector('#guidance')
const status = document.querySelector('#form-status')
const helpDialog = document.querySelector('#help-dialog')
const tip = document.querySelector('.tip-card > div')

function updateCount() {
  count.textContent = `${narrative.value.length} caracteres`
}

narrative.addEventListener('input', updateCount)

form.addEventListener('submit', (event) => {
  event.preventDefault()
  if (!narrative.value.trim()) {
    status.textContent = 'Escribe una descripción sintética antes de obtener la orientación de ejemplo.'
    narrative.focus()
    return
  }
  result.hidden = false
  status.textContent = 'Se muestra una orientación mock de demostración. La revisión humana sigue siendo necesaria.'
  result.scrollIntoView({ behavior: 'smooth', block: 'nearest' })
})

document.querySelector('[data-dictation]').addEventListener('click', () => {
  status.textContent = 'El dictado es conceptual en esta propuesta. No se solicita permiso ni se procesa audio.'
})

document.querySelector('[data-reset]').addEventListener('click', () => {
  narrative.value = ''
  updateCount()
  result.hidden = true
  narrative.focus()
  status.textContent = 'La descripción de ejemplo se ha limpiado de esta vista.'
})

document.querySelector('[data-help]').addEventListener('click', () => helpDialog.showModal())
document.querySelector('[data-close-help]').addEventListener('click', () => helpDialog.close())

document.querySelector('[data-tip-toggle]').addEventListener('click', (event) => {
  const expanded = event.currentTarget.getAttribute('aria-expanded') === 'true'
  event.currentTarget.setAttribute('aria-expanded', String(!expanded))
  tip.hidden = expanded
  event.currentTarget.textContent = expanded ? 'Mostrar consejo' : 'Ocultar consejo'
})

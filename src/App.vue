<script setup>
import { onMounted, onUnmounted } from 'vue'
import SexualDelikte from './views/SexualDelikte.vue'

let dot = null

function onMouseMove(e) {
  if (!dot) return
  dot.style.left = `${e.clientX}px`
  dot.style.top = `${e.clientY}px`
}

function handleInteractiveHover(e) {
  if (!dot) return
  dot.classList.add('cursor-white')
}

function handleInteractiveLeave(e) {
  if (!dot) return
  dot.classList.remove('cursor-white')
}

onMounted(() => {
  dot = document.querySelector('.cursor-dot')
  window.addEventListener('mousemove', onMouseMove)

  // Add hover listeners to links, buttons, .info-btn, and .accordion-header
  const interactiveSelectors = ['a', 'button', '.info-btn', '.accordion-header']
  interactiveSelectors.forEach(sel => {
    document.querySelectorAll(sel).forEach(el => {
      el.addEventListener('mouseenter', handleInteractiveHover)
      el.addEventListener('mouseleave', handleInteractiveLeave)
    })
  })
})

onUnmounted(() => {
  window.removeEventListener('mousemove', onMouseMove)

  // Remove hover listeners
  const interactiveSelectors = ['a', 'button', '.info-btn', '.accordion-header']
  interactiveSelectors.forEach(sel => {
    document.querySelectorAll(sel).forEach(el => {
      el.removeEventListener('mouseenter', handleInteractiveHover)
      el.removeEventListener('mouseleave', handleInteractiveLeave)
    })
  })
})
</script>

<template>
  <!-- Custom Cursor Punkt -->
  <div class="cursor-dot"></div>

  <!-- Deine bestehende App -->
  <SexualDelikte />
</template>

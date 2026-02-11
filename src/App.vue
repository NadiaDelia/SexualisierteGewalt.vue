<script setup>
import { onMounted, onUnmounted } from 'vue'
import SexualDelikte from './views/SexualDelikte.vue'

let dot = null

function onMouseMove(e) {
  if (!dot) return
  dot.style.left = `${e.clientX}px`
  dot.style.top = `${e.clientY}px`
}

onMounted(() => {
  dot = document.querySelector('.cursor-dot')
  window.addEventListener('mousemove', onMouseMove)
})

onUnmounted(() => {
  window.removeEventListener('mousemove', onMouseMove)
})
</script>

<template>
  <!-- Custom Cursor Punkt -->
  <div class="cursor-dot"></div>

  <!-- Deine bestehende App -->
  <SexualDelikte />
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

import SexualDelikte from './views/SexualDelikte.vue'
import FooterBrava from './components/FooterBrava.vue'


const showFooter = ref(false)
let dot = null

function onMouseMove(e) {
  if (!dot) return
  dot.style.left = `${e.clientX}px`
  dot.style.top = `${e.clientY}px`
}

function isInteractive(target) {
  // Für Accordion: Nur auf .accordion-header oder .accordion-header * (also auch auf Kind-Elemente wie <span>)
  if (target.closest && target.closest('.accordion-header')) return true;
  return target.matches && (
    target.matches('a, button, .info-btn, .popup-close, .dot-item, .dot')
  );
}

function handleDelegatedHover(e) {
  if (!dot) return
  if (isInteractive(e.target)) {
    dot.classList.add('cursor-white')
  }
}

function handleDelegatedLeave(e) {
  if (!dot) return
  if (isInteractive(e.target)) {
    dot.classList.remove('cursor-white')
  }
}

function removeCursorWhite() {
  if (dot) dot.classList.remove('cursor-white')
}

onMounted(() => {
  dot = document.querySelector('.cursor-dot')
  window.addEventListener('mousemove', onMouseMove)

  // Delegated hover for all interactive elements (works for dynamic elements)
  document.addEventListener('mouseover', handleDelegatedHover)
  document.addEventListener('mouseout', handleDelegatedLeave)

  // Entferne den Hover-State beim Klick auf ein .popup-close
  document.addEventListener('click', function(e) {
    if (e.target && e.target.matches('.popup-close')) {
      removeCursorWhite();
    }
  });

  // Scroll-Event für Footer Sichtbarkeit
  window.addEventListener('scroll', checkScroll)
  checkScroll()
})


onUnmounted(() => {
  window.removeEventListener('mousemove', onMouseMove)
  document.removeEventListener('mouseover', handleDelegatedHover)
  document.removeEventListener('mouseout', handleDelegatedLeave)
  window.removeEventListener('scroll', checkScroll)
})

function checkScroll() {
  const scrollY = window.scrollY || window.pageYOffset;
  const viewportHeight = window.innerHeight;
  const fullHeight = document.documentElement.scrollHeight;
  // Zeige Footer, wenn User fast ganz unten ist (10px Toleranz)
  showFooter.value = scrollY + viewportHeight >= fullHeight - 10;
}
</script>

<template>
  <!-- Custom Cursor Punkt -->
  <div class="cursor-dot"></div>

  <!-- Deine bestehende App -->
  <SexualDelikte />
  <router-view />
  <FooterBrava v-if="showFooter" />
</template>

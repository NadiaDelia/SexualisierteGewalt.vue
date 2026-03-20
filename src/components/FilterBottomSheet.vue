<template>
  <div v-if="show" class="filter-bottom-sheet-overlay" @click.self="$emit('close')">
    <div class="filter-bottom-sheet">
      <slot>Filter-Inhalte hier</slot>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'
const props = defineProps({
  show: Boolean
})
</script>

<style scoped>
.filter-bottom-sheet-overlay {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  top: 0;
  background: rgba(0,0,0,0.4);
  z-index: 30000;
  display: flex;
  align-items: flex-end;
  justify-content: flex-start;
}
.filter-bottom-sheet {
  width: 100vw;
  background: #fff;
  border-top-left-radius: 0px;
  border-top-right-radius: 0px;
  min-height: 120px;
  box-shadow: 0 -2px 16px rgba(0,0,0,0.12);
  padding: 0em 1.5em 0.5em 1.5em;
  margin-bottom: env(safe-area-inset-bottom, 0px);
}
</style>

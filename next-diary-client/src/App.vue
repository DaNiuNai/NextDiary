<template>
  <div class="main-container">
    <h1 class="title">下一个日记 - Next Diary</h1>
    <transition name="fade" mode="out-in">
      <DiaryEditor v-if="currentView === 'editor'" @submitted="handleSubmitted" />
      <DiaryDisplay v-else-if="receivedDiary" :diary="receivedDiary" @new-exchange="resetToEditor" />
    </transition>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import DiaryEditor from './components/DiaryEditor.vue';
import DiaryDisplay from './components/DiaryDisplay.vue';
import type { Diary } from './types';

const currentView = ref<'editor' | 'display'>('editor');
const receivedDiary = ref<Diary | null>(null);

const handleSubmitted = (diary: Diary) => {
  receivedDiary.value = diary;
  currentView.value = 'display';
};

const resetToEditor = () => {
  receivedDiary.value = null;
  currentView.value = 'editor';
};
</script>

<style scoped>
.main-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}
.title {
  font-size: 2.5em;
  color: #303133;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
}
/* 过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>

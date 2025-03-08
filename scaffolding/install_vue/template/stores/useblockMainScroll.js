import { ref } from 'vue';
import { defineStore } from 'pinia';

export const useBlockMainScroll = defineStore('blockMainScroll', () => {
  const isBlockScroll = ref(false);

  function blockScroll() {
    isBlockScroll.value = true;
  }

  const unblockScroll = ()=>{
    isBlockScroll.value = false;
  }

  return { isBlockScroll, blockScroll, unblockScroll };
});
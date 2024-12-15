import { defineStore } from "pinia";
import { computed, ref } from "vue";

export const useOverlay = defineStore('overlay',()=>{
    const toggletOverlay = ref(false)
    
    function showOverlay (){
        toggletOverlay.value = true
    }
    
    function hiddenOverlay (){
        toggletOverlay.value = false
    }

    const watchShowOverlay = computed(()=>{
        return toggletOverlay.value
    })

    return { showOverlay, hiddenOverlay, watchShowOverlay }
})
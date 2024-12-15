<template>
    <div class="w-full mb-2">
        <div>
            <button 
                :class="[
                    bgColor,
                    bgHoverColor,
                    textColor,
                    cursorPoint,
                    'rounded',
                    'w-full',
                    'px-3',
                    'py-2',
                    'font-semibold'
                ]
                "
            >
                {{ textButton }}
            </button>
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue';

    const props = defineProps(
        {
            'textButton':{
                type: String,
                default: 'Button'
            },
            'disable':{
                type: Boolean,
                default: false
            }
        }
    )
    
    const bgColor = computed(()=>{
        return (!props.disable)? 'bg-blue-500' : 'bg-gray-200' 
    })
    const bgHoverColor = computed(()=>{
        return (!props.disable)? 'bg-blue-400' : '' 
    })
    const textColor = computed(()=>{
        return (!props.disable)? 'text-white' : 'text-neutral-400' 
    })
    const cursorPoint = computed(()=>{
        return (!props.disable)? 'pointer-pointer' : 'cursor-not-allowed' 
    })


</script>

<style lang="scss" scoped>

</style>
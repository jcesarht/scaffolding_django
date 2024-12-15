<template>
    <div :class="[
        'px-2',
        'py-2',
        typeInfoSignBackgroundStyle,
        'rounded',
        typeInfoSignBorderStyle,
        'border-2',
        'w-full',
        'relative',
        ]
        "
    >
        <p :class="[
            'text-x',
            'text-center',
            'break-word',
            typeInfoSignTextStyle,
            ]"
        >
            <slot></slot>
        </p>
    </div>
</template>

<script setup>
import { computed, reactive, watchEffect } from 'vue';

    const props = defineProps(
        {
            'typeInfo':'info'
        }
    )
    const style_box_info = reactive({
            "text_style": 'text-blue-500',
            "backgroud_color":  'bg-blue-100',
            "border_color": 'border-blue-500'
        })
    const typeInfoSignBorderStyle = computed(()=>{
        return style_box_info.border_color
    })
    const typeInfoSignTextStyle = computed(()=>{
        return style_box_info.text_style
    })
    const typeInfoSignBackgroundStyle = computed(()=>{
        return style_box_info.background_color
    })
    
    /**
     * Select the box alert style 
     */
    const initStyle = ()=>{
        if(props.typeInfo == 'info'){
            style_box_info.border_color = 'border-blue-500'
            style_box_info.text_style = 'text-blue-500'
            style_box_info.background_color = 'bg-blue-100'
        }
        else if(props.typeInfo == 'alert'){
            style_box_info.border_color = 'border-red-500'
            style_box_info.text_style = 'text-red-500'
            style_box_info.background_color = 'bg-red-100'
        }
        else if(props.typeInfo == 'warning'){
            style_box_info.border_color = 'border-yellow-500'
            style_box_info.text_style = 'text-yellow-500'
            style_box_info.background_color = 'bg-yellow-100'
        }
        else if(props.typeInfo == 'success'){
            style_box_info.border_color = 'border-green-500'
            style_box_info.text_style = 'text-green-500'
            style_box_info.background_color = 'bg-green-100'
        }

    }
    watchEffect(initStyle)

</script>

<style lang="scss" scoped>

</style>,
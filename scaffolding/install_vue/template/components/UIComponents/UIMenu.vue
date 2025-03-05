<template>
    <ul class="mt-1">
        <router-link :to="{name: mod.route}" v-for="mod in modules" :key="`module_${mod.id}`" >
            <div 
                :class="
                [
                    bgColor,
                    bgHoverColor,
                    textColor,
                    cursorPoint,
                    'mb-1',
                    'px-3 py-3',
                    'rounded-md',
                ]"

                @click="emitShowMenu()"
            >
                {{ mod.module_name }} {{ mod.id >= 9 ? '>':''}}
            </div>
        </router-link>
    </ul>
</template>

<script setup>
import { computed, ref } from 'vue';
    const showMenu = ref(false)

    const props = defineProps(
        {
            'disable':{
                type: Boolean,
                default: false
            }
        }
    )
    
    const bgColor = computed(()=>{
        return (!props.disable)? 'bg-blue-50' : 'bg-gray-200' 
    })
    const bgHoverColor = computed(()=>{
        return (!props.disable)? 'hover:bg-blue-300 hover:text-white' : '' 
    })
    const textColor = computed(()=>{
        return (!props.disable)? 'text-blue-500' : 'text-neutral-400' 
    })
    const cursorPoint = computed(()=>{
        return (!props.disable)? 'cursor-pointer' : 'cursor-not-allowed' 
    })
    
    const emit = defineEmits(['hiddeMenu'])
    const modules = computed(()=>{
        return [
            {
                id: 1,
                module_name: 'Dashboard',
                route: 'dashboard'
            }
        ]
    })
    
    const emitShowMenu = ()=>{
        emit('hiddeMenu',false)
    }
</script>
<style lang="scss" scoped>
</style>
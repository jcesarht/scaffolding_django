<template>
    <div class="px-2 py-2 sm:px-4 sm:py-5 bg-blue-200 min-h-full ">
        <div class="min-h-full flex w-full ">
            <div class="hidden sm:block w-1/3 rounded-md shadow-md bg-white p-1 mr-3">
                <div class="flex flex-col min-h-full">
                    <div class="flex justify-center items-center h-20 border-b border-blue-500">
                        <img src="@/assets/vue.svg" alt="logo" />
                    </div>
                    <div class="h-3/4 mt-3">
                        <UIMenu @hiddeMenu="hiddingMenu" />
                    </div>
                    <div class="flex items-end h-24">
                        <UIButton 
                            textButton="Logout" 
                            @click="logoutButton"
                            :disable="disableButton"
                        />
                    </div>
                </div> 
            </div>
            <div class="flex flex-col w-full ">
                <div class="grid grid-cols-2 col-span-12 rounded-md shadow-md bg-white px-4 py-2 sm:py-2 h-16 mb-6">
                    <div class="flex justify-start items-center">
                        <Bars3Icon class="
                            sm:hidden
                            self-center
                            size-8
                            sm:size-9
                            text-blue-500
                            hover:text-blue-900
                            cursor-pointer"
                            @click="showMenu=!showMenu"
                        />
                    </div>
                    <div class="flex justify-end items-center">
                        <div class="flex justify-center items-center w-8 h-8 sm:w-10 sm:h-10 rounded-full border-2 border-blue-300 bg-blue-100">
                            <span class="flex justify-center">
                                <UserIcon class="size-6 text-blue-500 cursor-pointer" />
                            </span>
                        </div>
                    </div>
                </div>
                <div class="rounded-md shadow-md bg-white flex-1 px-3 py-3 h-full">
                    <router-view></router-view>
                </div>
            </div>
        </div>
        <!-- overlay mobile menu-->
        <div>
            <div v-if="showMobileMenu">
                <div class="absolute top-0 left-0 w-full min-h-full  bg-black bg-opacity-50 z-10"  @click="showMenu=false">
                    <div
                        :class="[
                            'relative',
                            'top-0',
                            'w-3/4',
                            '-translate-x-full',
                            'p-1',
                            'h-full',
                            'rounded-r-md',
                            'shadow-md',
                            'bg-white',
                            activate ? 'active' : ''
                        ]"
                        @click.stop
                    >
                        <div class="flex flex-col h-screen ">
                            <div class="hidden xs:flex justify-center items-center py-6 sm:py-2 max-h-20 sm:h-16">
                                <img src="@/assets/vue.svg" alt="logo" />
                            </div>
                            <div class="overflow-y-auto">
                                <div>
                                    <UIMenu @hiddeMenu="hiddingMenu" />
                                </div>
                                <div class="flex items-end h-14">
                                    <UIButton 
                                        textButton="Logout" 
                                        @click="logoutButton"
                                        :disable="disableButton"
                                    />
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
    //import basic library
    import { ref, computed } from 'vue';
    import { useRouter } from 'vue-router';
    //import components
    import { UserIcon, Bars3Icon } from '@heroicons/vue/24/solid'
    import UIButton from '@/components/UIComponents/UIButton.vue'
    import UIMenu from '@/components/UIComponents/UIMenu.vue';
    //import stores
    import {useLoginUserStore} from '@/module/loginUser/stores/useLoginUserStore';
    import { useBlockMainScroll } from '@/stores/useblockMainScroll';
    
    const disableButton = ref(false)
    const showMenu = ref(false)
    const activate = ref(true)
    const router = useRouter()
    
    const {isAuthenticated, logoutAction, userData} = useLoginUserStore()
    
    //The store is called for blocking the main scroll
    const blockingMainScroll = useBlockMainScroll();
    const {blockScroll, unblockScroll } = blockingMainScroll;
    /**
     * show and hide mobile menu
     */
    const showMobileMenu = computed(()=>{
        menuEffectDelay();
        showMenu.value ? blockScroll() : unblockScroll();
        return showMenu.value
    })
    
    const menuEffectDelay = ()=>{
        setTimeout(()=>{
            activate.value = !activate.value
        }, 50);
    }

    const logoutButton = ()=>{
        if(!disableButton.value){
            logoutAction()
            router.push({name: 'login'})
        }
    }

    //hidde the menu from click on tab of the menu
    const hiddingMenu = ()=>{
        showMenu.value = false
        unblockScroll()
    }

</script>

<style scoped>
    .active {
        @apply transition translate-x-0 duration-300 ;
    }

</style>
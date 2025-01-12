<template>
    <div>
        <p>Hello {{ userData.firstName }}</p>
        This is a Dashboard 
        <UIButton textButton="Logout" @click="logoutButton"/>
    </div>
</template>

<script setup>
    import { useRouter } from 'vue-router';
    import UIButton from '@/components/UIComponents/UIButton.vue'
    import {useLoginUserStore} from '@/module/loginUser/stores/useLoginUserStore';

    const router = useRouter()
    const {isAuthenticated, logoutAction, userData} = useLoginUserStore()

    const logoutButton = ()=>{
        logoutAction()
        router.push({name: 'login'})
    }
</script>

<style lang="scss" scoped>

</style>
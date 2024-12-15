<template>
    <div class="bg-gradient-to-b from-blue-200 h-dvh w-dvw flex items-center justify-center">
        <div class="w-11/12 sm:w-5/12 lg:w-4/12 items-center py-10 px-3 sm:px-6 sm:mt-2">
            <div class="w-full mb-2 px-1">
                <p>Please enter the email associated with your account</p>
            </div>
            <div class="w-full mb-2">
                <base-info-sign typeInfo="alert" v-show="showSign">
                    {{ errorMessage }}  
                </base-info-sign>
            </div>
            <form novalidate @submit.prevent="checkRecoveryForm()" >
                <UIInputText 
                    placeholder="Email"
                    rule="email"
                    name="email"
                    required="true"
                    ref="inputEmailUser"
                />
                <UIButton 
                    textButton="Recovery Password"
                    ref="buttonLogin"
                    :disable="disableButton"
                />
            </form>
            <div class="w-full mt-9">
                <div class="float float-left">
                    <router-link :to="{name: 'login' }">Back to Login</router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
    import { ref } from 'vue';
    import UIInputText from '@/components/UIComponents/UIInputText.vue';
    import UIButton from '@/components/UIComponents/UIButton.vue';
    import baseInfoSign from '@/components/base/baseInfoSign.vue';
    import { useOverlay } from '@/stores/useOverlay';

    const showSign = ref(false)
    const errorMessage = ref(false)
    const disableButton = ref(false)
    const inputEmailUser = ref(null)
    const overlay = useOverlay()

    const { showOverlay, hiddenOverlay } = overlay

    const checkRecoveryForm = async ()=>{
        if(!disableButton.value){
            showSign.value = false
            errorMessage.value = ''
            disableButton.value = true

            if (
                !inputEmailUser.value.checkValidateError()
            ){
                showOverlay()
                
            }
            hiddenOverlay()
            disableButton.value = false       
        }
    }
</script>

<style lang="scss" scoped>

</style>
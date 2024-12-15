<template>
    <div class="bg-gradient-to-b from-blue-200 h-dvh w-dvw flex items-center justify-center">
        <div class="w-11/12 sm:w-5/12 lg:w-4/12 items-center py-10 px-3 text-center">
            <p class="font-bold text-lg">Error</p>
            <p class="italic text-9xl">404</p>
            <p class="font-bold text-lg mb-6">page not found</p>
            <UIButton textButton="Back" @click="$router.back()" />
       </div>
    </div>
</template>
<script setup>
    import UIButton from '@/components/UIComponents/UIButton.vue';
</script>

<style lang="scss" scoped>

</style>
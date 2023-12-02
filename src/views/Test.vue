<template>
    <div>
        <button @click="showNotification">顯示通知</button>
        <div v-if="notificationVisible" class="notification">{{ notificationMessage }}</div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            notificationVisible: false,
            notificationMessage: ''
        }
    },
    methods: {
        showNotification() {
            this.notificationMessage = '這是一條通知消息'
            this.notificationVisible = true

            // 設定一定時間後自動隱藏通知
            setTimeout(() => {
                this.notificationVisible = false
            }, 3000) // 這裡的3000表示通知顯示3秒後自動隱藏
        }
    }
}
</script>

<style scoped>
.notification {
    position: fixed;
    top: 0;
    left: 50%;
    transform: translateX(-50%);
    background-color: #4caf50;
    color: white;
    padding: 15px;
    border-radius: 5px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: opacity 0.5s ease-in-out;
}
</style>

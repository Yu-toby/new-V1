<template>
    <div>
        <n-date-picker v-model:value="timestamp" type="date" />
        <pre>{{timestamp}}</pre>
    </div>
</template>

<script>
import { ref } from 'vue'

export default {
    data() {
        const timestamp = ref(118313526e4)
        return {
            timestamp
        }
    }
}
</script>

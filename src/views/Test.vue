<template>
    <n-date-picker v-model:value="range" type="daterange" clearable @click="formattedRange"/>
    <!-- <pre>{{ formattedRange }}</pre> -->
    <p>{{ date_start }}</p>
    <p>{{ date_end }}</p>
</template>

<script>
import { ref } from 'vue'

export default {
    data() {
        return {
            range: ref([Date.now(), Date.now()]),
            date_start: Date.now(),
            date_end: Date.now(),
        }
    },
    mounted() {
        this.date_start = this.formatDate(this.range[0])
        this.date_end = this.formatDate(this.range[1])
    },
    computed: {
        formattedRange() {
            // 使用Date物件格式化選擇的日期區間
            if (this.range.length === 2) {
                this.date_start = this.formatDate(this.range[0])
                this.date_end = this.formatDate(this.range[1])
                return `${this.date_start} 至 ${this.date_end}`
            } else {
                return '未選擇日期區間'
            }
        }
    },
    methods: {
        formatDate(timestamp) {
            const dateObject = new Date(timestamp)
            const year = dateObject.getFullYear()
            const month = (dateObject.getMonth() + 1).toString().padStart(2, '0')
            const day = dateObject.getDate().toString().padStart(2, '0')
            return `${year}${month}${day}`
        }
    }
}
</script>
<template>
    <div class="con">
        <p class="word">最小溫度</p>
        <div class="bar" :style="{ height: barHeight, backgroundColor: tbcolor }">
            <div class="pointer" :style="{ top: pointerPosition + '%' }"></div>
        </div>
        <p class="word">最大溫度</p>
    </div>

    <!-- <input v-model="point" type="number" min="0" max="100" @input="updatePointerPosition" /> -->
</template>
    
    <script>
import { ref } from 'vue'

export default {
    data() {
        return {
            point: 0,
            device_temperature: 176,
            interval_min_template: 150,
            interval_max_template: 180
        }
    },
    mounted() {
        this.calculatePointerPosition()
    },
    computed: {
        pointerPosition() {
            return this.point
        },
        barHeight() {
            return this.interval_max_template - this.interval_min_template
        }
    },
    methods: {
        calculatePointerPosition() {
            const pt =
                ((this.device_temperature - this.interval_min_template) /
                    (this.interval_max_template - this.interval_min_template)) *
                100
            this.point = pt
        }
    }
}
</script>
    
    <style scoped>
.con {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
    width: 50px;
    height: 300px;
}
.bar {
    position: relative;
    display: flex;
    flex-direction: column;
    width: 20px;
    height: 300px;
    border: 1px solid #000000;
    background-color: #1a18183a;
}
.pointer {
    position: absolute;
    width: 100%;
    height: 4px;
    background-color: rgb(0, 0, 0);
    border-radius: 5px;
    z-index: 20;
}
.word {
    margin: 0;
    font-size: 12px;
    font-weight: bold;
}
</style>
    
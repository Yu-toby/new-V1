<template>
    <div class="con">
        <p class="word">{{interval_min_template}}℃</p>
        <div class="bar" :style="{ backgroundColor: tbcolor }">
            <div class="pointer" :style="{ top: pointer + '%' }"></div>
        </div>
        <p class="word">{{interval_max_template}}℃</p>
    </div>
</template>
    
    <script>
export default {
    props: {
        tbcolor: {
            type: String,
            default: ''
        },
        interval_min_template: {
            type: Number,
        },
        interval_max_template: {
            type: Number,
        },
        barHeight: {
            type: Number,
        },
        pointer: {
            type: Number,
        }
    },
}
</script>
    
    <style scoped>
.con {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
    width: 60px;
    height: 400px;
}
.bar {
    position: relative;
    display: flex;
    flex-direction: column;
    width: 20px;
    height: 400px;
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
    font-size: 15px;
    font-weight: bold;
}
</style>
    
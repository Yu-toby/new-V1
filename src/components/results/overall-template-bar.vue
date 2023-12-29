<template>
    <div class="con">
        <p class="word">0℃</p>
        <div class="bar">
            <div class="normal" :style="{ height: normal_height + '%' }"></div>
            <div class="notice" :style="{ height: notice_height + '%' }"></div>
            <div class="abnormal" :style="{ height: abnormal_height + '%' }"></div>
            <div class="danger" :style="{ height: danger_height + '%' }"></div>
            <div class="pointer" :style="{ top: pointer + '%' }"></div>
        </div>
        <p class="word">{{overall_max_template}}℃</p>
    </div>
</template>
      
<script>
export default {
    props: {
        overall_max_template: {
            type: Number
        },
        pointer: {
            type: Number
        },
        normal_height: {
            type: Number
        },
        notice_height: {
            type: Number
        },
        abnormal_height: {
            type: Number
        },
        danger_height: {
            type: Number
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

.normal {
    width: 100%;
    /* height: 25%; */
    background-color: rgb(118, 181, 75);
}

.notice {
    width: 100%;
    /* height: 25%; */
    background-color: rgb(255, 195, 1);
}

.abnormal {
    width: 100%;
    /* height: 25%; */
    background-color: rgb(234, 108, 22);
}

.danger {
    width: 100%;
    /* height: 25%; */
    background-color: rgb(234, 42, 22);
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
      
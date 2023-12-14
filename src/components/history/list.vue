<template>
    <div>
        <div class="his_list">
            <span id="img_name">{{ getImageName() }}</span>
            <span id="date">{{ date }}</span>
            <span id="equipment_name">{{ equipment_name }}</span>
            <span id="state">{{ state }}</span>
            <span id="tmp_max">{{ tmp_max }}</span>
            <span id="tmp_avg">{{ tmp_avg }}</span>
            <span id="tmp_min">{{ tmp_min }}</span>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        original_image: {
            type: String,
            default: ''
        },
        date: {
            type: String,
            default: ''
        },
        equipment_name: {
            type: String,
            default: ''
        },
        state: {
            type: String,
            default: ''
        },
        tmp_max: {
            type: String,
            default: ''
        },
        tmp_avg: {
            type: String,
            default: ''
        },
        tmp_min: {
            type: String,
            default: ''
        }

    },
    methods: {
        getImageName() {
            // 從 src 中獲取文件名稱
            const fileName = this.original_image.split('\\').pop()
            return fileName
        }
    }
}
</script>

<style scoped>
.his_list {
    /* background-color: rgb(209, 129, 32); */
    display: grid;
    grid-template-columns: 2fr 2fr 1.5fr 1.5fr 1fr 1fr 1fr;
    border-bottom: 2px solid rgba(0, 0, 0, 0.623);
}

.his_list span {
    /* border: 2px solid black; */
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    width: 100%;
    font-size: 20px;
    /* color: white; */
}
</style>
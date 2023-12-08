<template>
    <div>
        <div class="small-picture">
            <img class="picture" :src="src" alt="資訊錯誤" loading="lazy" />
        </div>
            <p class="image_name">{{ getImageName() }}</p>
    </div>
    
</template>
<script>
export default {
    props: {
        src: {
            type: String,
            default: ''
        },
        original_image: {
            type: String,
            default: ''
        }
    },
    methods: {
        getImageName() {
            // 從 src 中獲取文件名稱
            const fileName = this.original_image.split('\\').pop();
            return fileName;
        }
    }
}
</script>
<style >
.small-picture {
    overflow: hidden;
    padding: 5px;
    display: flex;
    justify-content: center;
    align-items: center;
    align-content: center;
    flex-direction: column;
    width: 100%;
    height: calc((100vh - 90px - 80px - 43px - 101px)/3);    /* 90px: navbar, 80px: optionsbar, 43px: tab, 37px: page */
}

.small-picture img {
    max-width: 100%;
    max-height: 100%;
    object-fit: cover;
}

.image_name {
    font-size: 13.5px;
    color: #000000;
    margin: 0;
    padding: 0;
    text-align: center;
    width: 100%;
    height: 20px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.small-picture img:hover {
    /* transform: scale(1.1, 1); */
    box-shadow: 8px 5px 8px #888888;
}
</style>
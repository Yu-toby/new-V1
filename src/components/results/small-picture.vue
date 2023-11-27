<template>
    <div class="small-picture">
        <img class="picture" :src="src" alt="資訊錯誤" loading="lazy" />
    </div>
</template>
<script>
export default {
    props: {
        src: {
            type: String,
            default: ''
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
    width: 100%;
    height: calc((100vh - 90px - 80px - 43px - 45px)/3);    /* 90px: navbar, 80px: optionsbar, 43px: tab, 37px: page */
}

.small-picture img {
    max-width: 100%;
    max-height: 100%;
    object-fit: cover;
}

.small-picture img:hover {
    /* transform: scale(1.1, 1); */
    box-shadow: 8px 5px 8px #888888;
}
</style>
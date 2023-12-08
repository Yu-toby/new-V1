<template>
  <div>
    <img :src="currentImage" alt="動態圖片" />
    <button @click="toggleImage">切換圖片</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      images: [],
      currentImageIndex: 0
    };
  },
  computed: {
    currentImage() {
      this.images = [
        'https://fakeimg.pl/250x100/',
        'https://fakeimg.pl/250x200/'
      ]
      return this.images[this.currentImageIndex];
    }
  },
  methods: {
    toggleImage() {
      // 在兩張圖片之間切換
      this.currentImageIndex = 1 - this.currentImageIndex;
    }
  }
};
</script>

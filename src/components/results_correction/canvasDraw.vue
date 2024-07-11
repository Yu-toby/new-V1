<template>
    <div>
      <canvas
        ref="canvas"
        @mousedown="startDrawing"
        @mousemove="draw"
        @mouseup="stopDrawing"
        @mouseleave="stopDrawing"
        width="640"
        height="480"
        style="border:1px solid #000000;">
      </canvas>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  
  export default {
    name: 'CanvasDraw',
    setup() {
      const canvas = ref(null);
      let ctx = null;
      let isDrawing = false;
      let startX = 0;
      let startY = 0;
  
      const startDrawing = (event) => {
        isDrawing = true;
        const rect = canvas.value.getBoundingClientRect();
        startX = event.clientX - rect.left;
        startY = event.clientY - rect.top;
        ctx.beginPath();
        ctx.moveTo(startX, startY);
      };
  
      const draw = (event) => {
        if (!isDrawing) return;
        const rect = canvas.value.getBoundingClientRect();
        const currentX = event.clientX - rect.left;
        const currentY = event.clientY - rect.top;
        ctx.clearRect(0, 0, canvas.value.width, canvas.value.height);
        ctx.beginPath();
        ctx.rect(startX, startY, currentX - startX, currentY - startY);
        ctx.stroke();
      };
  
      const stopDrawing = () => {
        if (!isDrawing) return;
        isDrawing = false;
      };
  
      onMounted(() => {
        ctx = canvas.value.getContext('2d');
      });
  
      return {
        canvas,
        startDrawing,
        draw,
        stopDrawing
      };
    }
  };
  </script>
  
  <style scoped>
  canvas {
    border: 1px solid #000;
  }
  </style>
  
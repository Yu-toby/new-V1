<template>
  <div>
      <div class="his_list">
          <span id="img_name">
            0{{ getImageName() }}
          </span>
          <span id="date">
            1{{ describe?.time }}
          </span>
          <span id="equipment_name">
            2{{ describe?.category  }}
          </span>
          <span id="state">
            3{{ describe?.result }}
          </span>
          <span id="tmp_max">
            4{{ describe?.max }}
          </span>
          <span id="tmp_avg">
            5{{ describe?.avg }}
          </span>
          <span id="tmp_min">
            6{{ describe?.min }}
          </span>
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
      describe: {
            type: Object,
            default: () => ({})
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
  background-color: rgb(209, 129, 32);
  display: grid;
  grid-template-columns: 2fr 2fr 1.5fr 1.5fr 1fr 1fr 1fr;
  
}

.his_list span {
  border: 2px solid black;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  width: 100%;
  font-size: 20px;
  color: white;
}
</style>
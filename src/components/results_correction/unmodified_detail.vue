<script setup>
import { ElMessage } from 'element-plus'
import 'element-plus/es/components/message/style/css'
</script>

<template>
    <div id="modal0">
        <div class="modal-content0">
            <div id="content_header">
                <p id="header_text">圖片名稱：{{ getImageName() }}</p>
            </div>
            <div id="content_body">
                <div class="show_img" ref="showImg">
                    <div class="img_frame">
                        <img :src="src" loading="lazy" ref="image">
                        <canvas ref="canvas" class="canvas"></canvas>
                    </div>
                </div>
                <div class="operating_area">
                    <div class="config_table">
                        <el-table :data="tableData" style="width: 100%" height="calc(85dvb - 350px)">
                            <el-table-column prop="number_id" align="center" label="編號" width="100" />
                            <el-table-column prop="name" align="center" label="名稱">
                                <template #default="scope">
                                    <el-select v-model="scope.row.device_name" placeholder="Select" style="width: 340px">
                                        <el-option
                                            v-for="item in device_name_list"
                                            :key="item.value"
                                            :label="item.label"
                                            :value="item.value"
                                        />
                                        <div class="add_option_btn">
                                            <el-button v-if="!isAdding" text bg size="small" @click="onAddOption">
                                                Add an option
                                            </el-button>
                                            <template v-else>
                                                <el-input
                                                    v-model="device_option_name"
                                                    class="option-input"
                                                    placeholder="input option name"
                                                    size="small"
                                                />
                                                <el-button type="primary" size="small" @click="Confirm_add_device_name">confirm</el-button>
                                                <el-button size="small" @click="cancel_add_device_name">cancel</el-button>
                                            </template>
                                        </div>
                                    </el-select>
                                </template>
                            </el-table-column>
                            <el-table-column fixed="right" align="center" width="120">
                                <template #default="scope">
                                    <el-button
                                        link
                                        type="primary"
                                        size="small"
                                        @click.prevent="deleteRow(scope.$index)"
                                    >Remove</el-button>
                                </template>
                            </el-table-column>
                        </el-table>
                        <el-button class="mt-4" style="width: 100%" @click="onAddItem">Add Item</el-button>
                    </div>
                </div>
            </div>
            <div id="content_bottom">
                <button class="cancel_btn" @click="cancel">取消修改</button>
                <button class="save_btn" @click="save">儲存修改</button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        src: {
            type: String,
            required: ''
        },
        details: {
            type: Object,
            default: () => ({})
        }
    },
    data() {
        return {
            // 純功能操作==========================================================================
            tableData: [],
            device_name_list: [
                { value: '電阻', label: '電阻' },
                { value: '風扇', label: '風扇' },
                { value: '馬達', label: '馬達' },
                { value: '表頭', label: '表頭' },
                { value: 'PVC電纜', label: 'PVC電纜' },
                { value: '指示燈', label: '指示燈' },
                { value: '變壓器', label: '變壓器' },
                { value: '斷路器', label: '斷路器' },
                { value: '電容', label: '電容' },
                { value: '繼電器', label: '繼電器' },
                { value: '電磁接觸器', label: '電磁接觸器' },
                { value: '熔絲', label: '熔絲' },
            ],
            device_option_name: '',
            isAdding: false,
            item_number: 1, // 用於生成Item的唯一編號
            currentIndex: -1, // 用於保存當前繪製的矩形框索引

            rectangles: [], // 用於存儲矩形框的數據
            drawing: false,
            startX: 0,
            startY: 0,
            currentRect: null

            // 資料回傳後==========================================================================
        }
    },
    watch: {
        details: {
            // 監聽describe的變化
            handler() {
                // 當describe有變化時，執行以下function
                this.initializeTableData()
            },
            deep: true
        }
    },
    mounted() {
        this.canvas = this.$refs.canvas
        this.ctx = this.canvas.getContext('2d')
        window.addEventListener('resize', this.updateCanvasSize)
        // 確保在圖片加載後更新畫布尺寸和矩形框
        this.initializeTableData()
    },
    methods: {
        cancel() {
            this.$emit('close')
        },
        save() {
            // 檢查是否有不完整的項目
            for (const item of this.tableData) {
                if (
                    !item.device_name ||
                    item.startX === null ||
                    item.startY === null ||
                    item.endX === null ||
                    item.endY === null
                ) {
                    ElMessage.error('請確認所有項目的名稱皆已填寫，方框皆確實繪製')
                    return
                }
            }

            console.log(this.tableData)

            // 發送過濾後的數據
            this.axios
                .post('/tsmcserver/reviseResult', {
                    result_dataset: this.tableData,
                    image: this.src,
                    original_id: this.details._id
                })
                .then((res) => {
                    console.log(res)
                    this.$emit('save_success')
                    this.$emit('close')
                })
                .catch((err) => {
                    console.log(err)
                })
        },
        getImageName() {
            // 從 src 中獲取文件名稱
            const fileName = this.src.split('\\').pop()
            return fileName
        },
        initializeTableData() {
            if (this.details && this.details.result_dataset) {
                this.details.result_dataset.forEach((item, index) => {
                    this.tableData.push({
                        device_name: item.category || '',
                        number_id: this.item_number++, // 分配唯一編號
                        startX: parseInt(item.coordinate.xmin),
                        startY: parseInt(item.coordinate.ymin),
                        endX: parseInt(item.coordinate.xmax),
                        endY: parseInt(item.coordinate.ymax),
                        isOriginal: true // 標記為原始矩形框
                    })
                    this.rectangles.push({
                        id: this.tableData[index].number_id,
                        x: parseInt(item.coordinate.xmin),
                        y: parseInt(item.coordinate.ymin),
                        width: item.coordinate.xmax - item.coordinate.xmin,
                        height: item.coordinate.ymax - item.coordinate.ymin,
                        isOriginal: true // 標記為原始矩形框
                    })
                })
                this.onImageLoad()
                this.onAddItem()
            }
        },
        // 功能操作區***************************************************************************************
        onAddItem() {
            const item_number = this.item_number++
            this.tableData.push({
                device_name: '',
                number_id: item_number, // 分配唯一編號
                startX: null,
                startY: null,
                endX: null,
                endY: null,
                isOriginal: false // 標記為新繪製的矩形框
            })
            this.rectangles.push({
                id: item_number,
                x: 0,
                y: 0,
                width: 0,
                height: 0,
                isOriginal: false // 標記為新繪製的矩形框
            }) // 初始化矩形框
            this.currentIndex = this.rectangles.length - 1
        },
        deleteRow(index) {
            this.tableData.splice(index, 1)
            this.rectangles.splice(index, 1)
            this.drawRectangles()
            this.currentIndex = this.rectangles.length - 1
        },
        onAddOption() {
            this.isAdding = true
        },
        Confirm_add_device_name() {
            if (this.device_option_name) {
                this.device_name_list.push({
                    value: this.device_option_name,
                    label: this.device_option_name
                })
                this.cancel_add_device_name()
            } else {
                ElMessage.error('選項名稱不能為空')
            }
        },
        cancel_add_device_name() {
            this.device_option_name = ''
            this.isAdding = false
        },
        // 繪製方框==========================================================================
        onImageLoad() {
            console.log('image loaded')
            this.updateCanvasSize()
            this.drawRectangles() // 確保圖片加載後繪製矩形框
            this.canvas.addEventListener('mousedown', this.onMouseDown)
            this.canvas.addEventListener('mousemove', this.onMouseMove)
            this.canvas.addEventListener('mouseup', this.onMouseUp)
        },
        updateCanvasSize() {
            console.log('update canvas size')
            const img = this.$refs.image
            const rect = img.getBoundingClientRect()
            this.canvas.width = img.clientWidth
            this.canvas.height = img.clientHeight
            this.canvas.style.width = `${img.clientWidth}px`
            this.canvas.style.height = `${img.clientHeight}px`
            this.canvas.style.left = rect.left
            this.canvas.style.top = rect.top
        },
        onMouseDown(e) {
            const rect = this.canvas.getBoundingClientRect()
            this.startX = e.clientX - rect.left
            this.startY = e.clientY - rect.top
            this.drawing = true
        },
        onMouseMove(e) {
            if (!this.drawing) return
            const rect = this.canvas.getBoundingClientRect()
            const mouseX = e.clientX - rect.left
            const mouseY = e.clientY - rect.top

            this.currentRect = {
                id: this.rectangles[this.rectangles.length - 1].id,
                x: this.startX,
                y: this.startY,
                width: mouseX - this.startX,
                height: mouseY - this.startY
            }
            this.rectangles[this.rectangles.length - 1] = this.currentRect
            this.drawRectangles()
        },
        onMouseUp(e) {
            if (this.drawing) {
                const rect = this.canvas.getBoundingClientRect()
                const endX = e.clientX - rect.left
                const endY = e.clientY - rect.top

                if (this.currentIndex !== -1) {
                    this.rectangles[this.currentIndex] = {
                        ...this.currentRect,
                        id: this.rectangles[this.currentIndex].id
                    }
                    this.tableData[this.currentIndex].startX = this.startX
                    this.tableData[this.currentIndex].startY = this.startY
                    this.tableData[this.currentIndex].endX = endX
                    this.tableData[this.currentIndex].endY = endY
                }

                this.drawing = false
            }
        },
        drawRectangles() {
            this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height)
            this.drawOriginalRectangles() // 繪製原始方框
            this.drawNewRectangles() // 繪製新方框
        },
        drawNewRectangles() {
            // this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
            this.rectangles.forEach((rect) => {
                if (!rect.isOriginal) {
                    this.ctx.lineWidth = 2
                    this.ctx.strokeStyle = 'red';
                    this.ctx.strokeRect(rect.x, rect.y, rect.width, rect.height);
                    this.ctx.fillStyle = 'black';
                    this.ctx.font = 'bold 20px Arial';
                    this.ctx.fillText(rect.id, rect.x + 2, rect.y + 16);
                }
            })
        },
        drawOriginalRectangles() {
            // this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
            this.rectangles.forEach((rect) => {
                if (rect.isOriginal) {
                    this.ctx.lineWidth = 3
                    this.ctx.strokeStyle = 'rgb(200, 200, 200)';
                    this.ctx.strokeRect(rect.x, rect.y, rect.width, rect.height);
                    this.ctx.fillStyle = 'black';
                    this.ctx.font = 'bold 20px Arial';
                    this.ctx.fillText(rect.id, rect.x + 2, rect.y + 16);
                }
            })
        }
    }
}
</script>

<style>
#modal0 {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.7);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 10;
}
.modal-content0 {
    padding: 0;
    height: 85dvb;
    width: 155dvb;
    background-color: white;
    border: 5px solid rgb(46, 46, 41);
    border-radius: 10px;
    display: grid;
    grid-template-rows: 60px 1fr 60px;
}
#content_header {
    margin: 0;
    display: flex;
    justify-content: center;
    align-items: center;
}
#header_text {
    margin: 0;
    font-size: 26px;
    font-weight: bold;
    display: flex;
    align-items: center;
    justify-content: center;
}
#content_body {
    margin: 0;
    background-color: #d0cece;
    display: grid;
    grid-template-columns: 0.8fr 1fr;
}
.show_img {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    width: 100%;
}
.img_frame {
    position: relative;
    width: 90%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}
.show_img img {
    max-width: 100%;
    max-height: 100%;
    object-fit: cover;
}
.canvas {
    position: absolute;
    width: 100%;
    height: 100%;
}
.operating_area {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    width: 100%;
}
.config_table {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 99%;
    height: 100%;
}
.add_option_btn {
    margin-top: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
}
#content_bottom {
    display: flex;
    justify-content: space-around;
    align-items: center;
}
#content_bottom button {
    font-size: 20px;
    padding: 5px 10px;
    border-radius: 20px;
    border: none;
    font-weight: bold;
}
.cancel_btn {
    background-color: #555454;
    color: white;
}
.save_btn {
    background-color: #1f6db3;
    color: white;
}
</style>

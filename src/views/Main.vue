<script setup>
import SmallPicture from '@/components/results/small-picture.vue'
import Detail from '@/components/results/detail.vue'
import * as XLSX from 'xlsx'
</script>

<template>
    <div class="container2">
        <div class="optionsbar">
            <div class="item" id="display-name">
                <input
                    type="file"
                    id="fileInput"
                    ref="fileInput"
                    multiple
                    accept=".jpg, .jpeg, .png"
                />
                <button
                    @click="uploadFiles"
                    id="uploadButton"
                    type="button"
                    class="btn"
                    :class="{ 'btn-secondary': !loading, 'btn-dark': loading }"
                    :disabled="loading"
                >
                    <span
                        v-if="loading"
                        class="spinner-border spinner-border-sm"
                        role="status"
                        aria-hidden="true"
                    ></span>
                    {{ loading ? '辨識中...' : '上傳' }}
                </button>
                <div id="status"></div>
            </div>
            <div class="dropdown item" id="drop-down-menu">
                <select v-model="selectedOption" @change="getCategories(); updateStatusNumber(); UpdatePageInformation()">
                    <option value disabled selected>請選擇類別</option>
                    <option
                        v-for="(category, index) in categories"
                        :key="index"
                        :value="category"
                    >{{ category }}</option>
                </select>
                <!-- <button
                    class="btn btn-secondary dropdown-toggle"
                    type="button"
                    id="dropdownMenuButton2"
                    data-bs-toggle="dropdown"
                    aria-expanded="false"
                >下拉選單</button>
                <ul class="dropdown-menu dropdown-menu-dark" aria-labelledby="dropdownMenuButton1" >
                    <li v-for="(option, index) in options" :key="index">
                        <a class="dropdown-item" href="#">{{ option }}</a>
                    </li>
                </ul>-->
            </div>
            <div class="item" id="export">
                <button type="button" class="btn btn-secondary" @click="exportExcel">匯出報告</button>
            </div>
        </div>

        <div class="content">
            <div>
                <ul class="nav nav-tabs nav-justified">
                    <li class="nav-item" id="normal" @click="selectedTab = '正常'; UpdatePageInformation()">
                        <a class="nav-link" href="#">
                            正常
                            <span>{{ normal_Number }}</span>
                        </a>
                    </li>
                    <li class="nav-item" id="notice" @click="selectedTab = '注意'; UpdatePageInformation()">
                        <a class="nav-link" href="#">
                            注意
                            <span>{{ notice_Number }}</span>
                        </a>
                    </li>
                    <li class="nav-item" id="abnormal" @click="selectedTab = '異常'; UpdatePageInformation()">
                        <a class="nav-link" href="#">
                            異常
                            <span>{{ abnormal_Number }}</span>
                        </a>
                    </li>
                    <li class="nav-item" id="danger" @click="selectedTab = '危險'; UpdatePageInformation()">
                        <a class="nav-link" href="#">
                            危險
                            <span>{{ danger_Number }}</span>
                        </a>
                    </li>
                </ul>
            </div>

            <div>
                <!-- 正常 -->
                <div class="tab_container" id="nor_con" v-if="selectedTab === '正常'">
                    <div class="img_outside_container" v-if="details && details.length > 0">
                        <div
                            v-for="(details, index) in details"
                            :src="details.image"
                            :key="index"
                            @click="show(index)"
                        >
                            <SmallPicture
                                v-if="details.result === '正常' && details.category === selectedOption && details.time === uploadTime"
                                :src="details.image"
                                loading="lazy"
                            ></SmallPicture>
                        </div>
                    </div>
                    <div class="img_outside_container" v-else></div>  
                    <div class="page">
                        <div class="example-pagination-block">
                            <el-pagination
                                background
                                layout="prev, pager, next"
                                :total="nor_totalPages"
                                :current-page="nor_currentPage"
                                @current-change="nor_handlePageChange"
                            />
                        </div>
                    </div>
                </div>
                <!-- 注意 -->
                <div class="tab_container" id="not_con" v-else-if="selectedTab === '注意'">
                    <div class="img_outside_container" v-if="details && details.length > 0">
                        <div
                            v-for="(details, index) in details"
                            :src="details.image"
                            :key="index"
                            @click="show(index)"
                        >
                            <SmallPicture
                                v-if="details.result === '注意' && details.category === selectedOption && details.time === uploadTime"
                                :src="details.image"
                            ></SmallPicture>
                        </div>
                    </div>
                    <div class="img_outside_container" v-else></div>  
                    <div class="page">
                        <div class="example-pagination-block">
                            <el-pagination
                                background
                                layout="prev, pager, next"
                                :total="not_totalPages"
                                :current-page="not_currentPage"
                                @current-change="not_handlePageChange"
                            />
                        </div>
                    </div>
                </div>
                <!-- 異常 -->
                <div class="tab_container" id="abn_con" v-else-if="selectedTab === '異常'">
                    <div class="img_outside_container" v-if="details && details.length > 0">
                        <div
                            v-for="(details, index) in details"
                            :src="details.image"
                            :key="index"
                            @click="show(index)"
                        >
                            <SmallPicture
                                v-if="details.result === '異常' && details.category === selectedOption && details.time === uploadTime"
                                :src="details.image"
                            ></SmallPicture>
                        </div>
                    </div>
                    <div class="img_outside_container" v-else></div>  
                    <div class="page">
                        <div class="example-pagination-block">
                            <el-pagination
                                background
                                layout="prev, pager, next"
                                :total="abn_totalPages"
                                :current-page="abn_currentPage"
                                @current-change="abn_handlePageChange"
                            />
                        </div>
                    </div>
                </div>
                <!-- 危險 -->
                <div class="tab_container" id="dan_con" v-else-if="selectedTab === '危險'">
                    <div class="img_outside_container" v-if="details && details.length > 0">
                        <div
                            v-for="(details, index) in details"
                            :src="details.image"
                            :key="index"
                            @click="show(index)"
                        >
                            <SmallPicture
                                v-if="details.result === '危險' && details.category === selectedOption && details.time === uploadTime"
                                :src="details.image"
                            ></SmallPicture>
                        </div>
                    </div>
                    <div class="img_outside_container" v-else></div>  
                    <div class="page">
                        <div class="example-pagination-block">
                            <el-pagination
                                background
                                layout="prev, pager, next"
                                :total="dan_totalPages"
                                :current-page="dan_currentPage"
                                @current-change="dan_handlePageChange"
                            />
                        </div>
                    </div>
                </div>
                <!-- 祥細資料 -->
                <div v-if="details && details.length > 0">
                    <Detail
                        :src="details[showIndex].image"
                        :bcolor="details[showIndex].result === '正常' ? 'rgb(226, 245, 215)' : details[showIndex].result === '注意' ? 'rgb(255, 243, 205)' : details[showIndex].result === '異常' ? 'rgb(248, 215, 178)' : 'rgb(245, 215, 215)'"
                        :tbcolor="details[showIndex].result === '正常' ? 'rgb(124, 208, 72)' : details[showIndex].result === '注意' ? 'rgb(255, 200, 25)' : details[showIndex].result === '異常' ? 'rgb(191, 108, 17)' : 'rgb(181, 59, 59)'"
                        :describe="details[showIndex]"
                        v-show="showModal"
                        @close="showModal = false"
                    ></Detail>
                </div>
                <div v-else></div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            selectedTab: '正常',
            normal_Number: 0,
            notice_Number: 0,
            abnormal_Number: 0,
            danger_Number: 0,
            category_total_number: 0,
            showIndex: 0,
            showModal: false,
            options: ['風扇', '電線', '保險絲', '繼電器', '...'],
            details: [{}],
            selectedOption: '', // 下拉選單標題
            categories: [], // 新增用來存放 MongoDB 中的類別選項
            loading: 0,
            uploadTime: '',
            nor_totalPages: 10,
            not_totalPages: 10,
            abn_totalPages: 10,
            dan_totalPages: 10,
            nor_currentPage: 1,
            not_currentPage: 1,
            abn_currentPage: 1,
            dan_currentPage: 1,
        }
    },
    mounted() {
        //獲取時間紀錄
        this.GetTimeRecord()

        //API
        // this.GetToDo()
        // this.intervalId = setInterval(this.GetToDo, 1000)

        // 在 mounted 中加入獲取 MongoDB 類別選項的程式碼
        this.getCategories()

        // 開始定時檢查 if_detect 狀態
        this.startCheckingIfDetect()

        //更四種新狀態數字
        this.updateStatusNumber()

        //更新頁面資訊
        this.UpdatePageInformation()
    },
    beforeUnmount() {
        //API
        clearInterval(this.intervalId)
    },
    methods: {
        show(index) {
            ;(this.showIndex = index), (this.showModal = true)
        },
        GetToDo() {
            this.axios.get('/tsmcserver').then((res) => {
                this.details = res.data
                console.log(this.details)
            })
        },
        // 上傳圖片
        uploadFiles() {
            // 獲取上傳的文件
            const fileInput = this.$refs.fileInput
            const files = fileInput.files

            // 檢查是否選擇了文件
            if (files.length === 0) {
                alert('請選擇要上傳的文件')
                return
            }

            // 使用FormData來構建HTTP POST請求
            const formData = new FormData()

            // 將每個選中的文件添加到FormData中
            for (let i = 0; i < files.length; i++) {
                formData.append('image', files[i])
            }

            // 當上傳過程開始時，將 loading 設置為 true
            this.loading = true
            this.ifDetectStatus = 1

            // 執行上傳操作
            this.axios
                .post('/tsmcserver', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data' // 設定標頭
                    }
                })
                .then((response) => {
                    if (response.data.status === 'success') {
                        // 上傳成功，執行相應操作
                        alert('上傳成功')
                        // 清空選中的文件
                        fileInput.value = ''
                        // 或取時間紀錄
                        this.GetTimeRecord()
                        // 重新獲取數據或執行其他操作
                        // this.GetToDo()
                        //更改if_detect狀態
                        this.toggleIfDetect()
                        // 開始定時檢查 if_detect 狀態
                        this.startCheckingIfDetect()
                    } else {
                        // 上傳失敗，執行相應操作
                        alert('上傳失敗')
                        this.loading = false // 上傳失敗時，重置 loading 為 false
                        this.ifDetectStatus = 0 // 辨識失敗時，重置為未辨識
                    }
                })
                .catch((error) => {
                    // 上傳過程中出現錯誤
                    console.error('上傳過程中出現錯誤：', error)
                    this.loading = false // 出現錯誤時，重置 loading 為 false
                    this.ifDetectStatus = 0 // 辨識失敗時，重置為未辨識
                })
        },
        // 切換 if_detect 狀態
        toggleIfDetect() {
            // 向後端發送POST請求來切換if_detect狀態
            this.axios.post('/tsmcserver/if_detect').then((res) => {
                if (res.data.status === 'success') {
                    // 更新ifDetectStatus以反映新的狀態
                    this.ifDetectStatus = res.data.new_number

                    // // 如果 if_detect 變成 0，則重置 loading 為 false
                    // if (res.data.new_number === 0) {
                    //     this.loading = false;
                    // }
                } else {
                    console.error('if_detect切換失敗')
                }
            })
        },
        // 開始定時檢查 if_detect 狀態
        startCheckingIfDetect() {
            // 設定每秒執行一次 checkIfDetect 方法
            this.ifDetectInterval = setInterval(this.checkIfDetect, 1000)
        },
        // 停止定時檢查 if_detect 狀態
        stopCheckingIfDetect() {
            clearInterval(this.ifDetectInterval)
            this.getCategories()
            this.GetTimeRecord()
            this.updateStatusNumber()
            this.UpdatePageInformation()
        },
        // 向後端發送請求來獲取 if_detect 狀態
        checkIfDetect() {
            this.axios.get('/tsmcserver/if_detect').then((res) => {
                console.log(res.data)
                this.loading = res.data
                if (res.data === 0) {
                    this.stopCheckingIfDetect()
                }
                // if (res.data.status === 'success') {
                //     this.ifDetectStatus = res.data.new_number;
                //     // 如果 if_detect 變成 0，則停止定時檢查
                //     if (res.data.new_number === 0) {
                //         this.stopCheckingIfDetect();
                //         this.loading = false;
                //     }
                // } else {
                //     console.error('if_detect 檢查失敗');
                // }
            })
        },
        //匯出excel檔案
        exportExcel() {
            try {
                const now = new Date()
                const year = now.getFullYear() // 取得年份
                const month = (now.getMonth() + 1).toString().padStart(2, '0') // 取得月份，並補零
                const day = now.getDate().toString().padStart(2, '0') // 取得日期，並補零

                const formattedDate = `${year}${month}${day}` // 格式化日期為 "年-月-日"
                // console.log(this.details)
                //整理資料以符合Excel格式
                const data = [
                    [`${formattedDate} — 台科大JDP Project —紅外線熱影像辨識報告`],
                    ['檔名', '類別', '結果', '最大溫度', '平均溫度', '最小溫度']
                ]
                for (const item of this.details) {
                    const parts = item.original_image.split('\\') // 使用斜杠字符分割 URL
                    const filename = parts[parts.length - 1] // 提取最後一個部分，即文件名
                    data.push([filename, item.category, item.result, item.max, item.avg, item.min])
                }

                // 創建工作簿和工作表
                const ws = XLSX.utils.aoa_to_sheet(data)
                const wb = XLSX.utils.book_new()
                XLSX.utils.book_append_sheet(wb, ws, '資料表')

                // 步驟3: 生成Excel文件\
                const filename = `${formattedDate}_紅外線熱影像辨識報告.xlsx` // 生成檔案名稱
                XLSX.writeFile(wb, filename)
            } catch (error) {
                console.error('匯出至Excel失敗：', error)
            }
        },
        //讀取時間紀錄
        GetTimeRecord() {
            this.axios.get('/tsmcserver/time_record').then((res) => {
                this.uploadTime = res.data
            })
        },
        //更新狀態數字
        updateStatusNumber() {
            // this.normal_Number = this.category_number[this.selectedOption]["正常"];
            // this.notice_Number = this.category_number[this.selectedOption]["注意"];
            // this.abnormal_Number = this.category_number[this.selectedOption]["異常"];
            // this.danger_Number = this.category_number[this.selectedOption]["危險"];
        },
        // 獲取 MongoDB 中的類別選項
        getCategories() {
            this.axios.get('/tsmcserver/categories').then((res) => {
                this.categories = res.data
            })
            this.UpdatePageInformation()
        },
        // 監聽頁碼變化事件
        nor_handlePageChange(newPage) {
            // 將當前頁碼更新為新的頁碼
            this.nor_currentPage = newPage

            // 在這裡可以執行相應的操作，例如獲取新頁碼對應的數據
            this.UpdatePageInformation()
        },
        not_handlePageChange(newPage) {
            // 將當前頁碼更新為新的頁碼
            this.not_currentPage = newPage

            // 在這裡可以執行相應的操作，例如獲取新頁碼對應的數據
            this.UpdatePageInformation()
        },
        abn_handlePageChange(newPage) {
            // 將當前頁碼更新為新的頁碼
            this.abn_currentPage = newPage

            // 在這裡可以執行相應的操作，例如獲取新頁碼對應的數據
            this.UpdatePageInformation()
        },
        dan_handlePageChange(newPage) {
            // 將當前頁碼更新為新的頁碼
            this.dan_currentPage = newPage

            // 在這裡可以執行相應的操作，例如獲取新頁碼對應的數據
            this.UpdatePageInformation()
        },
        UpdatePageInformation() {
            // 在這裡可以發起 API 請求，獲取新頁碼對應的數據
            // 這裡只是一個示例，實際應用中需要根據情況進行相應的處理
            // console.log(this.selectedTab)
            // console.log(this.selectedOption)
            // console.log(this.nor_currentPage)
            // console.log(this.not_currentPage)
            // console.log(this.abn_currentPage)
            // console.log(this.dan_currentPage)
            this.axios.post('/tsmcserver/page_information', {
                result: this.selectedTab,
                category: this.selectedOption,
                nor_currentPage: this.nor_currentPage,
                not_currentPage: this.not_currentPage,
                abn_currentPage: this.abn_currentPage,
                dan_currentPage: this.dan_currentPage
            }).then(response => {
                const { data, category_count } = response.data;     //解構數值

                this.details = data;
                this.category_total_number = category_count[this.selectedOption]["正常"] + category_count[this.selectedOption]["注意"] + category_count[this.selectedOption]["異常"] + category_count[this.selectedOption]["危險"];

                this.normal_Number = category_count[this.selectedOption]["正常"];
                this.notice_Number = category_count[this.selectedOption]["注意"];
                this.abnormal_Number = category_count[this.selectedOption]["異常"];
                this.danger_Number = category_count[this.selectedOption]["危險"];

                this.nor_totalPages = 10*Math.ceil(category_count[this.selectedOption]["正常"] / 18);
                this.not_totalPages = 10*Math.ceil(category_count[this.selectedOption]["注意"] / 18);
                this.abn_totalPages = 10*Math.ceil(category_count[this.selectedOption]["異常"] / 18);
                this.dan_totalPages = 10*Math.ceil(category_count[this.selectedOption]["危險"] / 18);
            }).catch(error => {
                console.log(error);
            });
            this.updateStatusNumber()
        }
    }
}
</script>

<style  scoped>
.container2 {
    margin: 0px;
    padding: 0px;
    display: grid;
    grid-template-rows: 80px 1fr;
}

/* 選項條============================================================= */

.optionsbar {
    display: grid;
    grid-template-columns: 1fr 3.2fr 1.4fr 1fr 0.8fr 1.2fr;
    /* border: 2px solid black; */
}

/* .item {
    border: 1px solid black;
} */

#display-name {
    grid-column: 2;
    display: flex;
    align-items: center;
    justify-content: center;
}

#drop-down-menu {
    grid-column: 4;
    display: flex;
    align-items: center;
    justify-content: center;
}

#export {
    grid-column: 6;
    display: flex;
    align-items: center;
    justify-content: center;
}

/*Tab=============================================================================*/
.content {
    display: grid;
    grid-template-rows: 43px 1fr;
    /* border: 2px solid black; */
}

.nav-item {
    border-top-left-radius: 12px; /* 左上角圓角 */
    border-top-right-radius: 12px; /* 右上角圓角 */
    border-bottom: none;
}

.nav-link,
.nav-link:hover,
.nav-link:active,
.nav-link:focus {
    margin: 0px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: black;
    font-weight: bold;
    font-size: 18px;
    border-top-left-radius: 12px; /* 左上角圓角 */
    border-top-right-radius: 12px; /* 右上角圓角 */
    border-bottom: none;
}

.nav-item#normal {
    background-color: rgb(118, 181, 75);
}

.nav-item#notice {
    background-color: rgb(255, 195, 1);
}

.nav-item#abnormal {
    background-color: rgb(234, 108, 22);
}

.nav-item#danger {
    background-color: rgb(234, 42, 22);
}
/*縮圖區================================================================================ */
.tab_container {
    display: flex;
    flex-direction: column;
}

.img_outside_container {
    flex: 1;
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    grid-template-rows: repeat(3, 1fr);
}
/* .img_container {
    padding: 5px;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: calc((100vh - 90px - 80px - 43px - 45px)/3);  /* 90px: navbar, 80px: optionsbar, 43px: tab, 37px: page 
} */
/* .img_container img {
    max-width: 100%;
    max-height: 100%;
    object-fit: cover;
} */
.page {
    display: flex;
    justify-content: center;
    align-items: flex-end;
}
.example-pagination-block + .example-pagination-block {
    margin-top: 10px;
}
.example-pagination-block .example-demonstration {
    margin-bottom: 16px;
}

#nor_con {
    background-color: rgb(226, 240, 217);
    border: 5px solid rgb(118, 181, 75);
    height: 100%;
}

#not_con {
    background-color: rgb(255, 248, 220);
    border: 5px solid rgb(255, 195, 1);
    height: 100%;
}

#abn_con {
    background-color: rgb(255, 235, 220);
    border: 5px solid rgb(234, 108, 22);
    height: 100%;
}

#dan_con {
    background-color: rgb(255, 220, 220);
    border: 5px solid rgb(234, 42, 22);
    height: 100%;
}
</style>
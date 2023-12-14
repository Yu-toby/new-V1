<script setup>
import HistoryList from '@/components/history/list.vue'
import Detail from '@/components/results/detail.vue'
</script>

<template>
    <div class="container3">
        <!-- 選項條 -->
        <div class="options_bar">
            <div class="date_selection">
                <n-date-picker v-model:value="range" type="daterange" clearable />
                <!-- <pre>{{ JSON.stringify(range) }}</pre> -->
            </div>
            <div class="device_selection">
                <select v-model="selectedOption" @change="getCategories(); updateStatusNumber()">
                    <option value disabled selected>請選擇類別</option>
                    <option
                        v-for="(category, index) in categories"
                        :key="index"
                        :value="category"
                    >{{ category }}</option>
                </select>
            </div>
            <div class="state_selection">
                <select v-model="StateOption" @change="getCategories(); updateStatusNumber()">
                    <option value disabled selected>請選擇狀態</option>
                    <option
                        v-for="(state, index1) in Option"
                        :key="index1"
                        :value="state"
                    >{{ state }}</option>
                </select>
            </div>
            <div class="check_button">
                <el-button round color="#414141" plain>Search</el-button>
            </div>
        </div>

        <div class="content">
            <!-- 歷史資料列表 -->
            <div class="historical_data">
                <div class="list_content">
                    <div class="list_title">
                        <span id="img_name">圖片名稱</span>
                        <span id="date">日期-時間</span>
                        <span id="equipment_name">設備名稱</span>
                        <span id="state">狀態</span>
                        <span id="tmp_max">最大溫度</span>
                        <span id="tmp_avg">平均溫度</span>
                        <span id="tmp_min">最小溫度</span>
                    </div>
                    <div class="history_list" v-if="details && details.length > 0">
                        <div
                            v-for="(details, index) in details"
                            :src="details.thermal"
                            :key="index"
                            @click="show(index)"
                        >
                            <HistoryList
                                v-if="details.result === '正常'"
                                :original_image="details.original_image"
                                :date="details.time"
                                :equipment_name="details.category"
                                :state="details.result"
                                :tmp_max="details.max"
                                :tmp_avg="details.avg"
                                :tmp_min="details.min"
                            ></HistoryList>
                        </div>
                    </div>
                    <!-- 祥細資料 -->
                    <div v-if="details && details.length > 0">
                        <Detail
                            :src="currentImage"
                            :bcolor="details[showIndex].result === '正常' ? 'rgb(226, 245, 215)' : details[showIndex].result === '注意' ? 'rgb(255, 243, 205)' : details[showIndex].result === '異常' ? 'rgb(248, 215, 178)' : 'rgb(245, 215, 215)'"
                            :tbcolor="details[showIndex].result === '正常' ? 'rgb(124, 208, 72)' : details[showIndex].result === '注意' ? 'rgb(255, 200, 25)' : details[showIndex].result === '異常' ? 'rgb(191, 108, 17)' : 'rgb(181, 59, 59)'"
                            :describe="details[showIndex]"
                            v-show="showModal"
                            @close="showModal = false"
                            @change="changeImage"
                        ></Detail>
                    </div>
                    <div v-else></div>
                    <!-- 頁數標籤 -->
            <div class="page_selection">
                <n-pagination
                    v-model:page.sync="page"
                    v-model:page-size.sync="pageSize"
                    :display-order="['quick-jumper', 'pages', 'size-picker']"
                    :page-count="100"
                    show-quick-jumper
                    show-size-picker
                    :page-sizes="pageSizes"
                />
            </div>
                </div>                
            </div>

            
            
        </div>
    </div>
</template>

<script>
import { ref } from 'vue'

export default {
    data() {
        return {
            // timestamp: ref(118313526e4),
            range: ref([118313526e4, Date.now()]),
            selectedOption: '', // 下拉選單標題
            StateOption: '', // 下拉選單標題
            categories: [], // 新增用來存放 MongoDB 中的類別選項
            Option: ['正常', '注意', '異常', '危險'],
            page: ref(1),
            pageSize: ref(20),
            pageSizes: [
                { label: '10 / page', value: 10 },
                { label: '20 / page', value: 20 },
                { label: '30 / page', value: 30 },
                { label: '40 / page', value: 40 }
            ],

            selectedTab:'',

            showIndex: 0,
            showModal: false,

            details: [{}],
                    
            images: [],
            currentImageIndex: 0,
        }
    },
    mounted() {
        //獲取時間紀錄
        this.GetTimeRecord();
        // 在 mounted 中加入獲取 MongoDB 類別選項的程式碼
        this.getCategories();
        //更四種新狀態數字
        // this.updateStatusNumber();
        this.UpdatePageInformation();
    },
    methods: {
        show(index) {
            ;(this.showIndex = index), (this.showModal = true)
        },
        //讀取時間紀錄
        GetTimeRecord() {
            this.axios.get('/tsmcserver/time_record').then((res) => {
                this.uploadTime = res.data
            })
        },
        //更新狀態數字
        updateStatusNumber() {
            this.axios.post('/tsmcserver/status_number',{category: this.selectedOption === '全部' ? '全部' : this.selectedOption})
            .then((res) => {
                this.normal_Number = res.data[this.selectedOption]["正常"];
                this.notice_Number = res.data[this.selectedOption]["注意"];
                this.abnormal_Number = res.data[this.selectedOption]["異常"];
                this.danger_Number = res.data[this.selectedOption]["危險"];
            })
        },
        // 獲取 MongoDB 中的類別選項
        getCategories() {
            this.axios.get('/tsmcserver/categories').then((res) => {
                const all_categories = res.data
                all_categories.unshift('全部')
                this.categories = all_categories
                this.UpdatePageInformation()
                // console.log(this.categories)
            })
            
        },
        UpdatePageInformation() {
            // 在這裡可以發起 API 請求，獲取新頁碼對應的數據
            this.axios.post('/tsmcserver/page_information', {
                result: '正常',
                category: this.selectedOption === '全部' ? '全部' : this.selectedOption,
                nor_currentPage: this.nor_currentPage,
                not_currentPage: this.not_currentPage,
                abn_currentPage: this.abn_currentPage,
                dan_currentPage: this.dan_currentPage
            }).then(response => {
                console.log(response.data);
                const { data, category_count } = response.data;     //解構數值
                

                this.details = data;
                console.log(this.details);
                // this.category_total_number = category_count[this.selectedOption]["正常"] + category_count[this.selectedOption]["注意"] + category_count[this.selectedOption]["異常"] + category_count[this.selectedOption]["危險"];

                // this.nor_totalPages = 10*Math.ceil(category_count[this.selectedOption]["正常"] / 18);
                // this.not_totalPages = 10*Math.ceil(category_count[this.selectedOption]["注意"] / 18);
                // this.abn_totalPages = 10*Math.ceil(category_count[this.selectedOption]["異常"] / 18);
                // this.dan_totalPages = 10*Math.ceil(category_count[this.selectedOption]["危險"] / 18);
            }).catch(error => {
                console.log(error);
            });
        },
        changeImage() {
            // 在兩張圖片之間切換
            this.currentImageIndex = 1 - this.currentImageIndex;
        }
    },
    computed: {
        currentImage() {
            this.images = [
                this.details[this.showIndex].thermal,
                this.details[this.showIndex].visible_light
            ]
            return this.images[this.currentImageIndex];
        }
    }
}
</script>

<style scoped>
.container3 {
    margin: 0px;
    padding: 0px;
    display: grid;
    grid-template-rows: 80px 1fr;
}

/* 選項條============================================================= */

.options_bar {
    display: grid;
    grid-template-columns: 1fr 3fr 1.5fr 1.5fr 1fr 1fr;
    /* border: 2px solid black; */
}

/* .item {
    border: 1px solid black;
} */

.date_selection {
    grid-column: 2;
    display: flex;
    align-items: center;
    justify-content: center;
}

.device_selection {
    grid-column: 3;
    display: flex;
    align-items: center;
    justify-content: center;
}

.state_selection {
    grid-column: 4;
    display: flex;
    align-items: center;
    justify-content: center;
}

.check_button {
    grid-column: 5;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* 歷史資料列表============================================================= */
.content {
    display: grid;
    /* grid-template-rows: 1fr 43px; */
    /* border: 2px solid black; */
}

.historical_data {
    display: grid;
    grid-template-columns: 0.5fr 3fr 0.5fr;
}

.list_content {
    grid-column: 2;
    display: flex;
    flex-direction: column;
    align-items: center;
    background-color: rgba(204, 204, 204, 0.74);
}

.list_title {
    width: 100%;
    height: 43px;
    background-color: rgb(26, 26, 26);
    /* font-size: 20px; */
    /* color: white; */
    display: grid;
    grid-template-columns: 2fr 2fr 1.5fr 1.5fr 1fr 1fr 1fr;
}

.list_title span {
    /* border: 2px solid black; */
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    width: 100%;
    font-size: 20px;
    color: rgb(255, 255, 255);
}

.history_list {
    width: 100%;
    height:100%;
    grid-gap: 10px;
    padding-top: 10px;
    overflow-y: scroll;
    overflow: hidden;
}

/* 頁數標籤=============================================================== */
.page_selection {
    display: flex;
    justify-content: center;
    align-items: flex-end;
    /* background-color: rgba(204, 204, 204, 0.74); */
}
</style>

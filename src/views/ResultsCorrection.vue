<script setup>
import SmallPicture from '@/components/results/small-picture.vue'
import Detail from '@/components/results_correction/result_correction.vue'
</script>

<template>
    <div class="container5">
        <el-tabs v-model="activeName" class="demo-tabs custom-tab-label">
            <!-- 未修改 -->
            <el-tab-pane label="未修改" name="first" style="">
                <div class="tab_body">
                    <div class="options">
                        <div class="switch_btn">
                            <el-switch
                                v-model="if_mark"
                                class="ml-2"
                                inline-prompt
                                style="--el-switch-on-color: #13ce66; --el-switch-off-color: #bfbfbf"
                                active-text="Y"
                                inactive-text="N"
                                @click="check_mark"
                            />
                            <span> 已標記紀錄</span>
                        </div>
                        <div class="search">
                            <el-input
                                v-model="unmodified_img_name_search"
                                style="width: 240px"
                                placeholder="請輸入照片名稱"
                                clearable
                                @clear="img_name_search = ''"
                            />
                            <button class="search_btn" @click="UnmodifiedSearch">搜尋</button>
                        </div>
                    </div>
                    <div class="content">
                        <div class="img_outside_container" v-if="details && details.length > 0">
                            <div
                                v-for="(detail, index) in details"
                                :src="detail.image_path"
                                :key="index"
                                @click="show(index)"
                            >
                                <SmallPicture
                                    v-if="detail.time === uploadTime"
                                    :src="detail.image_path"
                                    :original_image="detail.image_path"
                                ></SmallPicture>
                            </div>
                        </div>
                    </div>
                    <div class="page_selection">
                        <el-pagination
                            v-model:current-page="unmodified_currentPage"
                            background
                            layout="prev, pager, next, jumper"
                            :total="unmodified_totalPage"
                            @current-change="UnmodifiedCurrentChange"
                        />
                    </div>
                </div>                
            </el-tab-pane>
            <!-- 未學習的設備 -->
            <el-tab-pane label="未學習的設備" name="second">
                <div class="tab_body">
                    <div class="options">
                        <div class="search" style="grid-column: 2">
                            <el-input
                                v-model="not_studied_img_name_search"
                                style="width: 240px"
                                placeholder="請輸入照片名稱"
                                clearable
                                @clear="img_name_search = ''"
                            />
                            <button class="search_btn" @click="NotStudiedSearch">搜尋</button>
                        </div>
                    </div>
                    <div class="content">
                        123
                    </div>
                    <div class="page_selection">
                        <el-pagination
                            v-model:current-page="not_studied_currentPage"
                            background
                            layout="prev, pager, next, jumper"
                            :total="not_studied_totalPage"
                            @current-change="Not_studied_CurrentChange"
                        />
                    </div>
                </div>
            </el-tab-pane>
            <!-- 已修改 -->
            <el-tab-pane label="已修改" name="third">
                <div class="tab_body">
                    <div class="options">
                        <div class="search" style="grid-column: 2">
                            <el-input
                                v-model="already_edited_img_name_search"
                                style="width: 240px"
                                placeholder="請輸入照片名稱"
                                clearable
                                @clear="img_name_search = ''"
                            />
                            <button class="search_btn" @click="AlreadyEditedSearch">搜尋</button>
                        </div>
                        <div class="update_result">
                            <button class="update_result_btn" @click="update_result">上傳修正結果</button>
                        </div>
                    </div>
                    <div class="content">
                        123
                    </div>
                    <div class="page_selection">
                        <el-pagination
                            v-model:current-page="already_edited_currentPage"
                            background
                            layout="prev, pager, next, jumper"
                            :total="already_edited_totalPage"
                            @current-change="Already_edited_CurrentChange"
                        />
                    </div>
                </div>
            </el-tab-pane>
            <!-- 詳細資料 -->
            <div v-if="showModal && details && details.length > 0">
                <Detail 
                    :src="details[this.showIndex].image_path"
                    :details="details[this.showIndex]"
                    v-show="showModal"
                    @close="showModal = false"
                    ></Detail>
            </div>
        </el-tabs>
    </div>
</template>

<script>
export default {
    data() {
        return {
            activeName: 'first',
            showIndex: 0,
            showModal: false,
            // 未修改----------------------------------------------
            if_mark: false,
            unmodified_img_name_search: '',
            unmodified_currentPage: 1,
            unmodified_totalPage: 20,

            uploadTime: '',
            details:[],

            // 未學習的設備----------------------------------------------
            not_studied_img_name_search: '',
            not_studied_currentPage: 1,
            not_studied_totalPage: 20,
            // 已修改----------------------------------------------
            already_edited_img_name_search: '',
            already_edited_currentPage: 1,
            already_edited_totalPage: 20,
        }
    },
    mounted() {
        // 讀取時間紀錄
        this.GetTimeRecord()
        this.UnmodifiedPageInfo()
    },
    methods: {
        show(index) {
            ;(this.showIndex = index), (this.showModal = true)
        },
        // 未修改===================================================================================
        check_mark() {
            console.log('check_mark', this.if_mark)
            this.UnmodifiedPageInfo()
        },
        UnmodifiedSearch() {
            console.log('UnmodifiedSearch', this.unmodified_img_name_search)
        },
        UnmodifiedCurrentChange(val) {
            console.log('UnmodifiedCurrentChange', val)
        },
        //讀取時間紀錄
        GetTimeRecord() {
            this.axios.get('/tsmcserver/time_record').then((res) => {
                this.uploadTime = res.data
            })
        },
        UnmodifiedPageInfo() {
            console.log('UnmodifiedPageInfo')
            this.axios.post('/tsmcserver/unmodified_page_info', {
                currentPage: this.unmodified_currentPage,
                if_mark: this.if_mark ? 1 : 0,
                img_name_search: this.unmodified_img_name_search
            }).then((res) => {
                console.log('response：',res.data)
                this.details = res.data
                // console.log('this.details', this.details)
            })
        },
        // 未學習的設備===================================================================================
        NotStudiedSearch() {
            console.log('NotStudiedSearch')
        },
        Not_studied_CurrentChange(val) {
            console.log('Not_studied_CurrentChange', val)
        },
        // 已修改===================================================================================
        AlreadyEditedSearch() {
            console.log('AlreadyEditedSearch')
        },
        Already_edited_CurrentChange(val) {
            console.log('Already_edited_CurrentChange', val)
        },
        update_result() {
            console.log('update_result')
        }
    }
}
</script>

<style scoped >
.container5 {
    margin: 0px;
    padding: 10px 30px 0px 30px;
    /* display: grid;
    grid-template-rows: 80px 1fr; */
}
.custom-tab-label >>> .el-tabs__item {
    font-size: 18px !important;
}
.tab_body {
    display: grid;
    grid-template-rows: 50px 1fr;
}
.options {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    align-items: center;
    border-bottom: 2px solid #757575;
}
.search {
    display: flex;
    justify-content: center;
}
.search_btn {
    margin-left: 10px;
    font-size: 16px;
    padding: 0px 10px;
    background-color: #1F6DB3;
    color: white;
    border: none;
    border-radius: 5px;
    
}
.content {
    height: calc(100vh - 210px - 35px);
    /* background-color: #1F6DB3; */
    
}
.img_outside_container {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    grid-template-rows: repeat(3, 1fr);
}
.page_selection {
    height: 35px;
    /* background-color: #757575; */
    display: flex;
    align-items: center;
    justify-content: center;
}

/* 未修改頁面=================================================== */

/* 未學習的設備頁面=================================================== */

/* 已修改頁面=================================================== */
.update_result {
    display: flex;
    justify-content: flex-end;
}
.update_result_btn {
    font-size: 16px;
    font-weight: bold;
    padding: 5px 10px;
    background-color: #363636;
    color: white;
    border: none;
    border-radius: 5px;
}
</style>
<script setup>
import SmallPicture from '@/components/results/small-picture.vue'
import UnmodifiedDetail from '@/components/results_correction/unmodified_detail.vue'
import AlreadyEditedDetail from '@/components/results_correction/already_edited_detail.vue'
// import { fa } from 'element-plus/es/locale';
import { ElMessage, ElMessageBox } from 'element-plus'
import 'element-plus/es/components/message/style/css'
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
                                @clear="unmodified_img_name_search = ''; UnmodifiedSearch()"
                            />
                            <button class="search_btn" @click="UnmodifiedSearch">搜尋</button>
                        </div>
                    </div>
                    <div class="content">
                        <div class="img_outside_container" v-if="unmodified_details && unmodified_details.length > 0">
                            <div
                                v-for="(detail, index) in unmodified_details"
                                :src="detail.image_path"
                                :key="index"
                                @click="UnmodifiedShow(index)"
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
            <!-- 詳細資料 -->
            <div v-if="unmodified_showModal && unmodified_details && unmodified_details.length > 0">
                <UnmodifiedDetail 
                    :src="unmodified_details[this.unmodified_showIndex].image_path"
                    :details="unmodified_details[this.unmodified_showIndex]"
                    v-show="unmodified_showModal"
                    @close="unmodified_showModal = false"
                    @save_success="UnmodifiedPageInfo"
                    ></UnmodifiedDetail>
            </div>
<!-- 未學習的設備 -->
            <!-- <el-tab-pane label="未學習的設備" name="second">
                <div class="tab_body">
                    <div class="options">
                        <div class="search" style="grid-column: 2">
                            <el-input
                                v-model="not_studied_img_name_search"
                                style="width: 240px"
                                placeholder="請輸入照片名稱"
                                clearable
                                @clear="not_studied_img_name_search = ''; NotStudiedSearch()"
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
            </el-tab-pane> -->
<!-- 已修改 -->
            <el-tab-pane label="已修改(未訓練)" name="third">
                <div class="tab_body">
                    <div class="options">
                        <div class="search" style="grid-column: 2">
                            <el-input
                                v-model="already_edited_img_name_search"
                                style="width: 240px"
                                placeholder="請輸入照片名稱"
                                clearable
                                @clear="already_edited_img_name_search = ''; AlreadyEditedSearch()"
                            />
                            <button class="search_btn" @click="AlreadyEditedSearch">搜尋</button>
                        </div>
                        <div class="retrain">
                            <button v-if="!if_training" class="retrain_btn" @click="retrain">重新訓練模型</button>
                            <el-button v-else color="#000000" type="primary" loading>Retraining</el-button>
                        </div>
                    </div>
                    <div class="content">
                        <div class="img_outside_container" v-if="already_edited_details && already_edited_details.length > 0">
                            <div
                                v-for="(detail, index) in already_edited_details"
                                :src="detail.image_path"
                                :key="index"
                                @click="AlreadyEditedShow(index)"
                            >
                                <SmallPicture
                                    :src="detail.image_path"
                                    :original_image="detail.image_path"
                                ></SmallPicture>
                            </div>
                        </div>
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
            <div v-if="already_edited_showModal && already_edited_details && already_edited_details.length > 0">
                <AlreadyEditedDetail 
                    :src="already_edited_details[this.already_edited_showIndex].image_path"
                    :details="already_edited_details[this.already_edited_showIndex]"
                    v-show="already_edited_showModal"
                    @close="already_edited_showModal = false"
                    @update_result="update_already_edited_info(); UnmodifiedPageInfo()"
                    ></AlreadyEditedDetail>
            </div>
<!-- 已訓練 -->
            <el-tab-pane label="已訓練" name="fourth">
                <div class="tab_body">
                    <div class="options">
                        <div class="search" style="grid-column: 2">
                            <el-input
                                v-model="already_train_img_name_search"
                                style="width: 240px"
                                placeholder="請輸入照片名稱"
                                clearable
                                @clear="already_train_img_name_search = ''; AlreadyTrainSearch()"
                            />
                            <button class="search_btn" @click="AlreadyTrainSearch">搜尋</button>
                        </div>
                    </div>
                    <div class="content">
                        <div class="img_outside_container" v-if="already_train_details && already_train_details.length > 0">
                            <div
                                v-for="(detail, index) in already_train_details"
                                :src="detail.image_path"
                                :key="index"
                                @click="AlreadyTrainShow(index)"
                            >
                                <SmallPicture
                                    :src="detail.image_path"
                                    :original_image="detail.image_path"
                                ></SmallPicture>
                            </div>
                        </div>
                    </div>
                    <div class="page_selection">
                        <el-pagination
                            v-model:current-page="already_train_currentPage"
                            background
                            layout="prev, pager, next, jumper"
                            :total="already_train_totalPage"
                            @current-change="Already_train_CurrentChange"
                        />
                    </div>
                </div>
            </el-tab-pane>
        </el-tabs>
    </div>
</template>

<script>
export default {
    data() {
        return {
            activeName: 'first',
            uploadTime: '',
            // 未修改----------------------------------------------
            unmodified_showIndex: 0,
            unmodified_showModal: false,

            if_mark: false,
            unmodified_img_name_search: '',
            unmodified_currentPage: 1,
            unmodified_totalPage: 20,

            unmodified_details:[],

            // 未學習的設備----------------------------------------------
            not_studied_img_name_search: '',
            not_studied_currentPage: 1,
            not_studied_totalPage: 10,
            // 已修改----------------------------------------------
            already_edited_showIndex: 0,
            already_edited_showModal: false,
            already_edited_img_name_search: '',
            already_edited_currentPage: 1,
            already_edited_totalPage: 10,

            if_training: false,
            check_if_training: false,

            already_edited_details: [],
            // 已訓練----------------------------------------------
            already_train_showIndex: 0,
            already_train_showModal: false,
            already_train_img_name_search: '',
            already_train_currentPage: 1,
            already_train_totalPage: 10,

            already_train_details: []

        }
    },
    mounted() {
        // 讀取時間紀錄
        this.GetTimeRecord()
        this.UnmodifiedPageInfo()
    },
    watch: {
        activeName(newVal, oldVal) {
            if (newVal === 'first') {
                this.UnmodifiedPageInfo();
            } else if (newVal === 'second') {
                console.log('second');
            } else if (newVal === 'third') {
                this.AlreadyEditedPageInfo();
                this.startTrainingInterval();
            } else if (newVal === 'fourth') {
                console.log('fourth');
                this.AlreadyTrainPageInfo();
            }

            if (oldVal === 'third' && newVal !== 'third') {
                this.stopTrainingInterval();
            }
        }
    },
    methods: {
// 未修改===================================================================================
        UnmodifiedShow(index) {
            ;(this.unmodified_showIndex = index), (this.unmodified_showModal = true)
        },
        check_mark() {
            console.log('check_mark', this.if_mark)
            this.UnmodifiedPageInfo()
        },
        UnmodifiedSearch() {
            console.log('UnmodifiedSearch', this.unmodified_img_name_search)
            this.UnmodifiedPageInfo()
        },
        UnmodifiedCurrentChange(val) {
            console.log('UnmodifiedCurrentChange', val)
            this.UnmodifiedPageInfo()
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
                console.log('未修改',res.data)
                this.unmodified_details = res.data.data
                this.unmodified_totalPage = res.data.total_count
                console.log('this.unmodified_details', this.unmodified_details)
                // console.log('this.unmodified_details', this.unmodified_details)
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
        AlreadyEditedShow(index) {
            ;(this.already_edited_showIndex = index), (this.already_edited_showModal = true)
            console.log('AlreadyEditedShow')
        },
        AlreadyEditedSearch() {
            console.log('AlreadyEditedSearch')
            this.AlreadyEditedPageInfo()
        },
        Already_edited_CurrentChange(val) {
            console.log('Already_edited_CurrentChange', val)
            this.AlreadyEditedPageInfo()
        },
        AlreadyEditedPageInfo() {
            console.log('AlreadyEditedPageInfo')
            this.axios.post('/tsmcserver/already_edited_page_info', {
                currentPage: this.already_edited_currentPage,
                img_name_search: this.already_edited_img_name_search
            }).then((res) => {
                console.log('已修改：',res.data)
                this.already_edited_details = res.data.data
                this.already_edited_totalPage = res.data.total_count
                console.log('this.already_edited_details', this.already_edited_details)
                // console.log('this.unmodified_details', this.unmodified_details)
            })
        },
        update_already_edited_info() {
            console.log('update_already_edited_info')
            this.AlreadyEditedPageInfo()
        },
        retrain() {
            console.log('retrain')
            ElMessageBox.confirm(
                '確認要重新訓練？',
                '注意！！！',
                {
                    confirmButtonText: 'OK',
                    cancelButtonText: 'Cancel',
                    type: 'warning',
                }
            )
            .then(() => {
                this.axios.post('/tsmcserver/retrain').then((res) => {
                    // console.log('retrain', res)
                    if (res.data.status == "success") {
                        this.$message({
                            message: '正在重新訓練',
                            type: 'success'
                        })
                    } else {
                        console.log('重新訓練失敗', res.data.message)
                        const msg = res.data.message ? res.data.message : '重新訓練失敗'
                        this.$message({
                            message: res.data.message,
                            type: 'error'
                        })
                    }

                    this.AlreadyEditedPageInfo()
                    // this.AlreadyTrainPageInfo()
                    // this.CheckIfTraining()
                })
            })
            .catch(() => {
                this.$message({
                    type: 'info',
                    message: '已取消重新訓練'
                })
            })
        },
        startTrainingInterval() {
            this.ifTrainingInterval = setInterval(this.CheckIfTraining, 1000);
        },
        stopTrainingInterval() {
            if (this.ifTrainingInterval) {
                clearInterval(this.ifTrainingInterval);
                this.ifTrainingInterval = null;
            }
        },
        CheckIfTraining() {
            this.axios.get('/tsmcserver/if_training').then((res) => {
                // console.log('CheckIfTraining', res.data)
                if (this.check_if_training && res.data.if_train == 0) {
                    this.check_if_training = false
                    this.AlreadyEditedPageInfo()
                    this.AlreadyTrainPageInfo()
                    this.$message({
                            message: '重新訓練完成',
                            type: 'success'
                        })
                }
                if (res.data.if_train == 1) {
                    this.if_training = true
                    this.check_if_training = true
                } else {
                    this.if_training = false
                }
                console.log('if_training', this.if_training)
            })
        },
// 已訓練===================================================================================
        AlreadyTrainShow(index) {
            ;(this.already_train_showIndex = index), (this.already_train_showModal = true)
            console.log('AlreadyTrainShow')
        },
        AlreadyTrainSearch() {
            console.log('AlreadyTrainSearch')
            this.AlreadyTrainPageInfo()
        },
        Already_train_CurrentChange(val) {
            console.log('Already_train_CurrentChange', val)
        },
        AlreadyTrainPageInfo() {
            console.log('AlreadyTrainPageInfo')
            this.axios.post('/tsmcserver/already_train_page_info', {
                currentPage: this.already_train_currentPage,
                img_name_search: this.already_train_img_name_search
            }).then((res) => {
                console.log('已訓練：',res.data)
                this.already_train_details = res.data.data
                this.already_train_totalPage = res.data.total_count
                console.log('this.already_train_details', this.already_train_details)
                // console.log('this.unmodified_details', this.unmodified_details)
            })
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
.retrain {
    display: flex;
    justify-content: flex-end;
}
.retrain_btn {
    font-size: 16px;
    font-weight: bold;
    padding: 5px 10px;
    background-color: #363636;
    color: white;
    border: none;
    border-radius: 5px;
}
</style>
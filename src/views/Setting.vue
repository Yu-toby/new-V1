<script setup>
import TemperatureList from '@/components/temperature_setting/list.vue';
import { ElMessage, ElMessageBox } from 'element-plus'
import 'element-plus/es/components/message/style/css'
</script>

<template>
    <div class="container6">
        <el-tabs v-model="activeName" class="demo-tabs custom-tab-label">
            <el-tab-pane label="溫度閥值" name="first">
                <div class="temp_item_name">
                    <div class="device_name">設備名稱</div>
                    <div class="temp_value">最低溫度</div>
                    <div class="item_name">
                        <div class="color_area">正常</div>
                        <div class="temp_value">閥值</div>
                    </div>
                    <div class="item_name">
                        <div class="color_area">注意</div>
                        <div class="temp_value">閥值</div>
                    </div>
                    <div class="item_name">
                        <div class="color_area">警告</div>
                        <div class="temp_value">閥值</div>
                    </div>
                    <div class="item_name">
                        <div class="color_area">危險</div>
                        <div class="temp_value">最大溫度</div>
                    </div>
                </div>
                <div class="temp_list">
                    <TemperatureList
                        v-for="(item, index) in temperatureList"
                        :key="index"
                        :device_type="item.device_type"
                        :lowest_temperature="item.lowest_temperature"
                        :temperature="item.temperature"
                        :_id="item._id"
                        @update_temperature="updateTemperature(index, $event)"
                        @delete_data="removeTemperatureData(index)"
                    ></TemperatureList>
                </div>
                
            </el-tab-pane>
            <el-tab-pane label="模型板本" name="second">
                <div class="model_info">
                    <el-descriptions title="當前模型資訊" direction="vertical" :column="3" border>
                        <el-descriptions-item
                            label="Model"
                            label-align="center"
                            align="center"
                            :span="1.5"
                            label-class-name="my-label"
                            class-name="my-content"
                            width="50%"
                        >
                            {{ current_model.model }}
                        </el-descriptions-item>
                        <el-descriptions-item label="Version" label-align="center" align="center" :span="1.5">
                            {{ current_model.version }}
                        </el-descriptions-item>
                    </el-descriptions>
                    <el-descriptions direction="vertical" :column="3" border>
                        <el-descriptions-item label="P" label-align="center" align="center" :span="1">
                            {{ current_model.P }}
                        </el-descriptions-item>
                        <el-descriptions-item label="R" label-align="center" align="center" :span="1">
                            {{ current_model.R }}
                        </el-descriptions-item>
                        <el-descriptions-item label="mAP50" label-align="center" align="center" :span="1">
                            {{ current_model.mAP50 }}
                        </el-descriptions-item>
                    </el-descriptions>
                </div>
                <div class="model_list">
                    <div class="model_list_title">其他模型</div>
                    <el-table
                        :data="modelList"
                        style="width: 100%"
                        border
                        height="calc(100vh - 430px)"
                        :row-class-name="tableRowClassName"
                        class="model_list_table_header"
                    >
                        <el-table-column
                            prop="model"
                            label="Model"
                            align="center"
                            width="(100/6)%"
                        ></el-table-column>
                        <el-table-column
                            prop="version"
                            label="Version"
                            align="center"
                            width="(100/6)%"
                        ></el-table-column>
                        <el-table-column
                            prop="P"
                            label="P"
                            align="center"
                            width="(100/6)%"
                        ></el-table-column>
                        <el-table-column
                            prop="R"
                            label="R"
                            align="center"
                            width="(100/6)%"
                        ></el-table-column>
                        <el-table-column
                            prop="mAP50"
                            label="mAP50"
                            align="center"
                            width="(100/6)%"
                        ></el-table-column>
                        <el-table-column
                            label="Action"
                            align="center"
                            width="(100/6)%"
                        >
                            <template #default="{ row, $index }">
                                <el-button v-if="!row.using" type="primary" size="small" @click="selectVersion(row, $index)">Select</el-button>
                                <el-button v-if="!row.using" type="danger" size="small" @click="deleteVersion(row, $index)">Delete</el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                </div>
            </el-tab-pane>
            <!-- <el-tab-pane label="Role" name="third">Role</el-tab-pane>
            <el-tab-pane label="Task" name="fourth">Task</el-tab-pane> -->
        </el-tabs>
    </div>
</template>

<script>
export default {
    data() {
        return {
            activeName: 'first',
            temperatureList: [],
            current_model: {
                model: 'YOLO v5', version: '1.0', P: '83.15%', R: '71.65%', map50: '77.4%' 
            },
            modelList: [],
        }
    },
    watch: {
        activeName() {
            if (this.activeName === 'first') {
                this.TemperaturePageInfo();
            }
            else if (this.activeName === 'second') {
                this.VersionSettingPageInfo();
            }
        }
    },
    mounted() {
        this.TemperaturePageInfo();
    },
    methods: {
        // 溫度設定===============================================================
        TemperaturePageInfo() {
            this.axios.post('/tsmcserver/temperature_page_info', {
            }).then(res => {
                console.log('溫度數據', res.data);
                this.temperatureList = res.data.data;
            }).catch(err => {
                console.log(err);
            });
        },
        updateTemperature(index, data) {
            console.log('更新溫度數據', index, data);
            this.TemperaturePageInfo();
        },
        removeTemperatureData(index) {
            console.log('刪除溫度數據', index);
            this.TemperaturePageInfo();
        },
        // 模型板本===============================================================
        VersionSettingPageInfo() {
            console.log('模型板本');
            this.axios.post('/tsmcserver/version_setting_page_info', {
            }).then(res => {
                this.modelList = res.data.data;
                console.log('模型data', this.modelList);

                // 找到使用中的模型
                const currentModel = res.data.data.find(model => model.using === true);
                this.current_model = currentModel ? currentModel : null; // 確保即使沒有找到符合條件的模型也不會出錯
                // console.log('使用中的模型', this.current_model);
            }).catch(err => {
                console.log(err);
            });
        },
        selectVersion(row, index) {
            console.log('選擇模型', row, index);
            ElMessageBox.confirm(
                '確認要變更為此辨識模型版本？',
                '注意！！！',
                {
                    confirmButtonText: 'OK',
                    cancelButtonText: 'Cancel',
                    type: 'warning',
                }
            )
            .then(() => {
                console.log('change_model');
                this.axios.post('/tsmcserver/select_model_version', {
                    _id: row._id,
                }).then((res) => {
                    console.log(res);
                    this.VersionSettingPageInfo();
                }).catch((err) => {
                    console.log(err);
                });
                ElMessage({
                    type: 'success',
                    message: '變更成功',
                });
            })
            .catch(() => {
                ElMessage({
                    type: 'info',
                    message: '取消刪除',
                });
            });
        },
        deleteVersion(row, index) {
            console.log('刪除模型', row, index);
            ElMessageBox.confirm(
                '確認要刪除此辨識模型版本？',
                '注意！！！',
                {
                    confirmButtonText: 'OK',
                    cancelButtonText: 'Cancel',
                    type: 'warning',
                }
            )
            .then(() => {
                console.log('delete_model');
                this.axios.post('/tsmcserver/delete_model_version', {
                    _id: row._id,
                }).then((res) => {
                    console.log(res);
                    this.VersionSettingPageInfo();
                }).catch((err) => {
                    console.log(err);
                });
                ElMessage({
                    type: 'success',
                    message: '刪除成功',
                });
            })
            .catch(() => {
                ElMessage({
                    type: 'info',
                    message: '取消刪除',
                });
            });
        },
        tableRowClassName({ row, rowIndex }) {
            if (row.using) {
                console.log('使用中的模型', row);
                return 'using-model-row';
            }
            return '';
        },
    },    
    beforeUnmount() {
    }
}
</script>

<style scoped >
.container6 {
    margin: 0px;
    padding: 10px 30px 0px 30px;
    height: calc(100vh - 90px);
}
.custom-tab-label >>> .el-tabs__item {
    font-size: 18px !important;
}
/* 溫度設定=============================================================== */
.temp_item_name {
    height: 60px;
    font-size: 18px;
    font-weight: bold;
    display: flex;
    align-items: center;
    width: 100%;
    padding: 10px;
    display: grid;
    grid-template-columns: 1fr 0.12fr 1fr 1fr 1fr 1fr 1fr;
    padding: 10px 20px;
    background-color: rgb(12, 12, 12);
    color: white;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
}
.device_name {
    font-size: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
}
.item_name {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-around;
}
.color_area {
    width: 150px;
    height: 32px;
    text-align: center;
}
.temp_value {
    /* margin: 0 10px; */
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    width: 50px;
    height: 32px;
}
.temp_list {
    max-height: calc(100vh - 250px); /* Adjust this height as needed */
    overflow-y: auto;
    border-bottom: 1px solid #000000;
    border-left: 1px solid #000000;
    border-right: 1px solid #000000;
}
/* 模型板本=============================================================== */
::v-deep .el-descriptions__header {
    justify-content: center;
    width: 100%;
    margin-bottom: 6px;
}
::v-deep .el-descriptions__title {
    font-size: 20px;
}
.model_list_title {
    font-size: 20px;
    font-weight: bold;
    margin-top: 10px;
    margin-bottom: 3px;
    display: flex;
    justify-content: center;
}
.model_list_table_header ::v-deep .el-table__header-wrapper th {
    background-color: #505050; /* 修改表頭背景顏色 */
    color: #ffffff; /* 修改表頭文字顏色 */
    font-size: 16px;
}
::v-deep .el-table .using-model-row {
    background-color: #9ab5c5 !important;
    color: #000000 !important;
}
</style>
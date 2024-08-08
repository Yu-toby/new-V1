<script setup>
import { ElMessage, ElMessageBox } from 'element-plus'
import 'element-plus/es/components/message/style/css'
</script>

<template>
    <div class="temp_container">
        <div class="container_body">
            <div class="device_name">{{ device_type }}</div>
            <div class="temperature_threshold">
                <div v-if="!if_edit" class="temp_value">{{ editableLowestTemperature }}</div>
                <input v-else class="temp_value" v-model="editableLowestTemperature" type="number" />
            </div>            
            <div v-for="(value, index) in editableTemperature" :key="index" class="temperature_threshold">
                <div class="color_area" :style="{backgroundColor: colors[index] }"></div>
                <div v-if="!if_edit" class="temp_value">{{ value }}</div>
                <input v-else class="temp_value" v-model="editableTemperature[index]" type="number"/>
            </div>
            <div class="btn_area">
                <button v-if="!if_edit" @click="editTemperature" class="btn_item">修改</button>
                <button v-else @click="saveTemperature" class="btn_item">儲存</button>
                <button @click="deleteTemperature" class="btn_item">移除</button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        device_type: {
            type: String,
            required: true
        },
        lowest_temperature: {
            type: Number,
            required: true
        },
        temperature: {
            type: Array,
            required: true
        },
        _id: {
            type: String,
            required: true
        },
    },
    data() {
        return {
            editableLowestTemperature: this.lowest_temperature,
            editableTemperature: [...this.temperature],
            originalLowestTemperature: this.lowest_temperature,
            originalTemperature: [...this.temperature],
            colors: ['#b8e994', '#f6e58d', '#ffbe76', '#ff7979'],
            if_edit: false,
            
        }
    },
    methods: {
        editTemperature() {
            this.if_edit = true;
            this.editableLowestTemperature = this.lowest_temperature;
            this.editableTemperature = [...this.temperature];
        },
        saveTemperature() {
            ElMessageBox.confirm(
                '確認要變更此溫度資料？',
                '注意！！！',
                {
                    confirmButtonText: 'OK',
                    cancelButtonText: 'Cancel',
                    type: 'warning',
                }
            )
            .then(() => {
                this.if_edit = false;
                console.log('update id', this._id);
                console.log('update lowest_temperature', this.editableLowestTemperature);
                console.log('update temperature', this.editableTemperature);
                this.axios.post('/tsmcserver/update_temperature_data', {
                    _id: this._id,
                    lowest_temperature: this.editableLowestTemperature,
                    temperature: this.editableTemperature
                }).then((res) => {
                    this.$emit('update_temperature');
                    console.log('已變更detail', res);
                    ElMessage({
                        type: 'success',
                        message: '變更成功',
                    });
                }).catch((err) => {
                    console.log(err);
                    ElMessage({
                        type: 'error',
                        message: '變更失敗',
                    });
                });
            })
            .catch(() => {
                this.if_edit = false;
                this.editableLowestTemperature = this.originalLowestTemperature;
                this.editableTemperature = [...this.originalTemperature];
                ElMessage({
                    type: 'info',
                    message: '取消變更',
                });
            });
        },
        deleteTemperature() {
            ElMessageBox.confirm(
                '確認要刪除此溫度資料？',
                '注意！！！',
                {
                    confirmButtonText: 'OK',
                    cancelButtonText: 'Cancel',
                    type: 'warning',
                }
            )
            .then(() => {
                console.log('delete id', this._id);
                this.axios.post('/tsmcserver/delete_temperature_data', {
                    _id: this._id,
                }).then((res) => {
                    this.$emit('delete_data');
                    console.log('已刪除detail', res);
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
        }
    }
}
</script>

<style scoped>
.temp_container {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    /* border-bottom: 1px solid #ccc; */
}
.container_body {
    display: flex;
    align-items: center;
    width: 100%;
    border-bottom: 1px solid #ccc;
    border-left: 1px solid #ccc;
    border-right: 1px solid #ccc;
    display: grid;
    /* grid-template-columns: 1fr 50px 150px 150px 150px 150px 200px; */
    grid-template-columns: 1fr 0.12fr 1fr 1fr 1fr 1fr 1fr;
    padding: 10px 10px;
}
.device_name {
    font-size: 20px;
    font-weight: bold;
    display: flex;
    align-items: center;
    justify-content: center;
}
.temperature_threshold {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-around;
    /* width: 150px; */
}
.color_area {
    width: 150px;
    height: 20px;
    border-radius: 0;
    /* margin: 0 10px; */
}
.temp_value {
    /* margin: 0 10px; */
    display: flex;
    align-items: center;
    justify-content: center;
    width: 50px;
    height: 30px;
}
.btn_area {
    display: flex;
    align-items: center;
    justify-content: center;
    /* margin-left: 20px; */
}
.btn_item {
    width: 60px;
    height: 30px;
    border: 1px solid #ccc;
    border-radius: 5px;
    background-color: #f5f5f5;
    margin: 0px 10px;
    padding: 4px;
}
</style>

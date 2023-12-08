<template>
    <div class="container3">
        <div class="options_bar">
            <div class="date_selection">
                <n-date-picker v-model:value="timestamp" type="date" />
                <!-- <pre>{{timestamp}}</pre> -->
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
            <div class="status_selection">
                <select v-model="selectedOption" @change="getCategories(); updateStatusNumber()">
                    <option value disabled selected>請選擇狀態</option>
                    <option
                        v-for="(category, index) in Option"
                        :key="index"
                        :value="category"
                    >{{ category }}</option>
                </select>
            </div>
        </div>

        <div class="content">
            <div class="historical_data">
                <ul>
                    <div v-for="(item, index) in historicalData" :key="index">{{ item }}</div>
                </ul>
            </div>

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
</template>

<script>
import { ref } from 'vue'

export default {
    data() {
        return {
            timestamp: ref(118313526e4),
        selectedOption: '',
        Option: ['正常', '注意', '異常', '危險'],
        page: ref(1),
        pageSize: ref(20),
        pageSizes: [
            { label: '10 / page', value: 10 },
            { label: '20 / page', value: 20 },
            { label: '30 / page', value: 30 },
            { label: '40 / page', value: 40 }
        ],
        historicalData: []  // 此處新增 historicalData 數據屬性
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
    grid-template-columns: 1fr 2fr 2fr 2fr 1fr;
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

.status_selection {
    grid-column: 4;
    display: flex;
    align-items: center;
    justify-content: center;
}

.content {
    display: grid;
    grid-template-rows: 1fr 43px;
    /* border: 2px solid black; */
    background-color: rgb(187, 187, 157);
}

.page_selection {
    display: flex;
    justify-content: center;
    align-items: flex-end;
}
</style>

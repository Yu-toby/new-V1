<template>
    <div>
        <div class="example-pagination-block">
            <el-pagination
                background
                layout="prev, pager, next"
                :total="totalPages"
                :current-page="currentPage1"
                @current-change="handlePageChange1"
            />
            <div>當前頁碼: {{ currentPage1 }}</div>
        </div>

        <div class="example-pagination-block">
            <el-pagination
                background
                layout="prev, pager, next"
                :total="totalPages"
                :current-page="currentPage2"
                @current-change="handlePageChange2"
            />
            <div>當前頁碼: {{ currentPage2 }}</div>
        </div>
    </div>
</template>

<script  scoped>
export default {
    data() {
        return {
            totalPages: 100, // 總頁數
            currentPage1: 1, // 當前頁碼
            currentPage2: 1, // 當前頁碼
        }
    },
    methods: {
        // 監聽頁碼變化事件
        handlePageChange1(newPage) {
            // 將當前頁碼更新為新的頁碼
            this.currentPage1 = newPage

            // 在這裡可以執行相應的操作，例如獲取新頁碼對應的數據
            this.fetchDataForPage(newPage)
        },
        handlePageChange2(newPage) {
            // 將當前頁碼更新為新的頁碼
            this.currentPage2 = newPage

            // 在這裡可以執行相應的操作，例如獲取新頁碼對應的數據
            this.fetchDataForPage(newPage)
        },
        fetchDataForPage(page) {
            // 在這裡可以發起 API 請求，獲取新頁碼對應的數據
            // 這裡只是一個示例，實際應用中需要根據情況進行相應的處理
            console.log(`Fetching data for page ${page}`)
        }
    }
}
</script>

<style scoped>
.example-pagination-block + .example-pagination-block {
    margin-top: 20px;
}
.example-pagination-block .example-demonstration {
    margin-bottom: 56px;
}
</style>
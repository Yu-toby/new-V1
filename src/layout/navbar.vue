<template>
    <header class="navbar">
        <div class="header-logo">
            <img id="tsmc-logo" src="@/assets/picture/台積logo.png" />
            <a id="title-words">台積電熱影像辨識網頁</a>
        </div>
        <div class="options">
            <!-- <router-link to="/logout" ></router-link> -->
            <router-link to="/test" >測試頁面</router-link>
            <router-link to="/settings" >設定</router-link>
            <router-link to="/history">歷史查詢</router-link>            
            <!-- <router-link to="/resultsShow" >辨識結果</router-link> -->
            <router-link to="/" >首頁</router-link>
        </div>
    </header>
</template>

<script>
export default {}
</script>

<style scoped>
.navbar {
    overflow: hidden;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: rgba(0, 0, 0, 0.8);
    height: 55px;
    padding: 0px;
}
/*----------------------------------------------------------------------------------*/
.header-logo {    
    display: flex;
    color: rgba(0, 0, 0, 0.8);
    align-items: center;
    padding: 0px;    
}
#tsmc-logo {
    padding: 10px;
    height: 55px;
}
#title-words {
    font-weight: bold;
    font-size: 23px;
    color: rgb(255, 255, 255);
}
/*----------------------------------------------------------------------------------*/
.options a {    
    font-size: 18px;
    font-weight: bold;
    float: right;
    color: rgb(255, 255, 255);
    padding: 5px 15px;
    border-radius: 500px;
    text-decoration: none;
}

.options a:hover {
    background-color: #ffffff;
    color: rgba(0, 0, 0, 0.8);
}
</style>

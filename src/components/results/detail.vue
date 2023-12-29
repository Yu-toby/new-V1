<script setup>
import OverallTemplateBar from './overall-template-bar.vue';
import IntervalTemplateBar from './interval-template-bar.vue';
</script>

<template lang="">
    <div id="modal0">
        <div class="modal-content0">
            <div id="category-title">
                <p id="category-text">辨識類別：{{ describe?.category}}</p>
                <div id="closeButton"><button type="button" class="btn-close" aria-label="Close" @click="closeModal"></button></div>
            </div>
            <div id="details_con" :style="{ backgroundColor: bcolor }">
                <OverallTemplateBar
                    :overall_max_template="overallTmp"
                    :pointer="overall_pointer"
                ></OverallTemplateBar>
                <div class="details">
                    <table class="temperature-table0">
                        <tr>
                            <th id="top-table" :style="{ backgroundColor: tbcolor }">MAX</th>
                            <th id="top-table" :style="{ backgroundColor: tbcolor }">AVG</th>
                            <th id="top-table" :style="{ backgroundColor: tbcolor }">MIN</th>
                        </tr>
                        <tr>
                            <th id="max-temperature">{{describe?.max}}℃</th>
                            <th id="avg-temperature">{{describe?.avg}}℃</th>
                            <th id="min-temperature">{{describe?.min}}℃</th>
                        </tr>
                    </table>
                    <div class="change_image_btn">
                        <button type="button" class="btn btn-secondary" @click="changeImage">熱影像 / 可見光</button>
                    </div>
                    <img :src="src" id="detail-picture"  :style="{ borderColor: tbcolor }">
                </div>                
                <IntervalTemplateBar
                    :tbcolor="tbcolor"
                    :interval_min_template="tmpArray[0]"
                    :interval_max_template="tmpArray[1]"
                    :barHeight="interval_barHeight"
                    :pointer="interval_pointer"
                ></IntervalTemplateBar>
            </div>
            <div id="result-field">
                <p id="result-text">檢測結果：{{describe?.result}}</p>
            </div>
        </div> 
        <button @click="GetTemperatureArray">觸發</button>
    </div>
</template>
<script>
export default {
    props:{    
        src: {
            type: String,
            required: ''
        },    
        describe: {
            type: Object,
            default: () => ({})
        },
        bcolor: {
            type: String,
            default: ''
        },
        tbcolor: {
            type: String,
            default: ''
        }
    },
    emit: [
        "close"
    ],
    data() {
        return {
            temperature_array: [{}],
            overallTmp: 0,
            tmpArray: [],
            overall_pointer: 0,
            interval_pointer: 0,
            interval_barHeight: 0,
        }
    },
    mounted() {
        this.GetTemperatureArray();
    },
    methods: {
        closeModal() {
            this.$emit("close");
        },
        changeImage() {
            this.$emit("change");
        },
        GetTemperatureArray() {
            this.axios.post('/tsmcserver/getTemperatureArray', {
                name: this.describe?.category,
                result: this.describe?.result
            }).then(res => {
                this.temperature_array = res.data;
                this.overallTmp = this.temperature_array?.overall_tmp;
                this.tmpArray = this.temperature_array?.tmp;
                console.log(this.overallTmp);
                console.log(this.tmpArray);
                this.calculateOverallPointerPosition();
                this.calculateIntervalPointerPosition();
                this.calculateIntervalBarHeight();
            }).catch(err => {
                console.log(err);
            })
        },
        calculateOverallPointerPosition() {
            const pt = (this.describe?.max / this.overallTmp) * 100
            this.overall_pointer = pt
        },
        calculateIntervalPointerPosition() {
            const pt =
                ((this.describe?.max - this.tmpArray[0]) /
                    (this.tmpArray[1] - this.tmpArray[0])) *
                100
            this.interval_pointer = pt
        },
        calculateIntervalBarHeight() {
            const pt = (this.tmpArray[1] - this.tmpArray[0])
            this.interval_barHeight = pt
        },
    },
}
</script>
<style>
/* .hidden {
    display: none !important;
} */

#modal0 {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.35);
    display: flex;
    justify-content: center;
    align-items: center;
}

.modal-content0 {
    padding: 0;
    height: 70dvb;
    width: 85dvb;
    background-color: white;
    border: 5px solid rgb(46, 46, 41);
    border-radius: 10px;
    display: grid;
    grid-template-rows: 0.12fr 1fr 0.12fr;
}

#category-title {
    margin: 0;
    display: grid;
    grid-template-columns: 50px 1fr 35px;
    /* border: 1px solid black; */

}

#category-text {
    margin: 0;
    grid-column: 2;
    font-size: 2vw;
    font-weight: bold;
    display: flex;
    align-items: center;
    justify-content: center;
}

#closeButton {
    grid-column: 3;
    display: flex;
    align-items: center;
    justify-content: start;
}

#details_con {
    margin: 0;
    /* background-color: rgb(226, 245, 215); */
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-around;
}

.details {
    margin: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-around;
    /* border: 1px solid black; */
}

.temperature-table0 {
    margin-bottom: 3%;
    font-size: 1.5vw;
    border-collapse: collapse;
}

.temperature-table0 th {
    padding: 0.1vw 1.5vw;
    border: 3px solid rgb(66, 66, 58);
    height: 100%;
    background-color: white;
    text-align: center;
}

/* #top-table {
    background-color: rgb(124, 208, 72);
} */

#detail-picture {
    height: 33vh;
    width: auto;
    margin-top: 10px;
    border: 3px solid;
    /* border-color: rgb(124, 208, 72); */
}

#result-field {
    margin: 0;
    display: flex;
    justify-content: center;
    /* border: 1px solid black; */
}

#result-text {
    margin: 0;
    font-size: 2vw;
    font-weight: bold;
    display: flex;
    align-items: center;
    justify-content: center;
}

.change_image_btn {
    margin-top: 5px;
    /* display: flex; */
    /* justify-content: center; */
}
</style>
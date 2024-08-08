<script setup>
import OverallTemplateBar from './overall-template-bar.vue'
import IntervalTemplateBar from './interval-template-bar.vue'
</script>

<template lang="">
    <div id="modal0">
        <div class="modal-content0">
            <div id="category-title">
                <div id="error_check">
                    <el-checkbox v-model="identification_error" label="辨識錯誤" @change="check_error"/>
                    <!-- <el-switch
                        v-model="identification_error"
                        inline-prompt
                        active-text="是"
                        inactive-text="否"
                        @change="check_error"
                    /> -->
                </div>
                <p id="category-text">辨識類別：{{ describe?.category}}</p>
                <div id="closeButton">
                    <div/>
                    <button type="button" class="btn-close" aria-label="Close" @click="closeModal"/>
                </div>
            </div>
            <div id="details_con" :style="{ backgroundColor: bcolor }">
                <OverallTemplateBar
                    :overall_max_template="overallTmp"
                    :pointer="overall_pointer"
                    :normal_height="normal_height"
                    :notice_height="notice_height"
                    :abnormal_height="abnormal_height"
                    :danger_height="danger_height"
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
                        <button type="button" class="btn btn-secondary" @click="ChangeImage">熱影像 / 可見光</button>
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
    </div>
</template>
<script>
export default {
    props: {
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
        },
        // error_check: {
        //     type: Boolean,
        //     default: false
        // }
    },
    emit: ['close'],
    watch: {
        describe: {
            // 監聽describe的變化
            handler() {
                // 當describe有變化時，執行以下function
                this.GetTemperatureArray();
                this.identification_error = this.describe?.correction_mark;
            },
            deep: true
        }
    },
    data() {
        return {
            temperature_array: [{}],
            overallTmp: 0,
            tmpArray: [],
            overall_pointer: 0,
            interval_pointer: 0,
            interval_barHeight: 0,
            nor_height: [],
            not_height: [],
            abn_height: [],
            dan_height: [],
            normal_height: 0,
            notice_height: 0,
            abnormal_height: 0,
            danger_height: 0,
            identification_error: this.describe?.correction_mark
        }
    },
    mounted() {
        this.GetTemperatureArray()
        this.identification_error = this.describe?.correction_mark
    },
    methods: {
        closeModal() {
            this.$emit('close')
        },
        ChangeImage() {
            console.log('ChangeImage')
            this.$emit('change1')
        },
        check_error() {
            console.log('Checkbox changed: ', this.identification_error, this.describe?._id)

            this.axios.post('/tsmcserver/identification_error', {
                _id: this.describe?._id,
                correction_mark: this.identification_error
            }).then((res) => {
                console.log(res)
                this.$emit('check_error_change')
            }).catch((err) => {
                console.log(err)
            })
        },
        GetTemperatureArray() {
            console.log('GetTemperatureArray')
            console.log(this.describe?.category, this.describe?.result)
            if (this.describe?.category !== undefined && this.describe?.result !== undefined) {
                this.axios
                    .post('/tsmcserver/getTemperatureArray', {
                        name: this.describe?.category || '',
                        result: this.describe?.result || ''
                    })
                    .then((res) => {
                        this.temperature_array = res.data
                        this.overallTmp = this.temperature_array?.overall_tmp
                        this.tmpArray = this.temperature_array?.tmp
                        this.nor_height = this.temperature_array?.normal_tmp
                        this.not_height = this.temperature_array?.notice_tmp
                        this.abn_height = this.temperature_array?.abnormal_tmp
                        this.dan_height = this.temperature_array?.danger_tmp

                        this.calculateOverallPointerPosition()
                        this.calculateIntervalPointerPosition()
                        this.calculateIntervalBarHeight()
                        this.calculateStateHeight()
                    })
                    .catch((err) => {
                        console.log(err)
                    })
            } else {
                console.log('category or result is empty')
                return
            }
        },
        calculateOverallPointerPosition() {
            const pt = (this.describe?.max / this.overallTmp) * 100
            this.overall_pointer = pt
        },
        calculateIntervalPointerPosition() {
            const pt =
                ((this.describe?.max - this.tmpArray[0]) / (this.tmpArray[1] - this.tmpArray[0])) *
                100
            this.interval_pointer = pt
        },
        calculateIntervalBarHeight() {
            const pt = this.tmpArray[1] - this.tmpArray[0]
            this.interval_barHeight = pt
        },
        calculateStateHeight() {
            this.normal_height = ((this.nor_height[1] - this.nor_height[0]) / this.overallTmp) * 100
            this.notice_height = ((this.not_height[1] - this.not_height[0]) / this.overallTmp) * 100
            this.abnormal_height =
                ((this.abn_height[1] - this.abn_height[0]) / this.overallTmp) * 100
            this.danger_height = ((this.dan_height[1] - this.dan_height[0]) / this.overallTmp) * 100
            // console.log(this.normal_height, this.notice_height, this.abnormal_height, this.danger_height);
        }
    }
}
</script>

<style scoped>
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
    grid-template-columns: 100px 1fr 100px;
    /* border: 1px solid black; */
    position: relative;
}

#error_check {
    grid-column: 1;
    display: flex;
    align-items: center;
    justify-content: center;
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
    justify-content: space-around;
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
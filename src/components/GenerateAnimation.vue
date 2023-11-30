<template>
<div class="m-3">
    <h5 class="mt-3" v-if="techniqueName">{{techniqueName}}</h5>
    <p>{{techniqueDescription}}</p>
    <div>
        <button class="btn btn-success p-1 m-1" @click="() => {showPies = false; generateFn()}" :disabled="textToShow.some(word => !word.show)">Generate</button>
    </div>
    <span v-for="word in textToShow" :key="word.pos">
        <button v-if="word.show" class="btn btn-dark p-1 m-1" disabled>{{ word.word }}</button>
    </span>
    <button v-if="textToShow.some(word => !word.show)" class="btn btn-secondary p-1 m-1" disabled><span class="loading"></span></button>
    <div v-if="showPies || (textToShow.length && textToShow.every(word => word.show))"><button class="btn btn-primary p-1 m-3" @click="() => {this.showPies=true}">How?</button></div>
    <div class="row pie-container" v-if="showPies">
        <div class="col p-1 m-0" v-for="word in textToShow" :key="word.pos">
            <div><button class="btn btn-light"><small>{{ word.pos }}</small></button></div>
            <div v-if="word.prevN">
            <div v-for="x in word.prevN.split(' ')" :key="x"><button class="btn btn-light"><small>{{ x }}</small></button></div>
            <button class="btn btn-light"><small>=></small></button>
            </div>
            <div><button class="btn btn-dark p-1 m-1" disabled>{{ word.word }}</button></div>
            <!-- <div><button class="btn btn-dark p-1 m-1" :style="{'background-color': word.backgroundColor}">{{ word.word }}</button></div> -->
            <div class="d-flex justify-content-center align-items-center" v-if="word.hasPie">
                <Pie :data="word.pieChartData" :options="chartOptions" style="width: 50px; height: 75px" />
            </div>
        </div>
    </div>
</div>
</template>

<script>       
import {
    Chart as ChartJS,
    ArcElement,
    Tooltip,
    Legend,
    Colors
} from 'chart.js'
import {
    Pie
} from 'vue-chartjs'

ChartJS.register(ArcElement, Tooltip, Legend, Colors) 

export default {
    components: {
        Pie
    },
    props: {
        textToShow: {
            type: Array,
        },
        generateFn: {
            type: Function,
        },
        techniqueName: {
            type: String,
        },
        techniqueDescription: {
            type: String,
        },
    },
    data() {
        return {
            showPies: false,
            chartOptions: {
                responsive: true,
                maintainAspectRatio: false,
                plugins:{
                    legend: {
                        display: false,
                    },
                },
            }
        }
    }
};
</script>

<style>
.pie-container .col:not(:last-child) {
    border-right: 3px solid #ccc;
}

.loading::after {
    display: inline-block;
    animation: dotty steps(1, end) 1s infinite;
    content: '';
}

@keyframes dotty {
    0% {
        content: '';
    }

    25% {
        content: '.';
    }

    50% {
        content: '..';
    }

    75% {
        content: '...';
    }

    100% {
        content: '';
    }
}
</style>

<template>
<div>
    <h3>Ord "flow"</h3>
    <p>
        Nedenfor vil vi lave et diagram kaldet et "sankey-diagram". Dette diagram viser "flow" af ord fra det ene til det andet (dvs. hvor ofte et eller flere ord fører til et andet ord). <br>
        Det er grundlæggende sandsynlighed, men bare smukt. <br>
        Dette diagram er baseret på alles inputsætninger. Du kan vælge vinduesstørrelsen som før. <br>
    </p>
    <label>Vælg vinduesstørrelsen:</label>
    1<input type="range" v-model="windowSize" min="1" max="5" />5
    <div class="my-2"><button class="btn btn-success" @click="getChart()" :disabled="!chartReady">{{chartReady ? 'Lav diagrammet' : 'Opdaterer...'}}</button></div>
    <div class="my-3" style="height:200vh;" v-show="currChart">
        <canvas ref="chart"></canvas>
    </div>
    <button class="btn btn-primary mb-3" @click="moveOn()" :disabled="!canAdvance" v-if="currChart">{{ canAdvance ? 'Fortsæt' : 'Vent venligst...' }}</button>
</div>
</template>

<script>
import {
    Chart,
    registerables
} from 'chart.js';
import {
    SankeyController,
    Flow
} from 'chartjs-chart-sankey';

Chart.defaults.font.size = 12;
Chart.defaults.font.family = 'JetBrains Mono'
Chart.defaults.font.weight = 'bold'
Chart.defaults.borderColor = 'black'

Chart.register(SankeyController, Flow, ...registerables);

export default {
    data() {
        return {
            windowSize: 1,
            minOccurrences: 1,
            chartReady: true,
            currChart: undefined
        }
    },
    props: {
        allSentences: {
            type: Array
        },
        currState: {
            type: String
        },
        states: {
            type: Array
        }
    },
    computed: {
        canAdvance() {
            return this.states.indexOf(this.currState) > this.states.indexOf('sankey')
        },
        ctx() {
            return this.$refs.chart.getContext('2d')
        },
        fromWords() {
            let words = [];
            for (let key in this.probabilities) {
                words.push(key);
            }
            const countMap = words.reduce((acc, color) => {
                acc[color] = (acc[color] || 0) + 1;
                return acc;
            }, {});
            let result = [];
            let min = this.minOccurrences
            while (result.length <= 0) {
                result = Object.keys(countMap)
                    .filter(color => countMap[color] > min);
                min--;
            }
            return result;
        },
        toWords() {
            let words = [];
            for (let key in this.probabilities) {
                for (let key2 in this.probabilities[key]) {
                    words.push(key2)
                }
            }
            const countMap = words.reduce((acc, color) => {
                acc[color] = (acc[color] || 0) + 1;
                return acc;
            }, {});
            let result = [];
            let min = this.minOccurrences
            while (result.length <= 0) {
                result = Object.keys(countMap)
                    .filter(color => countMap[color] > min);
                min--;
            }
            return result;
        },
        flows() {
            let flows = []
            for (let k of this.fromWords) {
                for (let k2 of this.toWords) {
                    if (k in this.probabilities && k2 in this.probabilities[k]) {
                        flows.push({
                            from: k + "\t",
                            to: k2,
                            flow: this.probabilities[k][k2]
                        })
                    }
                }
            }
            return flows
        },
        probabilities() {
            return this.slidingWindow(this.windowSize)
        }
    },
    methods: {
        moveOn() {
            this.$router.push({
                path: 'free',
            })
        },
        getColour(w, from) {
            let index = -1
            let totalWords = 1
            if (from) {
                index = this.fromWords.indexOf(w);
                totalWords = this.fromWords.length
            } else {
                index = this.toWords.indexOf(w)
                totalWords = this.toWords.length
            }
            if (index > -1) {
                return `hsl(${index * 360 / totalWords}, 100%, 50%)`
            }
            return 'black'
        },
        slidingWindow(N) {
            let probabilities = {}
            for (let s of this.allSentences) {
                let prevN = []
                for (let i = 0; i < N; i++) {
                    prevN.push(".")
                }
                for (let x of s.split(" ")) {
                    if (prevN.join(" ") in probabilities) {
                        if (x in probabilities[prevN.join(" ")]) {
                            probabilities[prevN.join(" ")][x]++
                        } else {
                            probabilities[prevN.join(" ")][x] = 1
                        }
                    } else {
                        probabilities[prevN.join(" ")] = {}
                        probabilities[prevN.join(" ")][x] = 1
                    }
                    prevN.shift()
                    prevN.push(x)
                }
                if (prevN.join(" ") in probabilities) {
                    if ("." in probabilities[prevN.join(" ")]) {
                        probabilities[prevN.join(" ")]["."]++
                    } else {
                        probabilities[prevN.join(" ")]["."] = 1
                    }
                } else {
                    probabilities[prevN.join(" ")] = {}
                    probabilities[prevN.join(" ")]["."] = 1
                }
            }
            return probabilities
        },
        getChart() {
            this.chartReady = false
            setTimeout(() => {
                this.chartReady = true
            }, 5000)
            if (this.currChart) {
                this.currChart.destroy()
            }
            this.currChart = new Chart(this.ctx, {
                type: 'sankey',
                data: {
                    datasets: [{
                        label: 'Sankey',
                        data: this.flows,
                        colorFrom: () => 'gray',
                        colorTo: (c) => this.getColour(c.dataset.data[c.dataIndex].to, false),
                        colorMode: 'gradient',
                        size: 'max',
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                }
            });
        }
    }
}
</script>

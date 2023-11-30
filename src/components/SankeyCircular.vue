<template>
<div>
    <button class="btn btn-success" ref="genbutton" @click="() => {getChart(); $refs.genbutton.remove()}">Render</button>
    <div class="my-3" style="height:100vh; width: 300vw;">
        <canvas ref="chart"></canvas>
    </div>
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

Chart.defaults.font.size = 30;
Chart.defaults.font.family = 'JetBrains Mono'
Chart.defaults.font.weight = 'bold'
Chart.defaults.borderColor = 'black'
Chart.defaults.backgroundColor = 'white'

Chart.register(SankeyController, Flow, ...registerables);

export default {
    data() {
        return {
            windowSize: 1,
            minOccurrences: 2,
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
            let words = new Set();
            for (let key in this.probabilities) {
                words.add(key);
            }
            return Array.from(words);
        },
        toWords() {
            let words = new Set()
            for (let key in this.probabilities) {
                for (let key2 in this.probabilities[key]) {
                    words.add(key2)
                }
            }
            return Array.from(words);
        },
        flows() {
            console.log(this.probabilities)
            let flows = []
            for (let k of this.fromWords) {
                for (let k2 of this.toWords) {
                    if (k in this.probabilities && k2 in this.probabilities[k]) {
                        flows.push({
                            from: k,
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
            console.log(this.flows)
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
                    animation: false
                }
            });
            setTimeout(() => {
                var link = document.createElement('a');
                link.download = 'chart.png';
                link.href = this.$refs.chart.toDataURL()
                link.click();
            }, 5000)
        }
    },
}
</script>

<template>
<div>
    <h3>Åben generation spil</h3>
    <p class="mb-5">
        Udforsk alle de generationsmetoder, vi har talt om indtil videre! <br>
        Du kan vælge datasæt, metode og vinduesstørrelse i menuen nedenfor. Hvis du ikke er sikker på, hvad noget betyder, skal du holde markøren over det, og du kan se en forklaring. <br>
        Derefter kan du generere en sætning, et ord ad gangen, baseret på alle vores teknikker. <br>
    </p>
    <div class="border border-dark rounded p-3 m-3">
        <h5 class="mt-3">Generer frit din egen, nye sætning her!</h5>
        <div class="row">
            <div class="col">
                <div class="my-2">
                    <b>Vælg et datasæt:</b>
                    <div class="btn-group">
                        <button :title="descriptionLookup[dataset]" v-for="(dataset, index) in datasets" :key="index" :class="['btn', 'btn-' + datasetButtonColor[dataset], { 'border border-4 border-dark': selectedDataset === dataset }]" @click="selectDataset(dataset)">
                            {{ dataset + (selectedDataset === dataset ? ' (valgt)' : '') }}
                        </button>
                    </div>
                </div>
                <div class="my-2">
                    <b>Vælg en metode:</b>
                    <div class="btn-group">
                        <button :title="descriptionLookup[method]" v-for="(method, index) in methods" :key="index" :class="['btn', 'btn-light', { 'border border-4 border-dark': selectedMethod === method }]" @click="selectMethod(method)">
                            {{ method + (selectedMethod === method ? ' (valgt)' : '') }}
                        </button>
                    </div>
                </div>
                <div class="my-2">
                    <b>Vælg en vinduesstørrelse{{ usesWindowSize? '' : ' (ikke brugt i denne metode)'}}:</b>
                    <div>
                        1<input type="range" v-model="windowSize" min="1" max="5" :disabled="!usesWindowSize" />5
                    </div>
                </div>
                <div class="my-2">
                    <b>Sandsynligheder:</b>
                    <div class="d-flex justify-content-center align-items-center" style="max-height: 30vh;">
                        <Pie :data="pieChartData" :options="chartOptions" />
                    </div>
                </div>
                <button v-if="('x'+generatedSentence.map(x=>x.word).join()).slice(-1)[0] === '.'" class="btn btn-success" disabled>Du genererede et punktum. Ryd sætningen for at prøve igen.</button>
                <button v-else class="btn btn-success" @click="generateCurrWord">Generer næste ord</button>
            </div>

            <div class="col">
                <button class="btn btn-danger" @click="clearGeneratedSentence">Ryd sætning</button>
                <div class="border border-dark rounded p-3 m-3">
                    <span v-for="(word, i) in generatedSentence" :key="i">
                        <button :class="['btn', 'btn-' + datasetButtonColor[word.dataset], 'p-1', 'm-1']" disabled>{{ word.word }}</button>
                    </span>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<script>
import {
    fiveStarData,
    oneStarData,
    subtitleData
} from '../datasets.js'
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

ChartJS.defaults.font.size = 10

ChartJS.register(ArcElement, Tooltip, Legend, Colors)

export default {
    components: {
        Pie
    },
    props: {
        allSentences: {
            type: Array,
        },
    },
    computed: {
        usesWindowSize() {
            return this.methods.slice(0, 3).includes(this.selectedMethod)
        },
        genResult() {
            let currDataset = this.datasetLookup[this.selectedDataset]
            let currMethod = this.methodLookup[this.selectedMethod]
            let prevN = this.generatedSentence.map((x) => x.word).slice(-1 * this.windowSize)
            while (prevN.length < this.windowSize) {
                prevN.unshift(".")
            }
            return currMethod(currDataset, prevN, this.selectedDataset, this.generatedSentence.length)
        },
        allProbs() {
            return this.genResult.probs
        },
        allProbsWithOther() {
            let allProbsWithOther = this.allProbs
            if (this.allProbs.length > 5) {
                allProbsWithOther = this.allProbs.slice(0, 5)
                allProbsWithOther.push(['Andre', this.allProbs.slice(5).reduce((a, [, b]) => a + b, 0)])
            }
            return allProbsWithOther
        },
        pieChartData() {
            return {
                labels: this.allProbsWithOther.map((x) => x[0]),
                datasets: [{
                    data: this.allProbsWithOther.map((x) => x[1]),
                    backgroundColor: this.pieChartColors
                }]
            }
        },
    },
    data() {
        return {
            datasetButtonColor: {
                'Indsendte sætninger': 'primary',
                '5-stjerne anmeldelser': 'success',
                '1-stjerne anmeldelser': 'warning',
                'Undertekster til film og tv': 'secondary',
            },
            datasets: [
                'Indsendte sætninger',
                '5-stjerne anmeldelser',
                '1-stjerne anmeldelser',
                'Undertekster til film og tv',
            ],
            datasetLookup: {
                'Indsendte sætninger': fiveStarData,
                '5-stjerne anmeldelser': fiveStarData,
                '1-stjerne anmeldelser': oneStarData,
                'Undertekster til film og tv': subtitleData,
            },
            selectedDataset: 'Indsendte sætninger',
            methods: [
                'Vælg højeste AKA grådig',
                'Vægtet tilfældig',
                'Tilfældig',
                'Mest almindelig',
                'Mest almindelig ved position'
            ],
            methodLookup: {
                'Vælg højeste AKA grådig': this.greedyGen,
                'Vægtet tilfældig': this.randomGen,
                'Tilfældig': this.completeRandomGen,
                'Mest almindelig': this.mostCommonGen,
                'Mest almindelig ved position': this.mostCommonAtPosGen
            },
            selectedMethod: 'Vælg højeste AKA grådig',
            descriptionLookup: {
                'Indsendte sætninger': 'Generation vil være baseret på alles sætninger fra i dag',
                '5-stjerne anmeldelser': 'Generation vil være baseret på 500 5-stjernede anmeldelser fra tripadvisor',
                '1-stjerne anmeldelser': 'Generation vil være baseret på 500 1-stjernede anmeldelser fra tripadvisor',
                'Undertekster til film og tv': 'Generation vil være baseret på 500 tilfældigt udvalgte undertekster fra film og tv-serier',
                'Vælg højeste AKA grådig': 'Den grådige metode vælger altid det mest sandsynlige ord til at følge de foregående N ord',
                'Vægtet tilfældig': 'Den vægtede tilfældige metode vælger det næste ord fra alle ord, der fulgte de foregående N ord tilfældigt, men sandsynligheden er proportional med, hvor almindeligt ordet var. Så hvis "er" dukkede op to gange efter "jeg" og "har" dukkede op én gang, ville "er" blive valgt 2/3 af tiden og "har" valgt 1/3 af tiden.',
                'Tilfældig': 'Den tilfældige metode vælger det næste ord blandt alle ord, der fulgte de foregående N ord tilfældigt, med fuldstændig lige stor sandsynlighed for hvert muligt ord',
                'Mest almindelig': 'Den mest almindelige metode vælger altid det mest almindelige ord overordnet i datasættet.',
                'Mest almindelig ved position': 'Den mest almindelige ved position metode vælger altid det mest almindelige ord på den aktuelle position i datasættet. (dvs. hvis du er på dit femte ord, vil det vælge det mest almindelige femte ord af sætninger i datasættet',
            },
            windowSize: 3,
            pieChartColors: [
                '#e41a1c',
                '#377eb8',
                '#4daf4a',
                '#984ea3',
                '#ff7f00',
                '#bbb'
            ],
            generatedSentence: [],
        };
    },
    methods: {
        clearGeneratedSentence() {
            this.generatedSentence = []
        },
        selectDataset(dataset) {
            this.selectedDataset = dataset
        },
        selectMethod(method) {
            this.selectedMethod = method
        },
        mode(arr) {
            return arr.sort((a, b) =>
                arr.filter(v => v === a).length -
                arr.filter(v => v === b).length
            ).pop();
        },
        getSubmittedData() {
            let sentences = this.allSentences
            let maxLen = Math.max(...sentences.map((sentence) => sentence.split(' ').length + 1))

            let wordCounts = {};
            for (let sentence of sentences) {
                let words = sentence.split(' ');
                while (words.length < maxLen) {
                    words.push('.');
                }
                for (let i = 0; i < words.length; i++) {
                    let word = words[i];
                    if (!wordCounts[i]) wordCounts[i] = {};
                    wordCounts[i][word] = wordCounts[i][word] ? wordCounts[i][word] + 1 : 1;
                }
            }
            let mostCommonWordsList = [];
            for (let i = 0; i < Object.keys(wordCounts).length; i++) {
                let words = Object.entries(wordCounts[i]);
                let max = Math.max(...words.map(([, count]) => count));
                let mostCommonWord = words.find(([, count]) => count === max)[0];
                if (mostCommonWord == '.') break;
                mostCommonWordsList.push(mostCommonWord);
            }

            console.log({
                'number_of_sentences': sentences.length,
                'all_sentences': sentences,
                'avg_sentence_length': Math.round(sentences.map(x=>x.split(" ").length).reduce((total, num) => total + num, 0) / sentences.length),
                'max_sentence_length': maxLen,
                'most_common_word': this.mode(sentences.map((x) => x.split(" ")).flat()),
                'most_common_word_at_position': mostCommonWordsList,
                'sliding_window': [1,2,3,4,5].map(x => this.slidingWindow(sentences, x))
            })

            return {
                'number_of_sentences': sentences.length,
                'all_sentences': sentences,
                'avg_sentence_length': Math.round(sentences.map(x=>x.split(" ").length).reduce((total, num) => total + num, 0) / sentences.length),
                'max_sentence_length': maxLen,
                'most_common_word': this.mode(sentences.map((x) => x.split(" ")).flat()),
                'most_common_word_at_position': mostCommonWordsList,
                'sliding_window': [1,2,3,4,5].map(x => this.slidingWindow(sentences, x))
            }
        },
        slidingWindow(sentences, N) {
            let probabilities = {}
            for (let s of sentences) {
                let prevN = []
                for (let i = 0; i < N; i++) {
                    prevN.push(".")
                }
                for (let x of s.split(" ")) {
                    if (prevN.join(" ") in probabilities) {
                        probabilities[prevN.join(" ")].push(x)
                    } else {
                        probabilities[prevN.join(" ")] = [x]
                    }
                    prevN.shift()
                    prevN.push(x)
                }
                if (prevN.join(" ") in probabilities) {
                    probabilities[prevN.join(" ")].push(".")
                } else {
                    probabilities[prevN.join(" ")] = ["."]
                }
            }
            for (let key in probabilities) {
                let currList = probabilities[key]
                let counts = {}
                for (let x of currList) {
                    if (x in counts) {
                        counts[x] += 1
                    } else {
                        counts[x] = 1
                    }
                }
                probabilities[key] = Object.entries(counts).sort((a, b) => b[1] - a[1])
            }
            return probabilities
        },
        generateCurrWord() {
            console.log(this.genResult)
            this.generatedSentence = [...this.generatedSentence, this.genResult]
            console.log(this.generatedSentence)
        },
        greedyGen(dataset, prevN, datasetName) {
            if (!([prevN.join(" ")] in dataset['sliding_window'][prevN.length - 1])) {
                return {
                    word: ".",
                    probs: [
                        [".", 1]
                    ],
                    dataset: datasetName
                }
            }
            return {
                word: dataset['sliding_window'][prevN.length - 1][prevN.join(" ")][0][0],
                probs: dataset['sliding_window'][prevN.length - 1][prevN.join(" ")],
                dataset: datasetName
            }
        },
        randomGen(dataset, prevN, datasetName) {
            if (!([prevN.join(" ")] in dataset['sliding_window'][prevN.length - 1])) {
                return {
                    word: ".",
                    probs: [
                        [".", 1]
                    ],
                    dataset: datasetName
                }
            }
            return {
                word: this.getRandomKeyProportionateToValue(dataset['sliding_window'][prevN.length - 1][prevN.join(" ")]),
                probs: dataset['sliding_window'][prevN.length - 1][prevN.join(" ")],
                dataset: datasetName
            }
        },
        completeRandomGen(dataset, prevN, datasetName) {
            if (!([prevN.join(" ")] in dataset['sliding_window'][prevN.length - 1])) {
                return {
                    word: ".",
                    probs: [
                        [".", 1]
                    ],
                    dataset: datasetName
                }
            }
            return {
                word: this.getRandomKey(dataset['sliding_window'][prevN.length - 1][prevN.join(" ")]),
                probs: dataset['sliding_window'][prevN.length - 1][prevN.join(" ")],
                dataset: datasetName
            }
        },
        mostCommonGen(dataset, prevN, datasetName) {
            return {
                word: dataset['most_common_word'],
                probs: [
                    [dataset['most_common_word'], 1]
                ],
                dataset: datasetName
            }
        },
        mostCommonAtPosGen(dataset, prevN, datasetName, pos) {
            if (pos >= dataset['most_common_word_at_position'].length) {
                return {
                    word: ".",
                    probs: [
                        [".", 1]
                    ],
                    dataset: datasetName
                }
            }
            return {
                word: dataset['most_common_word_at_position'][pos],
                probs: [
                    [dataset['most_common_word_at_position'][pos], 1]
                ],
                dataset: datasetName
            }
        },
        getRandomKeyProportionateToValue(tuple_list) {
            let totalSum = 0;
            for (let x of tuple_list) {
                totalSum += x[1];
            }

            const randomNum = Math.random() * totalSum;

            let currentSum = 0;
            for (let x of tuple_list) {
                currentSum += x[1];
                if (randomNum < currentSum) {
                    return x[0];
                }
            }
        },
        getRandomKey(tuple_list) {
            return tuple_list[Math.floor(Math.random() * tuple_list.length)][0]
        },
    },
    watch: {
        allSentences() {
            this.datasetLookup['Indsendte sætninger'] = this.getSubmittedData()
        },
    },
};
</script>

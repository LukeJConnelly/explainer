<template>
<div>
    <h3>Free generation game</h3>
    <p class="mb-5">
        Explore all the generation methods we've talked about so far! <br>
        You can select the dataset, method, and window size in the menu below. If you're not sure what something means, hover over it and you can see an explanation. <br>
        Then, you can generate a sentence one word at a time based on all our techniques. <br>
    </p>
    <div class="border border-dark rounded p-3 m-3">
        <h5 class="mt-3">Freely generate your own, new sentence here!</h5>
        <div class="row">
            <div class="col">
                <div class="my-2">
                    <b>Select a dataset:</b>
                    <div class="btn-group">
                        <button :title="descriptionLookup[dataset]" v-for="(dataset, index) in datasets" :key="index" :class="['btn', 'btn-' + datasetButtonColor[dataset], { 'border border-4 border-dark': selectedDataset === dataset }]" @click="selectDataset(dataset)">
                            {{ dataset + (selectedDataset === dataset ? ' (current)' : '') }}
                        </button>
                    </div>
                </div>
                <div class="my-2">
                    <b>Select a method:</b>
                    <div class="btn-group">
                        <button :title="descriptionLookup[dataset]" v-for="(method, index) in methods" :key="index" :class="['btn', 'btn-light', { 'border border-4 border-dark': selectedMethod === method }]" @click="selectMethod(method)">
                            {{ method + (selectedMethod === method ? ' (current)' : '') }}
                        </button>
                    </div>
                </div>
                <div class="my-2">
                    <b>Select a window Size{{ usesWindowSize? '' : ' (not used in this method)'}}:</b>
                    <div>
                        1<input type="range" v-model="windowSize" min="1" max="5" :disabled="!usesWindowSize" />5
                    </div>
                </div>
                <div class="my-2">
                    <b>Probabilities:</b>
                    <div class="d-flex justify-content-center align-items-center" style="max-height: 30vh;">
                        <Pie :data="pieChartData" :options="chartOptions" />
                    </div>
                </div>
                <button v-if="('x'+generatedSentence.map(x=>x.word).join()).slice(-1)[0] === '.'" class="btn btn-success" disabled>You generated a full-stop. Clear the sentence to try again</button>
                <button v-else class="btn btn-success" @click="generateCurrWord">Generate Next Word</button>
            </div>

            <div class="col">
                <button class="btn btn-danger" @click="clearGeneratedSentence">Clear Sentence</button>
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
                allProbsWithOther.push(['Others', this.allProbs.slice(5).reduce((a, [, b]) => a + b, 0)])
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
                'Submitted Sentences': 'primary',
                'Five Star Reviews': 'success',
                'One Star Reviews': 'warning',
                'Movie & TV Subtitles': 'secondary',
            },
            datasets: [
                'Submitted Sentences',
                'Five Star Reviews',
                'One Star Reviews',
                'Movie & TV Subtitles',
            ],
            datasetLookup: {
                'Submitted Sentences': fiveStarData,
                'Five Star Reviews': fiveStarData,
                'One Star Reviews': oneStarData,
                'Movie & TV Subtitles': subtitleData,
            },
            selectedDataset: 'Submitted Sentences',
            methods: [
                'Greedy',
                'Weighted Random',
                'Random',
                'Most Common',
                'Most Common at Position'
            ],
            methodLookup: {
                'Greedy': this.greedyGen,
                'Weighted Random': this.randomGen,
                'Random': this.completeRandomGen,
                'Most Common': this.mostCommonGen,
                'Most Common at Position': this.mostCommonAtPosGen
            },
            selectedMethod: 'Greedy',
            descriptionLookup: {
                'Submitted Sentences': 'Generation will be based on everyones sentences from today',
                'Five Star Reviews': 'Generation will be based on 500 five star reviews from tripadvisor',
                'One Star Reviews': 'Generation will be based on 500 one star reviews from tripadvisor',
                'Movie & TV Subtitles': 'Generation will be based on 500 randomly selected subtitles from movies and TV shows',
                'Greedy': 'The greedy method always chooses the most likely word to follow the previous N words.',
                'Weighted Random': 'The weighted random method chooses the next word from all words which followed the previous N words randomly, but the probability is proportional to how common the word was. So if er appeared twice after jeg and har appeared once, er would be chosen 2/3 of the time and har would be chosen 1/3 of the time.',
                'Random': 'The random method chooses the next word from all words which followed the previous N words randomly, with completely equal probability for each possible word.',
                'Most Common': 'The most common method always chooses the most common word overall in the dataset.',
                'Most Common at Position': 'The most common at position method always chooses the most common word at the current position in the dataset. (ie. if youre on your fifth word, it will choose the most common fifth word of sentences in the dataset',
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
            this.datasetLookup['Submitted Sentences'] = this.getSubmittedData()
        },
    },
};
</script>

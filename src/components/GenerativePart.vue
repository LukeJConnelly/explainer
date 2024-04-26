<template>
<div>
    <!-- States: "mode", "mode-by-pos", "ngram", "rand" -->
    <h3>Generering af tekst</h3>
    <p>
        På denne side vil vi generere tekst ved hjælp af de data, vi har indsamlet.
        Hver boks repræsenterer en ny generation metode. Ved at klikke på "generer" oprettes en sætning ved brug af metoden.
        Efter generering vil du også være i stand til at klikke på en "hvordan"-knap for at se cirkeldiagrammer, der repræsenterer de sandsynligheder/faktorer, der bruges til at træffe beslutninger.
        Her er den første teknik:
    </p>
    <div class="border border-dark rounded p-3 m-3">
        <GenerateAnimation :textToShow="mostCommonWordInEveryPosition" :generateFn="getMostCommonWordInEveryPosition" :techniqueName="techniques['mode'][0]" :techniqueDescription="techniques['mode'][1]"></GenerateAnimation>
    </div>
    <div class="border border-dark rounded p-3 m-3" v-if="mostCommonWordInEveryPosition.length && stateOk('mode-by-pos')">
        <GenerateAnimation :textToShow="mostCommonWordAtEachPosition" :generateFn="getMostCommonWordAtEachPosition" :techniqueName="techniques['pos'][0]" :techniqueDescription="techniques['pos'][1]"></GenerateAnimation>
    </div>
    <div class="border border-dark rounded p-3 m-3" v-if="mostCommonWordAtEachPosition.length  && stateOk('ngram')">
        <h5 class="mt-3">Mest almindeligt efter tidligere {{windowSize}}-ord-vindue</h5>
        <label>Vælg vinduesstørrelsen:</label>
        <span class="my-2">
            1<input type="range" v-model="windowSize" min="1" max="5" />5
        </span>
        <GenerateAnimation :textToShow="sliding" :generateFn="getSliding" :techniqueName="techniques['ngram'][0]" :techniqueDescription="techniques['ngram'][1]"></GenerateAnimation>
    </div>
    <div class="border border-dark rounded p-3 m-3" v-if="sliding.length  && stateOk('rand')">
        <h5 class="mt-3">Tilfældig valg fra alle ord der fulgte den tidligere {{windowSize}}-ord-vindue</h5>
        <label>Vælg vinduesstørrelsen:</label>
        <span class="my-2">
            1<input type="range" v-model="randomWindowSize" min="1" max="5" />5
        </span>
        <GenerateAnimation :textToShow="slidingRandom" :generateFn="getSlidingRandom"  :techniqueName="techniques['rand'][0]" :techniqueDescription="techniques['rand'][1]"></GenerateAnimation>
    </div>
    <button class="btn btn-primary mb-3" v-if="slidingRandom.length" @click="moveOn()" :disabled="!stateOk('sankey')">{{ stateOk('sankey') ? 'Fortsæt' : 'Vent venligst...' }}</button>
</div>
</template>

<script>
import GenerateAnimation from './GenerateAnimation.vue';

export default {
    components: {
        GenerateAnimation
    },
    props: {
        allSentences: {
            type: Array,
        },
        currState: {
            type: String,
        },
        states: {
            type: Array,
        },
    },
    data() {
        return {
            mostCommonWordInEveryPosition: [],
            mostCommonWordAtEachPosition: [],
            sliding: [],
            slidingRandom: [],
            windowSize: 2,
            randomWindowSize: 3,
            pieChartColors: [
                '#e41a1c',
                '#377eb8',
                '#4daf4a',
                '#984ea3',
                '#ff7f00',
                '#bbb'
            ],
            techniques: {
                'mode': ['Mest almindelig', 'Denne teknik vil altid vælge det mest almindelige ord i alle sætninger'],
                'pos': ['Positionelt mest almindelige ord', 'Denne teknik vælger det mest almindelige ord på hver position (mest almindelige 1. ord, mest almindelige 2. ord...)'],
                'ngram': ['', 'Denne teknik vælger det mest almindelige ord til at følge de foregående N ord (som vi kalder et vindue her), hvor N kan være et hvilket som helst tal. Du kan vælge dette N ved at bruge skyderen ovenfor.'],
                'rand': ['', 'Denne teknik vælger et tilfældigt ord, som fulgte de foregående N ord. Vælg N ved at bruge skyderen ovenfor.'],
            },
        };
    },
    methods: {
        moveOn() {
            this.$router.push({
                path: 'sankey',
            })
        },
        stateOk(s) {
            return this.states.indexOf(this.currState) >= this.states.indexOf(s)
        },
        getOtheredProbs(probs) {
            let allProbsWithOther = probs
            if (probs.length > 5) {
                allProbsWithOther = probs.slice(0, 5)
                allProbsWithOther.push(['Andre', probs.slice(5).reduce((a, [, b]) => a + b, 0)])
            }
            return allProbsWithOther
        },
        getMostCommonWordInEveryPosition() {
            let wordCounts = {};
            let maxSentenceLength = Math.max(...this.allSentences.map((sentence) => sentence.split(' ').length + 1));
            for (let sentence of this.allSentences) {
                let words = sentence.split(' ');
                for (let w of words) {
                    wordCounts[w] = wordCounts[w] ? wordCounts[w] + 1 : 1;
                }
            }
            let allProbs = Object.entries(wordCounts).sort(([, a], [, b]) => b - a)
            let allProbsWithOther = this.getOtheredProbs(allProbs)
            let mostCommonWord = allProbs[0][0];
            let filledArray = []
            for (let i = 0; i < maxSentenceLength; i++) {
                filledArray.push(mostCommonWord)
            }
            this.mostCommonWordInEveryPosition = filledArray.concat('.').map((word, i) => ({
                word,
                pos: i,
                show: false,
                count: wordCounts[word],
                hasPie: i < maxSentenceLength,
                backgroundColor: this.pieChartColors[allProbsWithOther.findIndex(([w]) => w == word)],
                pieChartData: {
                    labels: allProbsWithOther.map((x) => x[0]),
                    datasets: [{
                        data: allProbsWithOther.map((x) => x[1]),
                        backgroundColor: this.pieChartColors
                    }]
                }
            }));
            for (let i in this.mostCommonWordInEveryPosition) {
                setTimeout(() => {
                    this.mostCommonWordInEveryPosition[i].show = true;
                }, i * 1000);
            }
        },
        getMostCommonWordAtEachPosition() {
            let wordCounts = {};
            let maxSentenceLength = Math.max(...this.allSentences.map((sentence) => sentence.split(' ').length + 1));
            for (let sentence of this.allSentences) {
                let words = sentence.split(' ');
                while (words.length < maxSentenceLength) {
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
                let allProbs = words.sort(([, a], [, b]) => b - a)
                let allProbsWithOther = this.getOtheredProbs(allProbs)
                mostCommonWordsList.push({
                    word: mostCommonWord,
                    count: max,
                    probs: allProbsWithOther
                });
                if (mostCommonWord == '.') break;
            }
            this.mostCommonWordAtEachPosition = mostCommonWordsList.map((word, i) => ({
                word: word.word,
                pos: i,
                show: false,
                count: word.count,
                hasPie: true,
                backgroundColor: this.pieChartColors[word.probs.findIndex(([w]) => w == word.word)],
                pieChartData: {
                    labels: word.probs.map((x) => x[0]),
                    datasets: [{
                        data: word.probs.map((x) => x[1]),
                        backgroundColor: this.pieChartColors
                    }]
                }
            }));
            for (let i in this.mostCommonWordAtEachPosition) {
                setTimeout(() => {
                    this.mostCommonWordAtEachPosition[i].show = true;
                }, i * 1000);
            }
        },
        getSliding() {
            let slidingResult = this.greedyChoice(this.slidingWindow(this.windowSize))
            this.sliding = slidingResult.map((word, i) => ({
                word: word.word,
                pos: i,
                show: false,
                count: word.probs[0][1],
                prevN: word.prevN,
                hasPie: true,
                backgroundColor: this.pieChartColors[word.probs.findIndex(([w]) => w == word.word)],
                pieChartData: {
                    labels: this.getOtheredProbs(word.probs).map((x) => x[0]),
                    datasets: [{
                        data: this.getOtheredProbs(word.probs).map((x) => x[1]),
                        backgroundColor: this.pieChartColors
                    }]
                }
            }));
            for (let i in this.sliding) {
                setTimeout(() => {
                    this.sliding[i].show = true;
                }, i * 1000);
            }
        },
        getSlidingRandom() {
            let slidingResult = this.randomChoice(this.slidingWindow(this.randomWindowSize))
            this.slidingRandom = slidingResult.map((word, i) => ({
                word: word.word,
                pos: i,
                show: false,
                count: word.probs[0][1],
                prevN: word.prevN,
                hasPie: true,
                backgroundColor: this.pieChartColors[word.probs.findIndex(([w]) => w == word.word)],
                pieChartData: {
                    labels: this.getOtheredProbs(word.probs).map((x) => x[0]),
                    datasets: [{
                        data: this.getOtheredProbs(word.probs).map((x) => x[1]),
                        backgroundColor: this.pieChartColors
                    }]
                }
            }));
            for (let i in this.slidingRandom) {
                setTimeout(() => {
                    this.slidingRandom[i].show = true;
                }, i * 1000);
            }
        },
        greedyChoice(probabilities) {
            let N = Object.keys(probabilities)[0].split(' ').length
            let prevN = []
            for (let i = 0; i < N; i++) {
                prevN.push(".")
            }
            let sentence = []
            let nextWord = Object.entries(probabilities[prevN.join(" ")]).reduce((a, b) => a[1] > b[1] ? a : b)[0]
            while (nextWord !== "." && sentence.length < 40) {
                sentence.push({
                    word: nextWord,
                    probs: Object.entries(probabilities[prevN.join(" ")]).sort(([, a], [, b]) => b - a),
                    prevN: prevN.join(" ")
                })
                prevN.shift()
                prevN.push(nextWord)
                nextWord = Object.entries(probabilities[prevN.join(" ")]).reduce((a, b) => a[1] > b[1] ? a : b)[0]
            }
            sentence.push({
                word: nextWord,
                probs: Object.entries(probabilities[prevN.join(" ")]).sort(([, a], [, b]) => b - a),
                prevN: prevN.join(" ")
            })
            return sentence
        },
        getRandomKeyProportionateToValue(dictionary) {
            let totalSum = 0;
            for (let key in dictionary) {
                totalSum += dictionary[key];
            }

            const randomNum = Math.random() * totalSum;

            let currentSum = 0;
            for (let key in dictionary) {
                currentSum += dictionary[key];
                if (randomNum < currentSum) {
                    return key;
                }
            }
        },
        randomChoice(probabilities) {
            let N = Object.keys(probabilities)[0].split(' ').length
            let prevN = []
            for (let i = 0; i < N; i++) {
                prevN.push(".")
            }
            let sentence = []
            let nextWord = this.getRandomKeyProportionateToValue(probabilities[prevN.join(" ")])
            while (nextWord !== ".") {
                sentence.push({
                    word: nextWord,
                    probs: Object.entries(probabilities[prevN.join(" ")]).sort(([, a], [, b]) => b - a),
                    prevN: prevN.join(" ")
                })
                prevN.shift()
                prevN.push(nextWord)
                nextWord = this.getRandomKeyProportionateToValue(probabilities[prevN.join(" ")])
            }
            sentence.push({
                word: nextWord,
                probs: Object.entries(probabilities[prevN.join(" ")]).sort(([, a], [, b]) => b - a),
                prevN: prevN.join(" ")
            })
            return sentence
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
        }
    },
};
</script>

<template>
<div>
    <h3>Word Clouds</h3>
    <p>
        Now, we'd like to look at the sentences we recieved as a word cloud. <br>
        A word cloud is a visual representation of the words in a sentence, with the size of the word representing how often it appears in the sentence. <br>
        The bigger the word, the more often it was in the original text. <br>
        There are some options for customisation available at the bottom of the page :)
    </p>
    <h4 class="mt-4">Your Personal Word Cloud</h4>
    <p>
        This is your cleaned sentence as a word cloud
    </p>
    <div class="p-5 border border-3 border-dark rounded mx-auto mb-5" style="width: 20vw; height: 20vw;">
        <vue-word-cloud :spacing="1/2" :words="countOccurences(sentence.split(' '))" :color="([, weight]) => getColour(weight, maxYourSentence)" font-family="JetBrains Mono" />
    </div>
    <h4 class="mt-4">The Groups Word Cloud</h4>
    <p>
        This is everyones cleaned sentence joined together as a word cloud. So, the bigger the word, the more often it was in everyones sentences.<br>
        This is a good way to see what everyone has in common, and what makes everyone unique.
    </p>
    <div class="p-5 border border-3 border-dark rounded mx-auto" style="width: 40vw; height: 40vw;">
        <vue-word-cloud :spacing="1/2" :words="countOccurences(allSentences.join(' ').split(' '))" :color="([, weight]) => getColour(weight, maxAllSentences)" font-family="JetBrains Mono" />
    </div>
    <div class="my-5">
        <h4 class="p-2">Options</h4>
        <div class="my-2 mb-5">
            <label for="stopwords">
                <h5>Exclude stop words:</h5>
            </label>
            <input id="stopwords" type="checkbox" v-model="excludeStopWords">
            <p class="my-1">
                This means excluding common words that don't really have much meaning to a text (like "jeg", "og", "er", etc.)
            </p>
        </div>
        <p>
            Here you can pick the colour of the smallest words in the word clouds (words that appeared least frequently in the sentences)
        </p>
        <div class="row d-flex align-items-center justify-content-center pb-3 mb-1">
            <div style="width: 50px; height: 50px; border: solid black 3px; border-radius: 5px;" :style="{'background-color': `rgb(${minColor.map(num => num).join(',')})`}"></div>
            <div class="col">
                <label for="redmin">Red:</label>
                <input type="range" id="redmin" v-model.number="minColor[0]" min="0" max="255">
            </div>
            <div class="col">
                <label for="greenmin">Green:</label>
                <input type="range" id="greenmin" v-model.number="minColor[1]" min="0" max="255">
            </div>
            <div class="col">
                <label for="bluemin">Blue:</label>
                <input type="range" id="bluemin" v-model.number="minColor[2]" min="0" max="255">
            </div>
        </div>
        <p>
            Here you can pick the colour of the largest words in the word clouds (words that were common in the sentences)
        </p>
        <div class="row d-flex align-items-center justify-content-center pb-3">
            <div style="width: 50px; height: 50px; border: solid black 3px; border-radius: 5px;" :style="{'background-color': `rgb(${maxColor.map(num => num).join(',')})`}"></div>
            <div class="col">
                <label for="redmax">Red:</label>
                <input type="range" id="redmax" v-model.number="maxColor[0]" min="0" max="255">
            </div>
            <div class="col">
                <label for="greenmax">Green:</label>
                <input type="range" id="greenmax" v-model.number="maxColor[1]" min="0" max="255">
            </div>
            <div class="col">
                <label for="bluemin">Blue:</label>
                <input type="range" id="bluemax" v-model.number="maxColor[2]" min="0" max="255">
            </div>
        </div>
    </div>
    <button class="btn btn-primary mb-3" @click="moveOn()" :disabled="!canAdvance">{{ canAdvance ? 'Continue' : 'Please Wait...' }}</button>
</div>
</template>

<style>
input {
    vertical-align: -2px;
}
</style>

<script>
import VueWordCloud from 'vuewordcloud';
import {
    stopWords
} from '../stopwords.js';

export default {
    components: {
        'vue-word-cloud': VueWordCloud,
    },
    data() {
        return {
            minColor: [0, 0, 255],
            maxColor: [255, 0, 0],
            excludeStopWords: false
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
        sentence() {
            return this.$route.query.sentence
        },
        maxYourSentence() {
            return Math.max(...this.countOccurences(this.sentence.split(' ')).map(([, weight]) => weight));
        },
        maxAllSentences() {
            return Math.max(...this.countOccurences(this.allSentences.join(' ').split(' ')).map(([, weight]) => weight));
        },
        canAdvance() {
            return this.states.indexOf(this.currState) > this.states.indexOf('cloud')
        }
    },
    methods: {
        moveOn() {
            this.$router.push({
                path: 'generative',
            })
        },
        countOccurences(wordList) {
            let counts = {};
            for (let word of wordList) {
                if (this.excludeStopWords && stopWords.includes(word))
                    continue
                counts[word] = counts[word] ? counts[word] + 1 : 1;
            }
            return Object.entries(counts);
        },
        getColour(weight, max) {
            let percentage = weight / max;

            let color = this.minColor.map((minComponent, index) => {
                const maxComponent = this.maxColor[index];
                const interpolatedComponent = Math.round(
                    minComponent + percentage * (maxComponent - minComponent)
                );
                return interpolatedComponent;
            });

            return `rgb(${color.join(',')})`;
        }
    }
}
</script>

<template>
<div>
    <h3>Word Clouds</h3>
    <p>
        Nu vil vi gerne se på de sætninger, vi modtog, som en word cloud. <br>
        En word cloud er en visuel repræsentation af ordene i en sætning, hvor størrelsen af ordet repræsenterer, hvor ofte det optræder i sætningen. <br>
        Jo større ord, jo oftere var det i den originale tekst. <br>
        Der er nogle muligheder for tilpasning nederst på siden :)
    </p>
    <h4 class="mt-4">Din personlige Word Cloud</h4>
    <p>
        Dette er din rensede sætning som en word cloud
    </p>
    <div class="p-5 border border-3 border-dark rounded mx-auto mb-5" style="width: 20vw; height: 20vw;">
        <vue-word-cloud :spacing="1/2" :words="countOccurences(sentence.split(' '))" :color="([, weight]) => getColour(weight, maxYourSentence)" font-family="JetBrains Mono" />
    </div>
    <h4 class="mt-4">Gruppens Word Cloud</h4>
    <p>
        Dette er alles rensede sætninger sammensat som en word cloud. Så jo større ordet er, jo oftere var det i alles sætninger.<br>
        Dette er en god måde at se, hvad alle har til fælles, og hvad der gør alle unikke.
    </p>
    <div class="p-5 border border-3 border-dark rounded mx-auto" style="width: 40vw; height: 40vw;">
        <vue-word-cloud :spacing="1/2" :words="countOccurences(allSentences.join(' ').split(' '))" :color="([, weight]) => getColour(weight, maxAllSentences)" font-family="JetBrains Mono" />
    </div>
    <div class="my-5">
        <h4 class="p-2">Muligheder</h4>
        <div class="my-2 mb-5">
            <label for="stopwords">
                <h5>Ekskluderer "stop" ord: </h5>
            </label>
            <input id="stopwords" type="checkbox" v-model="excludeStopWords">
            <p class="my-1">
                Det betyder, at man udelukker almindelige ord, der ikke rigtig har den store betydning for en tekst (såsom "jeg", "og", "er" osv.)
            </p>
        </div>
        <p>
            Her kan du vælge farven på de mindste ord i word cloudet (ord, der optrådte mindst hyppigt i sætningerne)
        </p>
        <div class="row d-flex align-items-center justify-content-center pb-3 mb-1">
            <div style="width: 50px; height: 50px; border: solid black 3px; border-radius: 5px;" :style="{'background-color': `rgb(${minColor.map(num => num).join(',')})`}"></div>
            <div class="col">
                <label for="redmin">Rød:</label>
                <input type="range" id="redmin" v-model.number="minColor[0]" min="0" max="255">
            </div>
            <div class="col">
                <label for="greenmin">Grøn:</label>
                <input type="range" id="greenmin" v-model.number="minColor[1]" min="0" max="255">
            </div>
            <div class="col">
                <label for="bluemin">Blå:</label>
                <input type="range" id="bluemin" v-model.number="minColor[2]" min="0" max="255">
            </div>
        </div>
        <p>
            Her kan du vælge farven på de største ord i word cloudet (ord, der var almindelige i sætningerne)
        </p>
        <div class="row d-flex align-items-center justify-content-center pb-3">
            <div style="width: 50px; height: 50px; border: solid black 3px; border-radius: 5px;" :style="{'background-color': `rgb(${maxColor.map(num => num).join(',')})`}"></div>
            <div class="col">
                <label for="redmax">Rød:</label>
                <input type="range" id="redmax" v-model.number="maxColor[0]" min="0" max="255">
            </div>
            <div class="col">
                <label for="greenmax">Grøn:</label>
                <input type="range" id="greenmax" v-model.number="maxColor[1]" min="0" max="255">
            </div>
            <div class="col">
                <label for="bluemin">Blå:</label>
                <input type="range" id="bluemax" v-model.number="maxColor[2]" min="0" max="255">
            </div>
        </div>
    </div>
    <button class="btn btn-primary mb-3" @click="moveOn()" :disabled="!canAdvance">{{ canAdvance ? 'Forsæt' : 'Vent venligst...' }}</button>
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

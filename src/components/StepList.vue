<template>
<div>
    <label>Your submitted sentence:</label>
    <p>{{ inputText }}</p>
</div>
<div v-if="stepNumber > 0">
    <label>As lowercase:</label>
    <p>{{ lower }}</p>
</div>
<div v-if="stepNumber > 1">
    <label>Without punctuation:</label>
    <p>{{ noPunctuation }}</p>
</div>
<div v-if="stepNumber > 2">
    <label>Without double spaces:</label>
    <p>{{ noDoubleSpaces }}</p>
</div>
<div v-if="stepNumber > 3">
    <label>Split by spaces:</label>
    <div>
        <button v-for="(word, index) in spaceSplit" :key="index" disabled class="btn btn-primary m-1">{{ word }}</button>
    </div>
</div>
<div v-if="stepNumber > 4">
    <label>As a word cloud:</label>
    <VueWordCloud style="
    height: 500px;
    width: 500px;
    margin: auto;
  " :words="spaceSplit" font-family="Roboto" />
</div>
<div v-if="stepNumber > 5">
    <label>Your sentence has been added to the list of all sentences...</label>
    <label>Here are the ten most common words:</label>
    <div>
        <button v-for="(word, index) in topNInDict(10, countOccurences(allWords))" :key="index" disabled class="btn btn-primary m-1">{{ word[0] }} ({{ word[1] }})</button>
    </div>
</div>
<div v-if="stepNumber > 6">
    <label>Here are all sentences as a word cloud:</label>
    <VueWordCloud style="
    height: 500px;
    width: 500px;
    margin: auto;
  " :words="dictToList(countOccurences(allWords))" font-family="Roboto" />
</div>
<div v-if="stepNumber > 7">
    <label>Lets remove common words:</label>
    <VueWordCloud style="
    height: 500px;
    width: 500px;
    margin: auto;
  " :words="dictToList(countOccurences(allWordsFiltered))" font-family="Roboto" />
</div>
<div v-if="stepNumber > 8">
    <h2>Lets try and do some generation</h2>
    <label>Lets take the most common word every time:</label>
    <br>
    <button v-for="(word, index) in generateMostCommonWord()" :key="index" disabled class="btn btn-primary m-1">{{ word[0] }}</button>
</div>
<div v-if="stepNumber > 9">
    <label>Lets take the most common word at each position:</label>
    <br>
    <button v-for="(word, index) in generateMostCommonWordInPosition()" :key="index" disabled class="btn btn-primary m-1">{{ word }}</button>
</div>
<div v-if="stepNumber > 10">
    <label>Lets try a 2-sliding window approach:</label>
    <br>
    <button v-for="(word, index) in greedyChoice(slidingWindow(2))" :key="index" disabled class="btn btn-primary m-1">{{ word }}</button>
</div>
<div v-if="stepNumber > 11">
    <label>Lets make that a 3-sliding window:</label>
    <br>
    <button v-for="(word, index) in greedyChoice(slidingWindow(3))" :key="index" disabled class="btn btn-primary m-1">{{ word }}</button>
</div>
<div v-if="stepNumber > 12">
    <label>Lets add randomness to that:</label>
    <br>
    <label>1st time</label><button v-for="(word, index) in randomChoice(slidingWindow(3))" :key="index" disabled class="btn btn-primary m-1">{{ word }}</button><br>
    <label>2nd time</label><button v-for="(word, index) in randomChoice(slidingWindow(3))" :key="index" disabled class="btn btn-primary m-1">{{ word }}</button><br>
    <label>3rd time</label><button v-for="(word, index) in randomChoice(slidingWindow(3))" :key="index" disabled class="btn btn-primary m-1">{{ word }}</button><br>
    <label>4th time</label><button v-for="(word, index) in randomChoice(slidingWindow(3))" :key="index" disabled class="btn btn-primary m-1">{{ word }}</button><br>
    <label>5th time</label><button v-for="(word, index) in randomChoice(slidingWindow(3))" :key="index" disabled class="btn btn-primary m-1">{{ word }}</button>
</div>
</template>

<script>
import VueWordCloud from 'vuewordcloud';

export default {
    name: 'StepList',
    components: {
        [VueWordCloud.name]: VueWordCloud,
    },
    props: {
        inputText: String,
        stepNumber: Number
    },
    computed: {
        lower() {
            return this.inputText.toLowerCase()
        },
        noPunctuation() {
            return this.lower.replace(/[.,/#!$%^&*;:{}=\-_`~()]/g, "")
        },
        noDoubleSpaces() {
            return this.noPunctuation.replace(/\s{2,}/g, " ")
        },
        spaceSplit() {
            return this.noDoubleSpaces.split(' ')
        },
        allWords() {
            return this.allTexts.reduce((acc, val) => {
                acc.push(...this.fullClean(val))
                return acc
            }, [])
        },
        allWordsFiltered() {
            return this.allWords.filter(word => !this.stopWords.includes(word))
        },
        avgSentenceLength() {
            return Math.floor(
                this.allTexts.reduce((total, sentence) => total + this.fullClean(sentence).length, 0) / this.allTexts.length
            );
        },
        maxSentenceLength() {
            return Math.max(...this.allTexts.map(sentence => this.fullClean(sentence).length))
        }
    },
    methods: {
        fullClean(s) {
            return s.toLowerCase().replace(/[.,/#!$%^&*;:{}=\-_`~()]/g, "").replace(/\s{2,}/g, " ").split(' ')
        },
        countOccurences(words) {
            return words.reduce((acc, val) => {
                if (acc[val]) {
                    acc[val]++
                } else {
                    acc[val] = 1
                }
                return acc
            }, {})
        },
        dictToList(dict) {
            return Object.keys(dict).map(key => {
                return [key, dict[key]]
            })
        },
        topNInDict(N, dict) {
            return Object.entries(dict).sort((a, b) => b[1] - a[1]).slice(0, N)
        },
        generateMostCommonWord() {
            return Array(this.avgSentenceLength).fill(this.topNInDict(1, this.countOccurences(this.allWords))[0])
        },
        generateMostCommonWordInPosition() {
            const mostCommonWords = Array.from({
                length: this.maxSentenceLength
            }, (_, i) => this.topNInDict(1, this.countOccurences(this.allTexts.map(x => this.fullClean(x)[i])))[0][0]);

            const firstUndefinedIndex = mostCommonWords.findIndex(word => word === 'undefined')
            const truncatedArray = firstUndefinedIndex === -1 ? mostCommonWords : mostCommonWords.slice(0, firstUndefinedIndex);

            return truncatedArray;
        },
        greedyChoice(probabilities) {
            let N = Object.keys(probabilities)[0].split(' ').length
            let prevN = Array(N).fill(".")
            let sentence = []
            let nextWord = Object.entries(probabilities[prevN.join(" ")]).reduce((a, b) => a[1] > b[1] ? a : b)[0]
            while (nextWord !== ".") {
                sentence.push(nextWord)
                prevN.shift()
                prevN.push(nextWord)
                nextWord = Object.entries(probabilities[prevN.join(" ")]).reduce((a, b) => a[1] > b[1] ? a : b)[0]
            }
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
            let prevN = Array(N).fill(".")
            let sentence = []
            let nextWord = this.getRandomKeyProportionateToValue(probabilities[prevN.join(" ")])
            while (nextWord !== ".") {
                sentence.push(nextWord)
                prevN.shift()
                prevN.push(nextWord)
                nextWord = this.getRandomKeyProportionateToValue(probabilities[prevN.join(" ")])
            }
            return sentence
        },
        slidingWindow(N) {
            let probabilities = {}
            for (let t of this.allTexts) {
                let prevN = Array(N).fill(".")
                for (let x of this.fullClean(t)) {
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
    data() {
        return {
            allTexts: [
                "Jeg elsker at spille fodbold og drømmer om at blive en professionel fodboldspiller en dag!",
                "Musik er min store passion, og jeg spiller guitar i mit eget band.",
                "Jeg elsker at læse fantasybøger og drømmer om at skrive min egen en dag.",
                "Matematik er min yndlingsfag, og jeg elsker at løse komplekse problemer.",
                "Naturen er mit fristed, og jeg elsker at vandre og udforske skove og bjerge.",
                "Jeg er en dyreelsker og har en samling af kæledyr derhjemme.",
                "At tegne og male er min kreative udfoldelse, og jeg drømmer om at blive en kunstner.",
                "Jeg bruger meget tid på at spille videospil og konkurrere online med mine venner.",
                "Jeg interesserer mig for historie og drømmer om at arbejde som arkæolog en dag.",
                "Jeg elsker at lave mad og eksperimentere med forskellige opskrifter.",
                "Jeg er en ivrig science fiction-fan og elsker at se rumfart og science fiction-film.",
                "Jeg bruger meget tid på at hjælpe i lokalsamfundet og frivilligt arbejde.",
                "Jeg er en teaterentusiast og elsker at optræde på scenen.",
                "Jeg elsker at rejse og udforske nye kulturer og steder.",
                "Jeg er en dygtig programmerer og elsker at skabe computerprogrammer.",
                "Jeg er en konkurrencemenneske og elsker at deltage i sportsbegivenheder.",
                "Jeg er en dedikeret studerende og stræber altid efter at opnå gode karakterer.",
                "Jeg drømmer om at blive astronaut og udforske rummet.",
                "Jeg elsker at skrive digte og noveller som en form for selvudtryk.",
                "Jeg er en positiv person og forsøger altid at sprede glæde omkring mig.",
                "Jeg elsker at spille tennis og drømmer om at vinde en grand slam-turnering.",
                "Jeg er en ivrig fotograf og elsker at fange smukke øjeblikke med mit kamera.",
                "Jeg bruger meget tid på at løse krydsord og gåder.",
                "Jeg interesserer mig for astronomi og drømmer om at opdage en ny stjerne.",
                "Jeg er en ivrig naturbeskytter og deltager i miljøprojekter.",
                "Jeg elsker at lave mad og bage, især kager og cookies.",
                "Jeg er en historiefortæller og elsker at opfinde fantastiske fortællinger.",
                "Jeg er en dedikeret gymnast og træner hårdt for at forbedre mine færdigheder.",
                "Jeg drømmer om at blive læge og hjælpe mennesker med deres helbred.",
                "Jeg elsker at se dokumentarfilm og lære om forskellige kulturer og historier.",
                "Jeg er en tekniknørd og bygger robotter i min fritid.",
                "Jeg er en kæmpe fan af science fiction-bøger og drømmer om at skrive en selv.",
                "Jeg elsker at synge og optræde på skolens talent shows.",
                "Jeg er en gamer og konkurrerer i esportsligaer.",
                "Jeg er en dedikeret naturfotograf og elsker at udforske vilde områder.",
                "Jeg bruger meget tid på at studere japansk sprog og kultur.",
                "Jeg er en aktiv friluftsperson og elsker at vandre og campere.",
                "Jeg er en ivrig bilsamler og elsker at restaurere gamle biler.",
                "Jeg interesserer mig for politik og drømmer om at blive politiker en dag.",
                "Jeg elsker at dykke og udforske undersøiske verden."
            ],
            stopWords: [
                "ad",
                "af",
                "akkurat",
                "al",
                "aldrig",
                "alene",
                "alle",
                "allerede",
                "alligevel",
                "alt",
                "altid",
                "altså",
                "anden",
                "andet",
                "andre",
                "art",
                "at",
                "bag",
                "bare",
                "begge",
                "bl.a.",
                "blandt",
                "blev",
                "blive",
                "bliver",
                "blot",
                "bringe",
                "brug",
                "burde",
                "både",
                "bør",
                "ca.",
                "da",
                "dag",
                "de",
                "del",
                "dem",
                "den",
                "denne",
                "dens",
                "der",
                "derefter",
                "deres",
                "derfor",
                "derfra",
                "deri",
                "dermed",
                "derpå",
                "derved",
                "des",
                "desto",
                "det",
                "dets",
                "dette",
                "dig",
                "din",
                "dine",
                "disse",
                "dit",
                "dog",
                "du",
                "dér",
                "dét",
                "efter",
                "egen",
                "ej",
                "eller",
                "ellers",
                "en",
                "end",
                "endelig",
                "endnu",
                "ene",
                "eneste",
                "enhver",
                "ens",
                "enten",
                "er",
                "et",
                "f.eks.",
                "faktisk",
                "far",
                "fat",
                "fem",
                "fik",
                "find",
                "finde",
                "fire",
                "flere",
                "flest",
                "fleste",
                "for",
                "foran",
                "fordi",
                "forrige",
                "fortsat",
                "fra",
                "fx",
                "få",
                "får",
                "følg",
                "følge",
                "følger",
                "før",
                "først",
                "første",
                "gang",
                "gennem",
                "gerne",
                "gid",
                "giv",
                "giver",
                "givet",
                "gjorde",
                "gjort",
                "god",
                "godt",
                "gå",
                "går",
                "gør",
                "gøre",
                "gørende",
                "ha",
                "haft",
                "ham",
                "han",
                "hans",
                "har",
                "havde",
                "have",
                "hej",
                "hel",
                "heldigvis",
                "hele",
                "heller",
                "helst",
                "helt",
                "hen",
                "hende",
                "hendes",
                "henover",
                "her",
                "herefter",
                "heri",
                "hermed",
                "herpå",
                "holder",
                "hos",
                "hun",
                "hvad",
                "hvem",
                "hver",
                "hvert",
                "hvilke",
                "hvilken",
                "hvilkes",
                "hvis",
                "hvor",
                "hvordan",
                "hvorefter",
                "hvorfor",
                "hvorfra",
                "hvorhen",
                "hvori",
                "hvorimod",
                "hvornår",
                "hvorved",
                "hør",
                "hører",
                "hørt",
                "hørte",
                "i",
                "igen",
                "igennem",
                "ikke",
                "imellem",
                "imens",
                "imod",
                "ind",
                "indtil",
                "ingen",
                "intet",
                "især",
                "iøvrigt",
                "ja",
                "jeg",
                "jer",
                "jeres",
                "jo",
                "kan",
                "kom",
                "komme",
                "kommer",
                "kommet",
                "kun",
                "kunne",
                "lad",
                "langs",
                "lav",
                "lave",
                "lavet",
                "lidt",
                "lig",
                "lige",
                "ligesom",
                "ligeså",
                "ligge",
                "ligger",
                "lille",
                "lissom",
                "længere",
                "man",
                "mand",
                "mange",
                "med",
                "meget",
                "mellem",
                "men",
                "mens",
                "mere",
                "mest",
                "mig",
                "min",
                "mindre",
                "mindst",
                "mine",
                "mit",
                "mod",
                "må",
                "måske",
                "måtte",
                "måttet",
                "ned",
                "nej",
                "nemlig",
                "netop",
                "ni",
                "nogen",
                "nogensinde",
                "noget",
                "nogle",
                "nok",
                "nu",
                "ny",
                "nye",
                "nyt",
                "nå",
                "når",
                "nær",
                "næste",
                "næsten",
                "og",
                "også",
                "okay",
                "om",
                "omkring",
                "op",
                "os",
                "otte",
                "over",
                "overalt",
                "overhovedet",
                "pga.",
                "på",
                "ret",
                "rigt",
                "ro",
                "rundt",
                "sagt",
                "samme",
                "sammen",
                "se",
                "seks",
                "selv",
                "selvom",
                "senere",
                "ser",
                "ses",
                "set",
                "siden",
                "sig",
                "sige",
                "siger",
                "simpelthen",
                "sin",
                "sine",
                "sit",
                "skal",
                "skam",
                "ske",
                "sker",
                "skulle",
                "små",
                "småt",
                "snart",
                "som",
                "stadig",
                "stor",
                "store",
                "stort",
                "synes",
                "syntes",
                "syv",
                "så",
                "sådan",
                "således",
                "såmænd",
                "såvel",
                "særlig",
                "tag",
                "tage",
                "temmelig",
                "thi",
                "ti",
                "tidligere",
                "til",
                "tilbage",
                "tit",
                "to",
                "tre",
                "tæt",
                "ud",
                "ude",
                "uden",
                "udover",
                "under",
                "undtagen",
                "var",
                "ved",
                "vel",
                "vi",
                "via",
                "videre",
                "vil",
                "ville",
                "vis",
                "vise",
                "vist",
                "vor",
                "vore",
                "vores",
                "vort",
                "vær",
                "være",
                "været",
                "véd",
                "år",
                "års",
                "én",
                "ét",
                "øvrigt"
            ]
        }
    },
}
</script>

<style scoped>

</style>

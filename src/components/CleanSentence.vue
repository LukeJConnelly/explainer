<template>
<div>
    <transition name="fade">
        <h3 v-if="step === 'punc-init'">Perfect!</h3>
    </transition>
    <p class="my-2">
        We've registered your sentence as: <b>{{ sentence }}</b><br>
        Below, we're going to "clean" up your sentence a bit (ie. removing unnecessary parts and lowercasing), so that it's easier for the computer to understand.<br>
    </p>
    <transition name="fade">
        <p v-if="'punc' === step.split('-')[0]">
            First, we're going to remove all punctuation, double spaces, and other characters.
            You can guess what characters are going to be removed if you'd like - click the character to mark it as a guess (it'll turn dark grey). <br>
            Then, when you're ready you can click the "Highlight all punctuation and double spaces" button to reveal what's going to be cleaned.
            If you'd like to see it again you can click the reset button and try again.
        </p>
    </transition>
    <transition name="fade">
        <p v-if="step === 'punc-started'">Now, you can click on any of the highlighted characters to remove them. Or, you can auto-click them all using the "Click all" button. When you're done, click the "Continue" button to move on to the next step.</p>
    </transition>
    <transition name="fade">
        <p v-if="step === 'punc-finished'">Great! Hit the continue button to advance</p>
    </transition>
    <transition name="fade">
        <p v-if="'caps' === step.split('-')[0]">
            Okay, here we're going to remove caps. There's no guessing this time, just click the "Highlight uppercase characters" button to reveal what's going to be cleaned.<br>
            You can reset to before caps were removed by using the reset button. If you want to see the punctuation part again, you can reload the page.
        </p>
    </transition>
    <transition name="fade">
        <p v-if="step === 'caps-started'">This time you can click on a highlighted character to lowercase it (or use the click all button if you want)</p>
    </transition>
    <transition name="fade">
        <p v-if="step === 'caps-finished'">Nice! Hit the continue button to advance</p>
    </transition>
    <transition name="fade">
        <p v-if="'space' === step.split('-')[0]">
            Finally, we're going to split the sentence by spaces (so that we can get our words)<br>
            Click the "Highlight spaces" button to reveal what's going to be cleaned.<br>
            You can reset to the unsplit sentence at any time using the reset button
        </p>
    </transition>
    <transition name="fade">
        <p v-if="step === 'space-started'">Click on the highlighted spaces to cut out our words (or use click all)</p>
    </transition>
    <transition name="fade">
        <p v-if="step === 'space-finished'">Awesome! We've cleaned the sentence, which you can see below as words. Click the button to advance to the next part (if it's asking you to wait congratulations on being fast! We'll update it in a minute so you can move on)</p>
    </transition>
</div>
<div class="row">
    <div class="col">
        <button :disabled="step.endsWith('init')" @click="reset()" class="btn btn-danger">Reset</button>
    </div>
    <div class="col">
        <button v-if="step.startsWith('punc')" @click="removePunct()" :disabled="!step.endsWith('init')" class="btn btn-primary">Highlight all punctuation and double spaces</button>
        <button v-if="step.startsWith('caps')" @click="removeCaps()" :disabled="!step.endsWith('init')" class="btn btn-primary">Highlight uppercase characters</button>
        <button v-if="step.startsWith('space')" @click="splitBySpace()" :disabled="!step.endsWith('init')" class="btn btn-primary">Highlight spaces</button>
    </div>
    <div class="col">
        <button v-if="step.endsWith('started')" @click="clickAll()" class="btn btn-secondary">Click all</button>
        <button v-if="step === 'space-finished'" @click="finishStep()" class="btn btn-success" :disabled="!canAdvance">{{canAdvance ? 'Finish' : 'Please Wait...'}}</button>
        <button v-else-if="step.endsWith('finished')" @click="finishStep()" class="btn btn-success">Continue</button>
    </div>
</div>
<div v-if="step.startsWith('punc')" class="btn-group pt-5" role="group" id="textButtons">
    <button v-for="(c, index) in cache.punc" class="btn btn-light p-1 border m-0" @click="toggleActive" :key="index">{{ c }}</button>
</div>
<transition name="fade">
    <div v-if="score && step == 'punc-finished'" class="my-2">You were {{Math.round(score[0] * 100)}}% correct ({{score[1]}} / {{score[3]}}, with {{ score[2] }} wrong)</div>
</transition>
<div v-if="step.startsWith('caps')" class="btn-group pt-5" role="group" id="textButtons">
    <button v-for="(c, index) in cache.caps" class="btn btn-light p-1 border m-0" disabled :key="index">{{ c }}</button>
</div>
<div v-if="step.startsWith('space')" class="btn-group pt-5" role="group" id="textButtons">
    <button v-for="(c, index) in cache.space" class="btn btn-light p-1 border m-0" disabled :key="index">{{ c }}</button>
</div>
</template>

<script>
import {
    nextTick
} from 'vue';

export default {
    name: 'App',
    props: {
        currState: {
            type: String,
        },
        states: {
            type: Array,
        },
    },
    computed: {
        canAdvance() {
            return this.states.indexOf(this.currState) > this.states.indexOf('clean')
        },
    },
    data() {
        return {
            step: 'punc-init',
            sentence: this.$route.query.sentence,
            cache: {
                punc: this.$route.query.sentence,
                caps: '',
                space: ''
            },
            score: undefined,
        }
    },
    methods: {
        clickAll() {
            let buttons = document.getElementById('textButtons').children;
            this.checkIsFinal();
            for (let b of buttons) {
                if (!b.disabled) {
                    b.click();
                }
            }
        },
        checkIsFinal() {
            const textButtons = Array.from(document.getElementById('textButtons').children);
            if (textButtons.every((b) => b.disabled)) {
                this.step = this.step.split('-')[0] + '-finished';
            }
        },
        finishStep() {
            if (this.step == 'punc-finished') {
                this.step = 'caps-init';
            } else if (this.step == 'caps-finished') {
                this.step = 'space-init';
            } else if (this.step == 'space-finished') {
                this.$router.push({
                    path: 'cloud',
                    query: {
                        sentence: Array.from(document.getElementById('textButtons').children).map((b) => b.textContent).join('')
                    }
                })
            }
            this.cache[this.step.split('-')[0]] = Array.from(document.getElementById('textButtons').children).map((b) => b.textContent).join('');
        },
        toggleActive(e) {
            e.target.classList.toggle('active');
        },
        removePunct() {
            let score = [0, 0, 0, 0] // [%, correct, incorrect, total]
            this.step = 'punc-started'
            let prev = undefined;
            let check = this.checkIsFinal;
            for (let c of document.getElementById('textButtons').children) {
                c.disabled = true;
                if (this.isPunct(c.textContent) || this.areBothWhitespace(prev, c.textContent)) {
                    score[3] = score[3] + 1;
                    if (c.classList.contains('active')) {
                        score[1] = score[1] + 1;
                    }
                    c.classList = "btn p-1 border border-dark m-0 dangered";
                    c.style.color = "white";
                    c.disabled = false;
                    c.onclick = () => {
                        c.classList.add('pop');
                        setTimeout(function () {
                            c.remove();
                            check();
                        }, 300);
                    }
                } else {
                    if (c.classList.contains('active')) {
                        score[2] = score[2] + 1;
                    }
                }
                prev = c.textContent;
            }
            score[0] = score[3] === 0 ? 1 : score[1] / score[3];
            this.score = score;
            this.checkIsFinal();
        },
        isPunct(c) {
            return c && c.match(/^[^\w\sæøåÆØÅ]+$/);
        },
        areBothWhitespace(a, b) {
            if (!a && !b) {
                return true
            }
            return a && b && a.match(/^\s+$/i) && b.match(/^\s+$/i)
        },
        removeCaps() {
            this.step = 'caps-started'
            let check = this.checkIsFinal;
            for (let c of document.getElementById('textButtons').children) {
                if (c.textContent == c.textContent.toUpperCase() && c.textContent != c.textContent.toLowerCase()) {
                    c.classList = "btn p-1 border border-dark m-0 changing";
                    let prevColor = c.style.color;
                    c.style.color = "white";
                    c.disabled = false;
                    c.onclick = () => {
                        c.classList.add('pop');
                        setTimeout(function () {
                            c.style.color = prevColor;
                            c.disabled = true;
                            c.classList = "btn btn-light p-1 border m-0";
                            c.textContent = c.textContent.toLowerCase();
                            check();
                        }, 300);
                    }
                }
            }
            this.checkIsFinal();
        },
        splitBySpace() {
            this.step = 'space-started'
            let check = this.checkIsFinal;
            let textButtons = document.getElementById('textButtons').children
            for (let i in textButtons) {
                let c = textButtons[i]
                if (i == 0) {
                    c.classList = "btn btn-dark p-1 no-right-border m-0";
                } else if (i == textButtons.length - 1) {
                    c.classList = "btn btn-dark p-1 no-left-border m-0";
                } else if (c.classList) {
                    c.classList = "btn btn-dark p-1 no-left-border no-right-border m-0";
                }
                if (c.textContent == ' ') {
                    c.classList = "btn p-1 border border-dark m-0 dangered";
                    c.disabled = false;
                    c.onclick = () => {
                        c.disabled = true;
                        c.style.border = "none";
                        c.classList.add('pop');
                        setTimeout(function () {
                            let prev = c.previousSibling
                            if (prev) {
                                prev.classList.add('prev')
                                prev.classList.remove('no-right-border')
                            }
                            let next = c.nextSibling
                            if (next) {
                                next.classList.add('next')
                                next.classList.remove('no-left-border')
                            }
                            c.classList = "btn p-1 bg-transparent m-0";
                            check();
                        }, 300);
                    }
                }
            }
            this.checkIsFinal();
        },
        async reset() {
            this.score = undefined;
            let currCache = this.cache[this.step.split('-')[0]]
            this.cache[this.step.split('-')[0]] = ''
            await nextTick();
            this.cache[this.step.split('-')[0]] = currCache
            this.step = this.step.split('-')[0] + '-init'
            return
        }
    }
}
</script>

<style>
.dangered {
    background-color: #dc3545 !important;
    -webkit-transition: background-color 1000ms linear;
    -ms-transition: background-color 1000ms linear;
    transition: background-color 1000ms linear;
}

.changing {
    background-color: #ffc107 !important;
    -webkit-transition: background-color 1000ms linear;
    -ms-transition: background-color 1000ms linear;
    transition: background-color 1000ms linear;
}

.pop {
    animation: pop 0.3s linear 1;
}

@keyframes pop {
    50% {
        transform: scale(1.2);
    }

    75% {
        transform: scale(0.6);
    }
}

.prev {
    border-top-right-radius: 5px !important;
    border-bottom-right-radius: 5px !important;
}

.next {
    border-top-left-radius: 5px !important;
    border-bottom-left-radius: 5px !important;
}

.no-right-border {
    border-right: 1px solid #343A40 !important;
}

.no-left-border {
    border-left: 1px solid #343A40 !important;
}
</style>

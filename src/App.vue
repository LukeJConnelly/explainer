<template>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono&display=swap" rel="stylesheet">
<nav class="navbar navbar-dark bg-dark">
    <a class="navbar-brand m-2 ms-5" href="#">Generativ AI Værktøj</a>
</nav>
<div class="container mt-5">
    <router-view :reqAddress='this.reqAddress' :allSentences='this.allSentences' :states='this.states' :currState='this.state'></router-view>
</div>
</template>

<script>
import 'bootstrap/dist/css/bootstrap.css'
import {
    stateNames
} from './states.js'

export default {
    name: 'App',
    data() {
        return {
            reqAddress: 'https://explainer-backend.azurewebsites.net/', // DO NOT FORGET THE SLASH
            state: stateNames[0],
            states: stateNames,
            allSentences: []
        }
    },
    methods: {
        checkSubmit(t) {
            document.getElementById('submit-button').disabled = t.length < 4
        },
        aboutMeSubmit() {
            this.inputText = document.getElementById('about-me-input').value
        },
        saveSentence(s) {
            this.cleaned = s;
            this.addSentence(s);
        },
        finishWordCloud() {
            this.wordCloudDone = true;
        },
        finishGenerative() {
            this.generativeDone = true;
        },
        addSentence(s) {
            fetch(this.reqAddress + 'add', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        sentence: s
                    })
                })
                .then(response => response.text())
                .then(data => {
                    console.log("Posted", data);
                })
                .catch(error => {
                    console.error('Post Error:', error);
                });
        },
        getUpdate() {
            setTimeout(() => {
                this.getUpdate();
            }, 10000);

            return fetch(this.reqAddress)
                .then(response => response.json())
                .then(data => {
                    console.log("Updated", data);
                    this.allSentences = data.sentences;
                    this.state = data.state;
                })
                .catch(error => {
                    console.error('Get Error:', error);
                });
        },
    },
    beforeMount() {
        this.getUpdate();
    },
}
</script>

<style>
#app {
    font-family: JetBrains Mono, monospace;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 1s;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}
</style>

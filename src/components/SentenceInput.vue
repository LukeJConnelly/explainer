<template>
<div>
    <h3>Hej med dig!</h3>
    <p>
        Dette er webstedet, vi har designet til at hjælpe med at lære om NLP og Generativ AI.
        Hvis du har spørgsmål, er du velkommen til at spørge os.
        Hvis du støder på en fejl på et tidspunkt, så lad os også vide det :)<br>
        For at starte skal du blot indtaste en sætning om hvorfor sociale medier er god/dårlig nedenfor og klikke på indsend-knappen.
        Vi vil samle alles sætninger sammen og bruge dem senere i klassen.
    </p>
    <div class="row" id="about-me-form">
        <div class="col">
            <div class="form-group">
                <label for="about-me-input" class="my-2">Indtast din sætning om sociale medier nedenfor:</label>
                <div class="input-group">
                    <input type="text" class="form-control" id="about-me-input" name="about-me-input" @input="checkSubmit($event.target.value)">
                    <div class="input-group-append">
                        <button id="submit-button" type="submit" class="btn btn-primary" @click="aboutMeSubmit()" disabled>Indsend</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<script>
export default {
    props: {
        reqAddress: {
            type: String,
        },
    },
    methods: {
        checkSubmit(t) {
            document.getElementById('submit-button').disabled = t.length < 4
        },
        aboutMeSubmit() {
            const s = document.getElementById('about-me-input').value
            this.addSentence(s);
            this.$router.push({
                path: 'clean',
                query: {
                    sentence: s
                }
            })
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
                    console.log(data);
                })
                .catch(error => {
                    console.error('Post Error:', error);
                });
        },
    }
}
</script>

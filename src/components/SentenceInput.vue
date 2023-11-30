<template>
<div>
    <h3>Hi there!</h3>
    <p>
        This is the website we've designed to help with learning about NLP and Generative AI.
        If you have any questions, feel free to ask us.
        If you encounter an error at some point, let us know too :)<br>
        To start, just enter a sentence about yourself below and click the submit button. It can be anything about yourself you like!
        We're going to collect everyones sentences together and use them later on in the class.
    </p>
    <div class="row" id="about-me-form">
        <div class="col">
            <div class="form-group">
                <label for="about-me-input" class="my-2">Enter your sentence about yourself below:</label>
                <div class="input-group">
                    <input type="text" class="form-control" id="about-me-input" name="about-me-input" @input="checkSubmit($event.target.value)">
                    <div class="input-group-append">
                        <button id="submit-button" type="submit" class="btn btn-primary" @click="aboutMeSubmit()" disabled>Submit</button>
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

<template>
<div>
    <h1 class="my-2">Hi Admin</h1>
    <div class="row my-3">
        <div class="col">
            <button @click="previousState" class="btn btn-danger" id="prev-button" :disabled="isDisabled">Prev</button>
        </div>
        <div class="col">
            <h5>Current registered state: {{ currState }}<span v-if="isDisabled"> (Awaiting Update)</span></h5>
        </div>
        <div class="col text-right">
            <button @click="nextState" class="btn btn-success" id="next btn-button" :disabled="isDisabled">Next</button>
        </div>
    </div>
    <div class="row my-3">
        <div class="col" v-for="(state, index) in states" :key="index">
            <button :class="{'btn btn-primary': index == selectedState, 'btn btn-secondary': index < selectedState, 'btn btn-light': index > selectedState}" disabled>{{ state }}</button>
        </div>
    </div>
    <table class="table my-5">
        <thead>
            <tr>
                <th scope="col">#</th>
                <th scope="col">Submitted Sentences</th>
                <th scope="col">Delete</th>
            </tr>
        </thead>

        <tbody>
            <tr v-for="(s, index) in allSentences" :key="s">
                <td>{{ index + 1 }}</td>
                <td>{{ s }}</td>
                <td>
                    <button class="btn btn-danger" @click="deleteSentence(index)" :disabled="isDisabled">Delete</button>
                </td>
            </tr>
        </tbody>
    </table>
</div>
</template>

<script>
export default {
    data() {
        return {
            isDisabled: false,
        };
    },
    computed: {
        selectedState() {
            return this.states.indexOf(this.currState);
        },
    },
    props: {
        states: {
            type: Array,
            default: () => [],
        },
        currState: {
            type: String,
            default: '',
        },
        reqAddress: {
            type: String,
        },
        allSentences: {
            type: Array,
            default: () => [],
        },
    },
    methods: {
        nextState() {
            let newState = Math.min(this.selectedState + 1, this.states.length - 1);
            this.postState(this.states[newState]);
        },
        previousState() {
            let newState = Math.max(this.selectedState - 1, 0);
            this.postState(this.states[newState]);
        },
        deleteSentence(i) {
            this.isDisabled = true;
            setTimeout(() => {
                this.isDisabled = false;
            }, 10000);
            fetch(this.reqAddress + 'remove', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        sentence: i
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
        postState(s) {
            this.isDisabled = true;
            setTimeout(() => {
                this.isDisabled = false;
            }, 10000);
            fetch(this.reqAddress + 'state', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        state: s
                    })
                })
                .then(response => response.text())
                .then(data => {
                    console.log("Posted State", data);
                })
                .catch(error => {
                    console.error('Post State Error:', error);
                });
        }
    },
};
</script>

<style>
.btn {
    padding: 10px;
}
</style>

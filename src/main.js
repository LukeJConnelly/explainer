import { createApp } from 'vue'
import { createRouter, createWebHashHistory } from 'vue-router'
import App from './App.vue'

import SentenceInput from './components/SentenceInput.vue'
import CleanSentence from './components/CleanSentence.vue'
import WordCloud from './components/WordCloud.vue'
import GenerativePart from './components/GenerativePart.vue'
import SankeyChart from './components/SankeyChart.vue'
import SankeyCircular from './components/SankeyCircular.vue'
import AdminComponent from './components/AdminComponent.vue'
import ErrorComponent from './components/ErrorComponent.vue'
import FreeGeneration from './components/FreeGeneration.vue'

const routes = [
    { path: '/', component: SentenceInput },
    { path: '/clean', component: CleanSentence },
    { path: '/cloud', component: WordCloud },
    { path: '/admin', component: AdminComponent },
    { path: '/generative', component: GenerativePart },
    { path: '/sankey', component: SankeyChart },
    { path: '/gengame', component: SankeyCircular },
    { path: '/free', component: FreeGeneration },
    { path: '/:pathMatch(.*)*', component: ErrorComponent }
]

const router = createRouter({
    history: createWebHashHistory(),
    routes,
})

createApp(App).use(router).mount('#app')
<template>
    <section class="vh-100" style="background-color: #9a616d">
        <div class="container py-5 h-100">
            <div class="row d-flex justify-content-center align-items-center h-70">
                <div class="col col-xxxl-10">
                    <div class="row g-0">
                        <div class="col-md-6 col-lg-8 d-flex align-items-center">
                            <div class="input-group">

                            </div>
                        </div>
                    </div>
                    <h1 style="color:black">{{ title }}</h1>
                    <hr>
                    <h3 style="color:floralwhite">{{ description }}</h3>
                    <br>
                    <h4>Author</h4>
                    <h4>{{ author }} </h4>
                    <hr>
                    <h5 style="color:powderblue">vote {{ vote }}</h5>
                    <td v-if="logged">
                        <button @click="Upvote" class="btn btn-success">
                            Up
                        </button>
                    </td>
                    <td v-if="logged">
                        <button @click="Downvote" class="btn btn-danger">
                            Down
                        </button>
                    </td>
                </div>
            </div>
        </div>
    </section>
</template>

<script lang="ts">

import axios from "axios"
import { computed, onMounted, ref } from "vue"
import { useRoute } from "vue-router"
import { useStore } from "vuex";

export default {
    name: "aboutComponent",

    setup() {
        const store = useStore();
        const title = ref("");
        const description = ref("");
        const author = ref("");
        const vote = ref();
        const api_url = "http://localhost:5000/"
        const route = useRoute()
        const id = route.params.id
        const token = localStorage.getItem('token')

        onMounted(() => {
            axios
                .get(api_url + "getUser", {
                    headers: {
                        token: `${token}`,
                    },
                })
                .then((response) => {
                    if (response.data) {
                        console.log(response.data.author);
                        store.dispatch("setAuth", true);
                        if (response.data.author) {
                            store.dispatch("setAuthor", true);
                        } else {
                            store.dispatch("setAuthor", false);
                        }
                    } else {
                        store.dispatch("setAuth", false);
                    }
                })
                .catch((c) => {
                    console.log(c);
                    store.dispatch("setAuth", false);
                });

            axios
                .post(api_url + "getArticlebyid", {
                    id
                }

                ).then(response => {
                    title.value = response.data.title
                    description.value = response.data.description
                    author.value = response.data.author
                    vote.value = response.data.vote
                })


        })
        const logged = computed(() => store.state.authenticated);
        const Upvote = () => {
            axios
                .post(
                    api_url + "upvote",
                    {
                        id,
                    },
                    {
                        headers: { token: `${token}` },
                    }
                )
                .then((response) => {
                    vote.value = response.data
                });
        };

        const Downvote = () => {
            axios
                .post(
                    api_url + "downvote",
                    {
                        id,
                    },
                    {
                        headers: { token: `${token}` },
                    }
                )
                .then((response) => {
                    vote.value = response.data
                });
        };



        return {
            title, description, author, vote, Upvote, Downvote, logged
        }
    }


}


</script>

<style>
h1,
h2,
h3,
h4,
h5,
h6 {

    font-weight: 100;

}
</style>
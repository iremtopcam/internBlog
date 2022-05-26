<template>
  <section class="vh-100" style="background-color: #9a616d">
    <div class="container py-5 h-100">
      <h1>{{ message }}</h1>
      <div class="row d-flex justify-content-center align-items-center h-70">
        <div class="col col-xxxl-10">
          <div class="row g-0">
            <div class="col-md-6 col-lg-8 d-flex align-items-center">
              <div class="input-group">

            </div>
            </div>
            <table class="table table-hover table-dark">
              <thead v-if="items">
                <tr>
                  <th scope="col">Vote</th>
                  <th scope="col">Title</th>
                  <th scope="col">Description</th>
                  <th scope="col">Author</th>
                  <th v-if="logged" scope="col">Upvote</th>
                  <th v-if="logged" scope="col">Downvote</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, index) in items" :key="index">
                  <th scope="row">{{ item.vote }}</th>
                  <td><a v-bind:href="'/article/'+ item._id.$oid">
    <div style="height:100%;width:100%">
      {{ item.title }}
    </div>
  </a></td>
                  <td>{{ item.description.substring(0,60) }}...<a v-bind:href="'/article/'+ item._id.$oid">click for more</a></td>
                  <td>{{ item.author }}</td>
                  <td v-if="logged">
                    <button @click="Upvote(item._id.$oid)" class="btn btn-success">
                      Up
                    </button>
                  </td>
                  <td v-if="logged">
                    <button @click="Downvote(item._id.$oid)" class="btn btn-danger">
                      Down
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>



<script lang="ts">
import { computed, onMounted, ref } from "vue";
import axios from "axios";
import { useStore } from "vuex";
export default {
  name: "HomeComponent",

  setup() {
    const api_url = "http://localhost:5000/"
    const message = ref("");
    const token = localStorage.getItem("token");
    const store = useStore();
    let items = ref();

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
            message.value = `Hi ${response.data.name}`;
            store.dispatch("setAuth", true);
            if (response.data.author) {
              store.dispatch("setAuthor", true);
              message.value = `Hi Author! ${response.data.name}`;
            } else {
              store.dispatch("setAuthor", false);
            }
          } else {
            store.dispatch("setAuth", false);
            message.value = ``;
          }
        })
        .catch((c) => {
          console.log(c);
          store.dispatch("setAuth", false);
          message.value = ``;
        });

      axios.get(api_url + "getArticle").then((response) => {
        items.value = response.data;
      });
    });

    const logged = computed(() => store.state.authenticated);

    const Upvote = (id: string) => {
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
          console.log(response.data)
          axios.get(api_url + "getArticle").then((response) => {
            items.value = response.data;
          });
        });
    };

    const Downvote = (id: string) => {
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
          console.log(response.data)
          axios.get(api_url + "getArticle").then((response) => {
            items.value = response.data;
          });
        });
    };

    return {
      message,
      items,
      Upvote,
      logged,
      Downvote,
    };
  },
};
</script>


<style>
</style>



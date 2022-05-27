<template>
  <section>
    <br />
    <h2>Add Article</h2>
    <hr />
    <div align="Center">
      <form @submit.prevent="submit">
        <h3>Title</h3>
        <input required v-model="data.title" type="text" />
        <br /><br />
        <h3>Description</h3>
        <textarea required id="w3review" name="w3review" rows="10" cols="60" v-model="data.description"></textarea>
        <br />
        <button class="btn btn-success block" type="submit">Ekle</button>
      </form>
    </div>
    <br>
    <h2>Delete Article</h2>
    <hr>
    <div class="container" align="center">
      <label for="cars">Choose your article:</label>

      <select v-model="selected" name="cars" id="cars">
        <option v-for="article in articles" v-bind:key="article.author"
          v-bind:value="{ id: article._id, text: article.title }">
          {{ article.title }}
        </option>
      </select>
      <button class="btn btn-danger" type="submit" @click="deleteSubmit">Sil</button>
    </div>
    <br><br>
  </section>
</template>

<script lang="ts">
const api_url = "http://localhost:5000/"
import { onMounted, reactive, ref } from "vue";
import axios from "axios";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
export default {
  name: "DashboardComponent",

  setup() {
    const data = reactive({
      title: "",
      description: "",
    });

    const articles = ref()
    const selected = ref()

    const token = localStorage.getItem("token");
    const store = useStore();
    const router = useRouter();
    onMounted(() => {
      axios.get(api_url + "getUser", {
        headers: {
          'token': `${token}`
        }
      }).then((response) => {
        if (response.data) {
          console.log(response.data.author)
          store.dispatch('setAuth', true)
          if (response.data.author) {
            store.dispatch('setAuthor', true)
          } else {
            store.dispatch('setAuthor', false)
          }
        } else {
          store.dispatch('setAuth', false)
        }

      }).catch(c => {
        console.log(c)
        store.dispatch('setAuth', false)
      })

      axios.get(api_url + "getArticleByAuthor", {
        headers: {
          'token': `${token}`
        }
      }).then(response => {
        articles.value = response.data
      })


    })

    const submit = async () => {
      const title = data.title;
      const description = data.description;
      console.log(data);
      axios
        .post(api_url + "Article", {
          title, description
        }, {
          headers: { 'token': `${token}` }
        }

        )
        .then((response) => {
          console.log(response);
          if (response) {
            router.push("/");
          }


        })
        .catch((err) => {
          console.log(err);
        });
    };

    const deleteSubmit = async () => {
      const id = selected.value.id.$oid
      axios.post(api_url + "deleteArticle", {
        id
      }, {
        headers: { 'token': `${token}` }
      })
      
      router.push("/")
    }


    return { data, submit, articles, deleteSubmit, selected };
  },
};
</script>

<style>
.block {
  display: block;
  width: 20%;
  border: none;
  background-color: #04aa6d;
  padding: 14px 28px;
  font-size: 16px;
  cursor: pointer;
  text-align: center;
}
</style>
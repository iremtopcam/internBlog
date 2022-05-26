<template>
  <nav class="navbar navbar-expand-md navbar-dark fixed-static-top bg-dark ">
  <div class="navbar">
    <a class="navbar-brand" href="/about">Intern Blog</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarCollapse">
      <ul class="navbar-nav me-auto mb-2 mb-md-0">
        <li class="nav-item">
          <a class="nav-link active" aria-current="page" href="/">Home</a>
        </li>
        <li class="nav-item" v-if="!logged">
          <a class="nav-link active" aria-current="page" href="/login">Login</a>
        </li>
        <li class="nav-item" v-if="!logged">
          <a class="nav-link active" aria-current="page" href="/register">Register</a>
        </li>
        <li class="nav-item" v-if="logged&&author">
          <a class="nav-link active" aria-current="page" href="/dashboard">Dashboard</a>
        </li>
        <li class="nav-item" v-if="logged&&!author">
          <a class="nav-link active" aria-current="page" href="/" @click="setAuthor">Be Author</a>
        </li>
        <li class="nav-item" v-if="logged">
          <a class="nav-link active" aria-current="page" href="/" @click="logout">Logout</a>
        </li>
      </ul>
      <!-- <form class="d-flex">
        <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
        <button class="btn btn-outline-success" type="submit">Search</button>
      </form> -->
    </div>
  </div>
</nav>
</template>

<script lang="ts">
import {computed} from 'vue'
import {useStore} from 'vuex'
import axios from 'axios';

export default {
    name:"navComponent",

    setup(){
    const api_url = "http://localhost:5000/"
    const store = useStore();

    const logged = computed(()=>store.state.authenticated)
    const author = computed(()=>store.state.author)
    let token = localStorage.getItem('token')
    const logout = () => {
  
    axios.post(api_url+"logout",{
          headers: {
          'token': `${token}`
  }
        }).then(response=>{
          console.log(response)
          localStorage.removeItem('token')
      
          store.dispatch("setAuth",false)
        })
      

    }

    const setAuthor = () =>{
        axios.post(api_url+"updateUser",{
          author:true
        },
        {
          headers: {
          'token': `${token}`
  }
        }).then(response=>{
          console.log(response)
          store.dispatch("setAuthor",true)
          return author
        })
    }

    
    return {logged,logout,author,setAuthor}
  },

    

}
  
</script>

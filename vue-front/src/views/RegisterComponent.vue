<template>
  <section class="vh-100" style="background-color: #9a616d">
    <div class="container py-5 h-100">
      <div class="row d-flex justify-content-center align-items-center h-100">
        <div class="col col-xl-10">
          <div class="card" style="border-radius: 1rem">
            <div class="row g-0">
              <div class="col-md-6 col-lg-5 d-none d-md-block">
                <img
                  
                  src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-registration/img4.webp"
                  alt="login form"
                  class="img-fluid"
                  style="border-radius: 1rem 0 0 1rem"
                />
              </div>
              <div class="col-md-6 col-lg-7 d-flex align-items-center">
                <div class="card-body p-4 p-lg-5 text-black">
                  <form @submit.prevent="submit">
                    <div class="d-flex align-items-center mb-3 pb-1">
                      <i
                        class="fas fa-cubes fa-2x me-3"
                        style="color: #ff6219"
                      ></i>
                      <span class="h1 fw-bold mb-0">Register</span>
                    </div>

                    <h5 class="fw-normal mb-3 pb-3" style="letter-spacing: 1px">
                      Create a new account
                    </h5>

                    <div class="form-outline mb-4">
                      <input v-model="data.name "
                        type="name"
                        id="form2Example11"
                        class="form-control form-control-lg"
                        required
                      />
                      <label class="form-label" for="form2Example11"
                        >Name</label
                      >
                    </div>

                    <div class="form-outline mb-4">
                      <input v-model="data.surname"
                        type="surname"
                        id="form2Example12"
                        class="form-control form-control-lg"
                        required
                      />
                      <label class="form-label" for="form2Example12"
                        >Surname</label
                      >
                    </div>
                    <div class="form-outline mb-4">
                      <input v-model="data.email"
                        type="email"
                        id="form2Example12"
                        class="form-control form-control-lg"
                        required
                      />
                      <label class="form-label" for="form2Example12"
                        >Email</label
                      >
                    </div>
                    <div class="form-outline mb-4">
                      <input v-model="data.username"
                        type="username"
                        id="form2Example17"
                        class="form-control form-control-lg"
                        required
                      />
                      <label class="form-label" for="form2Example17"
                        >Username</label
                      >
                    </div>

                    <div class="form-outline mb-4">
                      <input v-model="data.password"
                        type="password"
                        id="form2Example27"
                        class="form-control form-control-lg"
                        required
                      />
                      <label class="form-label" for="form2Example27"
                        >Password</label
                      >
                    </div>

                    <div class="form-outline mb-4">
                      <input v-model="data.confirm_password"
                        type="password"
                        id="form2Example28"
                        class="form-control form-control-lg"
                      />
                      <label class="form-label" for="form2Example27"
                      required
                        >Confirm Password</label
                      >
                    </div>

                    <div class="pt-1 mb-4">
                      <button
                        class="btn btn-dark btn-lg btn-block"
                        type="submit"
                      >
                        Register
                      </button>
                    </div>

                  </form>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script lang="ts">
import {reactive} from 'vue';
import axios from 'axios';
import {useRouter} from 'vue-router'

export default {
  name: "RegisterComponent",
  setup(){
    const data = reactive({
      name:'',
      surname:'',
      username:'',
      password:'',
      confirm_password:'',
      email:'',
    
    });

  const router = useRouter();
  const api_url = "http://localhost:5000/"

  const submit = async()=>{
    
    const name = data.name
    const surname = data.surname
    const username = data.username
    const password = data.password
    const confirm_password = data.confirm_password
    const email = data.email
    console.log(data)
    console.log(localStorage.getItem("token"))
    axios
    .post(api_url+"Register",{
      name,surname,username,password,confirm_password,email})
    .then(response=>{
      console.log(response)
      
    })
    .catch(err=>{
      console.log(err)
    });

    router.push('/login')

    
    

    
  }

  
  return {
      data,
      submit
    }
  }
}
</script>

<style>
</style>
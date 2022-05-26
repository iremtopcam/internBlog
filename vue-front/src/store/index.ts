import { Commit, createStore } from 'vuex'

export default createStore({
  state: {
    authenticated:false,
    author:false,
  },
  getters: {
  },
  mutations: {
    SET_AUTH:(state:{authenticated:boolean}, auth:boolean)=>state.authenticated=auth,
    SET_AUTHOR:(state:{author:boolean},authorr:boolean)=>state.author=authorr
  },
  actions: {
    setAuth:({commit}:{commit:Commit},auth:boolean)=>commit('SET_AUTH',auth),
    setAuthor:({commit}:{commit:Commit},authorr:boolean)=>commit('SET_AUTHOR',authorr),
  },
  modules: {
  }
})

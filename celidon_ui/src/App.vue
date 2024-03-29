<template>
  <div id="app">
    <div class="header">
      <div class="main-logo">
        <div class="main-logo-item">
          <img class="celidon" src="/celidon-logo.svg">
        </div>
        <h1 class="title is-3 is-size-4-mobile"> Infrastrukturbasierte Lokalisierung </h1>
      </div>
      <div class="header-logos">
        <div class="header-logos logo-group">
          <div class="header-logo-item">
            <img class="tudo" src="/tudo-logo.svg">
          </div>
          <div class="header-logo-item">
            <img class="cni" src="/cni-logo.svg">
          </div>
        </div>
      </div>
    </div>
    <nav role="navigation" aria-label="main navigation">
      <a v-for="(item, index) in menu" v-on:click="view=index" v-bind:key="item.key" v-bind:class="{ 'is-active': view==index }">
        {{ item.text }}
      </a>
    </nav>
    <div class="site-content">
      <div class="map-content">
        <overview v-if="menu[view].key=='overview'" :ilocPositions="ilocPositions" :poiPositions="poiPositions" :hololensPositions="hololensPositions"/>
        <singleview v-for="item in activeSingleView" v-bind:key="item.key" v-bind:floorId="item.key" v-bind:mapSource="item.mapSource" :ilocPositions="ilocPositions" :poiPositions="poiPositions" :hololensPositions="hololensPositions"/>
      </div>
      <div class="information-content">
        <div class='informations'>
          <div class="table-container">
            <table>
              <tbody>
                <tr>
                  <th class="long">ID</th>
                  <th class="fix">x</th>
                  <th class="fix">y</th>
                  <th class="fix">z</th>
                  <th class="fix">t</th>
                </tr>
                  <tr v-for="([x, y, z, t], name) in active" v-bind:key="name">
                    <td>{{ name }}</td>
                    <td>{{ x }}</td>
                    <td>{{ y }}</td>
                    <td>{{ z }}</td>
                    <td>{{ t }}</td>
                  </tr>
              </tbody>
            </table>
            <h1 style="font-weight:bold"><br>Inaktive IDs</h1>
            <div v-for="(_, name) in inactive" v-bind:key="name">
              <p>{{ name }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-if="!connected" class="status has-background-danger has-text-white">
      No connection to localization server. Retrying...
    </div>
  </div>
</template>

<script>

import Vue from 'vue'
import overview from './layouts/overview.vue'
import singleview from './layouts/singleview.vue'

export default {
  name: 'app',
  components: {
    overview,
    singleview
  },
  props: {
    socketPath: {
      type: String,
      default: '/position_server'
    },
    layout: "overview",
  },
  data() {
    return {
      view: "0",
      connected: false,
      ilocPositions: {},
      poiPositions: {},
      hololensPositions: {},
      active: {},
      inactive: {},
      menu: [
        {key:'overview', text:'Übersicht'},
        {key: '-1', text: 'KG', mapSource: "/brandhaus_kg.svg"},
        {key: '0', text: 'EG', mapSource: "/brandhaus_eg.svg"},
        {key: '1', text: 'OG 1', mapSource: "/brandhaus_og.svg"},
        {key: '2', text: 'OG 2', mapSource: "/brandhaus_og.svg"}
      ]
    }
  },
  computed: {
    activeSingleView: function() {
      // Return a single view menu item if one is selected
      var item = this.menu[this.view]
      if(item.key == 'overview') {
        return []
      } else {
        return [item]
      }
    },
    socketUrl: function() {
      var new_uri;
      if (window.location.protocol === "https:") {
          new_uri = "wss:";
      } else {
          new_uri = "ws:";
      }
      new_uri += "//" + window.location.host;
      new_uri += this.socketPath;
      return new_uri
    },
  },
  created() {
    this.openSocket()
    window.setInterval(this.updateActive, 16)
  },
  destroyed() {
  },
  methods: {
    openSocket() {
      var socket = new WebSocket(this.socketUrl)
      var socketMsgCB = this.onMessage
      socket.addEventListener('open', this.onSocketOpen)
      socket.addEventListener('message', e => socketMsgCB(e.data))
      socket.addEventListener('close', this.onSocketClose)
      this.socket = socket
    },
    onSocketOpen() {
      this.connected = true
    },
    onSocketClose() {
      this.connected = false
      setTimeout(this.openSocket, 3000)
    },
    onMessage(msg) {
      var recv_msg = JSON.parse(msg)
      if(recv_msg.topic == 'iloc') {
        delete recv_msg.topic
        for(var key in recv_msg){
          if(!(key in this.ilocPositions)){
            Vue.set(this.ilocPositions, key, {})
          }
          for(var name in recv_msg[key]){
            const d = new Date();
            recv_msg[key][name].ts = d.getTime();
          }
          Vue.set(this.ilocPositions, key, Object.assign({}, this.ilocPositions[key], recv_msg[key]))
        }
      }
      if(recv_msg.topic == 'poi') {
        delete recv_msg.topic
        for(var key in recv_msg){
          if(!(key in this.poiPositions)){
            Vue.set(this.poiPositions, key, {})
          }
          for(var name in recv_msg[key]){
            const d = new Date();
            recv_msg[key][name].ts = d.getTime();
          }
          Vue.set(this.poiPositions, key, Object.assign({}, this.poiPositions[key], recv_msg[key]))
        }
      }
      if(recv_msg.topic == 'hololens') {
        delete recv_msg.topic
        for(var key in recv_msg){
          if(!(key in this.hololensPositions)){
            Vue.set(this.hololensPositions, key, {})
          }
          for(var name in recv_msg[key]){
            const d = new Date();
            recv_msg[key][name].ts = d.getTime();
          }
          Vue.set(this.hololensPositions, key, Object.assign({}, this.hololensPositions[key], recv_msg[key]))
        }
      }
    },
    updateActive: function() {
      Object.entries(this.ilocPositions).forEach(([key, item]) => {
        Object.entries(item).forEach(([name, infos]) => {
          const d = new Date();
          var now = d.getTime();
          var time = ((now - infos.ts)/1000).toFixed(1)
          // inactive users
          if(time > 5) {
            // remove from active list
            Vue.delete(this.active, name);
            // add to inactive list
            Vue.set(this.inactive, name, null);
          }
          // active
          else {
            Vue.set(this.active, name, [infos.pos[0].toFixed(2),
                                        infos.pos[1].toFixed(2),
                                        infos.pos[2].toFixed(2),
                                        time]);
            // remove from inactive list
            Vue.delete(this.inactive, name);
          }
        })
      })
    },
  }
}
</script>

<style>
@import "~bulma/css/bulma.css";
@import url('https://fonts.googleapis.com/css?family=Source+Sans+Pro');

html, body {
  font-family: "Source Sans Pro";
}
</style>

<style scoped>
div#app {
  min-height: 100vh;
  min-width: 320px;
  display: flex;
  flex-direction: column;
  background-image: linear-gradient(rgba(22, 22, 22, 0.1) 0%, rgba(22, 22, 22, 0.5) 75%, rgb(22, 22, 22) 100%);
}

.header {
  display: flex;
  flex-wrap: wrap;
  margin-bottom: 0rem;
  justify-content: space-between;
  padding: 0 1rem 0 1rem;
}

.main-logo {
  display: flex;
  align-items: center;
}
.main-logo-item img{
  display: block;
  margin: auto 0;
  height: 3rem;
  width: auto;
}
.title {
  color: black;
  margin-left: 0.5rem;
}

.header-logos{
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  justify-content: flex-end;
}
.logo-group {
  margin: 0 0.5rem;
}
.header-logo-item img{
  height: 3vw;
  min-height: 1.25rem;
  margin: 0 0.5rem;
}

nav {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  background-color: rgb(140,201,197);
}
nav > a {
  padding: 0.25rem 0.9rem;
  color: black;
}
nav > a:hover{
  background-color: rgba(0, 0, 0, 0.1);
}
nav > a.is-active {
  border-bottom: solid 5px rgb(100, 161, 157);
}

.site-content{
  flex: 1;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: space-evenly;
  padding: 0.5rem;
}
.map-content{
  flex: 6;
  display: flex;
}
.information-content{
  position: relative;
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 18rem;
  min-height: 18rem;
}
.internal-data {
  font-size: x-large;
  color: black;
  background-color: white;
}
.informations{
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  margin: 0.5rem;
  padding: 0.5rem;
  padding-top: 0;
  background-color: white;
  overflow: auto;
}
.informations .table-container {
  padding: 0.25rem 0.25rem 0.25rem 0.25rem;
}

@media only screen and (max-width: 768px) {
  .informations {
    position: inherit;
  }
  .site-content {
    display: block;
  }
}

table {
  width: 100%;
}
th {
  text-align: right;
}
.fix {
  width: 1em
}
.long {
  width: 4em
}
td {
  text-align: right;
}


.status {
  position: fixed;
  width: 100%;
  bottom: 0;
  padding: 0.17rem 1rem;
}

</style>

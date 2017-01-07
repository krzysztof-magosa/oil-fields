<template>
  <div class="component-app" id="app">
    <header></header>
    <div class="tabs-container">
      <div class="tabs-panel" v-bind:class="{ active: view == 'name' }">
        <name></name>
      </div>
      <div class="tabs-panel" v-bind:class="{ active: view == 'games' }">
        <games v-bind:games="games"></games>
      </div>
      <div v-if="game && !game.started" class="tabs-panel" v-bind:class="{ active: view == 'waiting' }">
        <waiting v-bind:me="me" v-bind:game="game"></waiting>
      </div>
      <div v-if="game && game.started" class="tabs-panel" v-bind:class="{ active: view == 'game' }">
        <game v-bind:me="me" v-bind:game="game" v-bind:estates="estates"></game>
      </div>
    </div>
  </div>
</template>

<script>
/* eslint-disable */
import Name from './components/Name';
import Games from './components/Games';
import Waiting from './components/Waiting';
import Game from './components/Game';

export default {
  name: 'app',
  data() {
    return {
      view: 'name',
      me: null,
      game: null,
      games: [],
      estates: [],
    };
  },
  methods: {
    onMessage: function(action, data) {
      switch(action) {
      case 'me':
        this.me = data;
        break;
      case 'games':
        this.games = data;
        this.view = 'games';
        break;
      case 'estates':
        this.estates = data;
        break;
      case 'game':
        this.game = data;
        this.view = data.started ? 'game' : 'waiting';
        break;
      }
    }
  },
  created() {
    this.$socket.onMessage(this.onMessage);
  },
  components: {
    Name,
    Games,
    Waiting,
    Game,
  },
};
</script>

<style scoped>
</style>

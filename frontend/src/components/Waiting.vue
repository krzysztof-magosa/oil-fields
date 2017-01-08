<template>
  <div>
    <h2>Waiting for owner to start game...</h2>
    <div>
      <table v-if="players">
        <thead>
          <tr>
            <th>Player</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="player in players">
            <td>{{ player.name }}</td>
          </tr>
        </tbody>
    </div>
    <div v-bind:class="{ hidden: !canStart }">
      <input type="button" value="Start" v-on:click="start">
    </div>
  </div>
</template>

<script>
/* eslint-disable */
export default {
  name: 'waiting',
  props: ['me', 'players', 'game'],
  data() {
    return {
    };
  },
  computed: {
    canStart: function() {
      if (!this.me || !this.game) {
        return false;
      }

      return this.me.uuid == this.game.owner;
    }
  },
  methods: {
    start: function() {
      this.$socket.send('start_game', {});
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>

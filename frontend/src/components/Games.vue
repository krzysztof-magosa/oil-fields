<template>
  <div class="view-games">
    <h2>Join to existing game</h2>
    <table>
      <thead>
        <tr>
          <th>Balance</th>
          <th>Owner</th>
          <th>Players</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(game, index) in games" v-on:click="join(index)">
          <td>{{ game.initial_balance }}</td>
          <td>{{ game.owner.name }}</td>
          <td>{{ game.player_names.join(", ") }}</td>
          <td class="ta-right"><input type="button" value="Join"></td>
        </tr>
      </tbody>
    </table>

    <h2>Create new game</h2>
    <form>
      <div class="form-group">
        <label>Initial balance</label>
        <input type="number" min="10000" max="1000000" v-model="initial_balance">
      </div>
      <input type="button" value="Create game" v-on:click="create">
    </form>
  </div>
</template>

<script>
/* eslint-disable */
export default {
  name: 'games',
  props: ['games'],
  data() {
    return {
      initial_balance: 1000000
    };
  },
  computed: {
/*    filteredGames: function() {
      return this.games.map(
        function(game) {
          return {
            uuid: game.uuid,
            initial_balance: game.initial_balance,
            owner: game.owner
          }
        }
      );
    } */
  },
  methods: {
    join: function submit(index) {
      const game = this.games[index];
      this.$socket.send(
        'join_game',
        {
          uuid: game.uuid
        }
      );
    },
    create: function() {
      this.$socket.send(
        'create_game',
        {
          initial_balance: this.initial_balance
        }
      );
    }
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
</style>

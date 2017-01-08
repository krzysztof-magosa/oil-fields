<template>
  <div>
    <h2>Factories</h2>
    <table>
      <thead>
        <tr>
          <td>Name</td>
          <td>Price</td>
          <td>Buy</td>
      </thead>
      <tbody>
        <tr v-for="(factory, index) in factories">
          <td>{{ factory.name }}</td>
          <td>{{ factory.price }}</td>
          <td>
            <input v-if="!factory.owner && me.balance > factory.price" type="button" value="Buy" @click="buy(index)">
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
/* eslint-disable */
export default {
  name: 'factories',
  props: ['estates', 'type', 'me'],
  data() {
    return {
    };
  },
  computed: {
    factories: function() {
      return this.estates.filter(function(item) {
        return this.type == item.type;
      }, this);
    }
  },
  methods: {
    buy: function(index) {
      this.$socket.send("buy_estate", { uuid: this.factories[index].uuid });
      this.$emit("set_view", "index");
    },
  },
};

</script>

<style>
</style>

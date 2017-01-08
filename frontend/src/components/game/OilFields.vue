<template>
  <div>
    <h2>Oil fields</h2>
    <table>
      <thead>
        <tr>
          <td>Name</td>
          <td>Price</td>
          <td>Buy</td>
      </thead>
      <tbody>
        <tr v-for="(oilfield, index) in oilfields">
          <td>{{ oilfield.name }}</td>
          <td>{{ oilfield.price }}</td>
          <td>
            <input v-if="!oilfield.owner && me.balance >= oilfield.price" type="button" value="Buy" @click="buy(index)">
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
/* eslint-disable */

export default {
  name: 'oilfields',
  props: ['estates', 'type', 'me'],
  data() {
    return {
    };
  },
  computed: {
    oilfields: function() {
      return this.estates.filter(function(item) {
        return item.type == "oilfield";
      }, this);
    }
  },
  methods: {
    buy: function(index) {
      this.$socket.send("buy_oilfield", {
        uuid: this.oilfields[index].uuid,
      });
      this.$emit("set_view", "index");
    },
  },
  components: {
  }
};

</script>

<style>
</style>

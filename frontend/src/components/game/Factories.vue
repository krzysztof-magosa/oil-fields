<template>
  <div>
    <modal v-if="showModal" @close="buy()">
      <div slot="body">
        <input type="number" v-model="price">
      </div>
      <h3 slot="header">Price of produced equipment</h3>
    </modal>

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
            <input v-if="!factory.owner && me.balance >= factory.price" type="button" value="Buy" @click="choose(index)">
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
/* eslint-disable */

import Modal from '../Modal';

export default {
  name: 'factories',
  props: ['estates', 'type', 'me'],
  data() {
    return {
      showModal: false,
      price: 1000,
      index: null,
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
    choose: function(index) {
      this.index = index;
      this.showModal = true;
    },
    buy: function() {
      this.$socket.send("buy_factory", {
        uuid: this.factories[this.index].uuid,
        equipment_price: this.price,
      });
      this.showModal = false;
      this.$emit("set_view", "index");
    },
  },
  components: {
    Modal
  }
};

</script>

<style>
</style>

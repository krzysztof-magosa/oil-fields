<template>
  <div>
    <input type="button" value="Cancel" v-bind:class="{ hidden: view == 'menu' }" v-on:click="view='menu'">
    <div class="tabs-container">
      <div class="tabs-panel" v-bind:class="{ active: view == 'menu' }">
        <h2>Turn: {{ game.turn }}</h2>
        <h2>$$$: {{ me.balance }}</h2>

        <h2>Estate shop</h2>
        <ul>
          <li>Drill factory</li>
          <li>Pump factory</li>
          <li>Wagon factory</li>
        </ul>

        <h2>Equipment shop</h2>
        <ul>
          <li>Drills</li>
          <li>Pumps</li>
          <li>Wagons</li>
        </ul>

        <h2>Other possibilites</h2>
        <ul>
          <li v-on:click="view='estate'">See my estate</li>
          <li>Next player</li>
          <li>Sabotage attempt</li>
          <li>Change price of equipment</li>
          <li>Get loan</li>
        </ul>
      </div>
      <div class="tabs-panel" v-bind:class="{ active: view == 'estate' }">
        <h2>Your oil fields</h2>
        <table>
          <thead>
            <tr>
              <td>Name</td>
              <td>D</td>
              <td>P</td>
              <td>W</td>
              <td>O</td>
          </thead>
          <tbody>
            <tr v-for="oil_field in my_oil_fields">
              <td>{{ oil_field.name }}</td>
              <td>{{ oil_field.equipments_count.drill }}</td>
              <td>{{ oil_field.equipments_count.pump }}</td>
              <td>{{ oil_field.equipments_count.wagon }}</td>
              <td>{{ oil_field.equipments_count.oil }}</td>
            </tr>
          </tbody>
        </table>

        <h2>Your factories</h2>
        <table>
          <thead>
            <tr>
              <td>Name</td>
              <td>E. Price</td>
              <td>Stock</td>
          </thead>
          <tbody>
            <tr v-for="factory in my_factories">
              <td>{{ factory.name }}</td>
              <td>{{ factory.equipment_price }}</td>
              <td>{{ factory.stock }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
/* eslint-disable */
export default {
  name: 'game',
  props: ['me', 'game', 'estates'],
  data() {
    return {
      view: 'menu'
    };
  },
  computed: {
    my_estates: function() {
      return this.estates.filter(function(item) {
        return item.owner == this.me.uuid;
      }, this);
    },
    my_oil_fields: function() {
      return this.my_estates.filter(function(item) {
        return item.type == 'oilfield';
      }, this);
    },
    my_factories: function() {
      return this.my_estates.filter(function(item) {
        return item.type != 'oilfield';
      }, this);
    }
  },
  methods: {
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
</style>

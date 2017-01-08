<template>
  <div>
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
          <td>{{ oil_field.oil }}</td>
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
</template>

<script>
/* eslint-disable */
export default {
  name: 'my-estate',
  props: ['me', 'game', 'estates'],
  data() {
    return {
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

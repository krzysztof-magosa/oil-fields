<template>
  <div>
    <h2>$$$: {{ me.balance }}</h2>
    <h2>Oil price: {{ game.oil_price }}</h2>

    <h2>Estate shop</h2>
    <ul>
      <li><a href="#" @click="$emit('set_view', 'factories-drill')">Drill factory</a></li>
      <li><a href="#" @click="$emit('set_view', 'factories-pump')">Pump factory</a></li>
      <li><a href="#" @click="$emit('set_view', 'factories-wagon')">Wagon factory</a></li>
    </ul>

    <h2>Equipment shop</h2>
    <ul>
      <li><a href="#">Drills</a></li>
      <li><a href="#">Pumps</a></li>
      <li><a href="#">Wagons</a></li>
    </ul>

    <h2>Other possibilites</h2>
    <ul>
      <li><a href="#" @click="$emit('set_view', 'my-estate')">See my estate</a></li>
      <li><a href="#" @click="$emit('next_player')">Next player</a></li>
      <li><a href="#">Sabotage attempt</a></li>
      <li><a href="#">Change price of equipment</a></li>
      <li><a href="#">Get loan</a></li>
    </ul>
</template>

<script>
/* eslint-disable */
export default {
  name: 'index',
  props: ['me', 'game'],
  data() {
    return {
    };
  },
  computed: {
  },
  methods: {
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
</style>

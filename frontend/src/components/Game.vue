<template>
  <div>
    <input type="button" value="Cancel" v-bind:class="{ hidden: (view == 'index' || view == 'waiting') }" v-on:click="set_view('index')">
    <div class="tabs-container">
      <div class="tabs-panel" v-bind:class="{ active: view == 'waiting' }">
        <waiting-for-other :me="me" :game="game"></waiting-for-other>
      </div>
      <div class="tabs-panel" v-bind:class="{ active: view == 'index' }">
        <index :me="me" :game="game" @set_view="set_view" @next_player="next_player"></index>
      </div>
      <div class="tabs-panel" v-bind:class="{ active: view == 'my-estate' }">
        <my-estate :me="me" :estates="estates"></my-estate>
      </div>
      <div class="tabs-panel" v-bind:class="{ active: view == 'factories-drill' }">
        <factories :me="me" :estates="estates" @set_view="set_view" type="drillfactory"></factories>
      </div>
      <div class="tabs-panel" v-bind:class="{ active: view == 'factories-pump' }">
        <factories :me="me" :estates="estates" @set_view="set_view" type="pumpfactory"></factories>
      </div>
      <div class="tabs-panel" v-bind:class="{ active: view == 'factories-wagon' }">
        <factories :me="me" :estates="estates" @set_view="set_view" type="wagonfactory"></factories>
      </div>
    </div>
  </div>
</template>

<script>
/* eslint-disable */
import Index from './game/Index';
import MyEstate from './game/MyEstate';
import Factories from './game/Factories';
import WaitingForOther from './game/WaitingForOther';

export default {
  name: 'game',
  props: ['me', 'game', 'estates'],
  data() {
    return {
      my_view: 'index',
    };
  },
  computed: {
    view: function() {
      return this.me.uuid == this.game.turn ? this.my_view : 'waiting';
    },
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
    set_view: function(view) {
      this.my_view = view;
    },
    next_player: function() {
      this.$socket.send("next_player", {});
    }
  },
  components: {
    Index,
    MyEstate,
    Factories,
    WaitingForOther,
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
</style>

<template>
  <div>
    <h2>Login to server</h2>
    <div>
        <input type="text" v-model="name" placeholder="Your name">
        <input type="submit" value="Connect!" v-on:click="submit">
    </div>
  </div>
</template>

<script>
export default {
  name: 'name',
  data() {
    return {
      name: 'anonymous',
    };
  },
  methods: {
    submit: function submit() {
      this.$socket.send('set_name', { name: this.name });
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>

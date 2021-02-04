<template>
  <div id="app">
    <CContainer>
      <Countries/>
    </CContainer>
  </div>
</template>

<script>
import Countries from './components/Countries.vue'

export default {
  name: 'App',
  components: {
    Countries
  }
}
</script>

<style lang="scss">
@import 'assets/scss/style';
</style>

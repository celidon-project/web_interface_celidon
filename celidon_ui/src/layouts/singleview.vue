<template>
  <div class="singleview">
    <div class="floor-maps">
        <FloorPlanView :floorId="floorId" :mapSource="mapSource" :ilocPositions="ilocPositions" :poiPositions="poiPositions" ref="floorRef"/>
    </div>
  </div>
</template>

<script>
import FloorPlanView from '../FloorPlanView.vue'

export default {
  components: {
    FloorPlanView
  },
  props: {
    floorId: String,
    mapSource: String,
    ilocPositions: Object,
    poiPositions: Object
  },
  mounted() {
    const floor = this.$refs.floorRef;
    window.addEventListener('orientationchange', function() {
      floor.floorMap.fitBounds(...floor.getBounds);
      })
  },
}
</script>

<style>
@import "~bulma/css/bulma.css";

body {
  font-family: "Source Sans Pro";
}
</style>

<style scoped>
.singleview {
  flex: 1;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
}
.floor-maps {
  display: flex;
  flex-direction: column;
  flex: 1;
  margin: 0.5rem;
  min-width: 200px;
  min-height: 200px;
}

</style>

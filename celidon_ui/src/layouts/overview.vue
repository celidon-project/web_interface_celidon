<template>
  <div class="overview">
    <div class="floor-maps">
      <div class="map">
          <FloorPlanView floorId="0" mapSource="/brandhaus_eg.svg" :ilocPositions="ilocPositions" :poiPositions="poiPositions" :viewBounds="viewBounds" ref="0"/>
      </div>
      <div class="map">
          <FloorPlanView floorId="1" mapSource="/brandhaus_og.svg" :ilocPositions="ilocPositions" :poiPositions="poiPositions" :viewBounds="viewBounds" ref="1"/>
      </div>
    </div>
    <div class="floor-maps">
      <div class="map">
          <FloorPlanView floorId="2" mapSource="/brandhaus_og.svg" :ilocPositions="ilocPositions" :poiPositions="poiPositions" :viewBounds="viewBounds" ref="2"/>
      </div>
      <div class="map">
          <FloorPlanView floorId="-1" mapSource="/brandhaus_kg.svg" :ilocPositions="ilocPositions" :poiPositions="poiPositions" :viewBounds="viewBounds" ref="-1"/>
      </div>
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
    ilocPositions: Object,
    poiPositions: Object
  },
  data() {
    return {
      viewBounds: [[0, 0], [12, 11.5]]
    }
  },
  mounted() {
    const floorRefs = this.$refs;
    window.addEventListener('orientationchange', function() {
      Object.values(floorRefs).forEach(floor => {
        floor.floorMap.fitBounds(...floor.getBounds);
      })
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
.overview {
  flex: 1;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
}
.floor-maps {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  width: 100%;
}
.map {
  flex: 1;
  padding: 0.5rem;
  min-width: 270px;
  min-height: 220px;
}

</style>

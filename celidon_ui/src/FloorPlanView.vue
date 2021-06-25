<template>
  <div id="container">
    <div class="floor" :id="floorId"></div>
    <h1 class="floor-title" v-if="floorId < 0"> KG </h1>
    <h1 class="floor-title" v-if="floorId == 0"> EG </h1>
    <h1 class="floor-title" v-if="floorId > 0"> OG {{ floorId }} </h1>
  </div>
</template>

<script>
  import L from 'leaflet'

  import mapUtil from './util/map.js'

  export default {
    name: 'FloorPlanView',
    props: {
      floorId: String,
      mapSource: String,
      ilocPositions: Object,
      poiPositions: Object,
      hololensPositions: Object,
      viewBounds: Array
    },
    data() {
      return {
        ffMarkers: {},
        poiMarkers: {},
        poiTimeouts: {},
        hololensMarkers: {},
        hololensTimeouts: {},
        floorMap: Object,
      }
    },
    computed: {
      getBounds() {
        if(this.viewBounds)
          return [this.viewBounds, {padding: [1, 1]}]
        else
          return [[[0, 0], [12, 19.5]], {padding: [10, 10]}]
      }
    },
    methods: {
      updateIloc() {
        if(this.ilocPositions) {
          var firemen = this.ilocPositions["floor"+this.floorId]
          if(firemen !== undefined) {
              this.ffMarkers = mapUtil.updateFiremanMarkers(this.ffMarkers, this.floorMap, firemen);
          }
        }
      },
      updatePoi() {
        if(this.poiPositions) {
          var poi = this.poiPositions["floor"+this.floorId]
          if(poi !== undefined) {
            this.poiTimeouts = mapUtil.updateTimeouts(this.poiTimeouts, poi)
            this.poiMarkers = mapUtil.updatePoiMarkers(this.poiMarkers, this.floorMap, this.poiTimeouts, poi);
          }
        }
      },
      updateHololens() {
        if(this.hololensPositions) {
          var hololens = this.hololensPositions["floor"+this.floorId]
          if(hololens !== undefined) {
            this.hololensTimeouts = mapUtil.updateTimeouts(this.hololensTimeouts, hololens)
            this.hololensMarkers = mapUtil.updateHololensMarkers(this.hololensMarkers, this.floorMap, this.hololensTimeouts, hololens);
          }
        }
      },
      updateMapSize() {
        this.floorMap.fitBounds(...this.getBounds);
        this.floorMap.invalidateSize();
      },
    },
    mounted() {
      this.floorMap = L.map(this.floorId, {
        zoomSnap: 0.1,
        zoomControl: false,
        dragging: false,
        touchZoom: false,
        doubleClickZoom: false,
        scrollWheelZoom: false,
        boxZoom: false,
        keyboard: false,
        tap: false,
        crs: L.CRS.Simple,
      });

      var imageBounds = [[0, 0], [12, 19.5]];
      L.imageOverlay(this.mapSource, imageBounds).addTo(this.floorMap);
      this.updateMapSize();

      window.setInterval(this.updateIloc, 100);
      window.setInterval(this.updatePoi, 100);
      window.setInterval(this.updateHololens, 100);
    }
  }

</script>

<style scoped>
@import "~leaflet/dist/leaflet.css";

#container {
  height: 100%;
  position: relative;
  display: flex;
  flex-direction: column;
}
.floor-title {
  position: absolute;
  top: 0;
  left: 0.5rem;
  font-size: x-large;
  color: black;
}
.floor {
  flex: 1;
  width: 100%;
  height: 100%;
  z-index: 0;
  background-color: white;
}
.floor >>> .leaflet-marker-pane > div {
  position: absolute;
}
.floor >>> i > svg {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
.floor >>> .leaflet-tooltip-top{
    border-color: none;
    border: none;
    background: rgba(0, 0, 0, 0);
    box-shadow: none;
}
.floor >>> .leaflet-tooltip-top:before, .leaflet-tooltip-bottom:before,
           .leaflet-tooltip-left:before, .leaflet-tooltip-right:before{
    border: none;
}

img.leaflet-marker-icon {
  background-color: red !important;
}
</style>

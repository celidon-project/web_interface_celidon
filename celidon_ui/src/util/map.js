import L from 'leaflet';

function firemanMarker(latlng, name) {
  return L.marker(
    latlng,
    {icon: L.icon({
      iconUrl: 'fireman-icon.svg',
      iconSize: [30, 30],
      iconAnchor: [15, 10],
      shadowUrl: null
    }),
     title: name})
     .bindTooltip(name,
      {
        permanent: true,
        direction: 'top',
        opacity: 1
      });
}

// markers: {name: LeafletMarker}
// map: LeafletMap
// objects: {name: {ts: timestamp, pos: lnglat}}
function updateFiremanMarkers(markers, map, objects) {
  // Update markers and add new markers
  Object.keys(objects).forEach(name => {
    var pos = objects[name].pos
    var marker = markers[name]
    if(marker) {
      marker.setLatLng([pos[1], pos[0]])
    } else {
      markers[name] = firemanMarker([pos[1], pos[0]], name)
      markers[name].addTo(map)
    }
  })
  // Delete old markers
  Object.entries(markers).forEach(([name, marker]) => {
    if(!objects[name]) {
      marker.remove()
      delete markers[name]
    }
  })
  return markers
}

function poiMarker(latlng, name) {
  return L.marker(
    latlng,
    {icon: L.icon({
      iconUrl: 'poi.svg',
      iconSize: [20, 20],
      iconAnchor: [10, 10],
      shadowUrl: null
    }),
     title: name})
     .bindTooltip(name,
      {
        permanent: true,
        direction: 'top',
        opacity: 1
      });
}

// markers: {name: LeafletMarker}
// map: LeafletMap
// objects: {name: {ts: timestamp, to: timeout, pos: lnglat, text: text}}
function updatePoiMarkers(markers, map, timeouts, objects) {
  // Update markers and add new markers
  Object.keys(objects).forEach(name => {
    var pos = objects[name].pos
    var marker = markers[name]
    if(marker) {
      marker.setLatLng([pos[1], pos[0]])
    } else {
      markers[name] = poiMarker([pos[1], pos[0]], objects[name].text)
      markers[name].addTo(map)
    }
  })
  // Delete old markers
  Object.entries(markers).forEach(([name, marker]) => {
    const d = new Date();
    var now = d.getTime();
    if(now - timeouts[name].ts > timeouts[name].to) {
      marker.remove()
      delete markers[name]
    }
  })
  return markers
}

// objects: {name: {ts: timestamp, to: timeout, pos: lnglat, text: text}}
function updateTimeouts(timeouts, objects) {
  // Update markers and add new markers
  Object.keys(objects).forEach(name => {
    timeouts[name] = {'ts': objects[name].ts,
                      'to': objects[name].to}
  })
  return timeouts
}

export default {updateFiremanMarkers, updatePoiMarkers, updateTimeouts}

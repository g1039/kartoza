const copy = "© <a href='https://kartoza.com/en/'>OpenStreetMap</a> contributors";
const url = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
const osm = L.tileLayer(url, { attribution: copy });
const map = L.map("map", { layers: [osm], minZoom: 5 });
const markers = JSON.parse(document.getElementById("markers-data").textContent);
const features = L.geoJSON(markers).bindPopup(layer => "<b>First Name: </b>" + layer.feature.properties.first_name + "<br>" + "<b>Last Name: </b>" + layer.feature.properties.last_name + "<br>" + "<b>Email: </b>" + layer.feature.properties.email + "<br>" + "<b>Home Address: </b>" + layer.feature.properties.home_address + "<br>" + "<b>Phone Number: </b>" + layer.feature.properties.phone_number)

map.addLayer(features).fitBounds(features.getBounds());

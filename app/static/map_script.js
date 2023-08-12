// script.js
function initMap() {
    // Make an API call to get bin data
    fetch('/get-bin-data/')
        .then(response => response.json())
        .then(data => {
            const binData = data.bins;
            // Use binData to create markers on the map
            createMarker(binData);
        })
        .catch(error => {
            console.error('Error fetching bin data:', error);
        });
}

function createMarker(binData) {
    const emptyBinIcon = {
        green: [
            {
                url: "/static/bins_img/green-empty-1.png",
                scaledSize: new google.maps.Size(60, 60),
            },
            {
                url: "/static/bins_img/green-empty-2.png",
                scaledSize: new google.maps.Size(60, 60),
            },
            {
                url: "/static/bins_img/green-empty-3.png",
                scaledSize: new google.maps.Size(60, 60),
            },
        ],
        
        red: [
            {
                url: "/static/bins_img/red-empty-1.png",
                scaledSize: new google.maps.Size(60, 60),
            },
            {
                url: "/static/bins_img/red-empty-2.png",
                scaledSize: new google.maps.Size(60, 60),
            },
            {
                url: "/static/bins_img/red-empty-3.png",
                scaledSize: new google.maps.Size(60, 60),
            },
        ],
    };

    const fullBinIcon = {
        green: [
            {
                url: "/static/bins_img/green-full-2.png",
                scaledSize: new google.maps.Size(80, 80),
            },
            {
                url: "/static/bins_img/green-full-1.png",
                scaledSize: new google.maps.Size(80, 80),
            },
            {
                url: "/static/bins_img/green-full-3.png",
                scaledSize: new google.maps.Size(70, 70),
            },
        ],
        red: [
            {
                url: "/static/bins_img/red-full-1.png",
                scaledSize: new google.maps.Size(80, 80),
            },
            {
                url: "/static/bins_img/red-full-2.png",
                scaledSize: new google.maps.Size(80, 80),
            },
            {
                url: "/static/bins_img/red-full-3.png",
                scaledSize: new google.maps.Size(80, 80),
            },
        ],
    };

    // Bin data goes here...
    // const bins = {{ bins_data_json|safe }};
    // const binData = [];

    // for(var idx in bins){
    //     binData.push({
    //         id: bins[idx].pk,
    //         name: bins[idx].fields.name,
    //         location: bins[idx].fields.location,
    //         lat: Number(bins[idx].fields.latitude),
    //         lng: Number(bins[idx].fields.longitude),
    //         garbage_level: Number(bins[idx].fields.garbage_level),
    //         moisture_status: bins[idx].fields.moisture_status,
    //         isFull: Number(bins[idx].fields.garbage_level) > 60,
    //         type: bins[idx].fields.moisture_status == true ? "green" : "red",
    //     });
    // }

    const bhubaneswar = { lat: 20.2961, lng: 85.8245 };
    const map = new google.maps.Map(document.getElementById('map'), {
        center: bhubaneswar,
        zoom: 10,
        mapTypeControl: false,
    });

    const bounds = new google.maps.LatLngBounds(); // Initialize bounds
    
    let currentInfoWindow = null;
    let currentDirectionsRenderer = null;
    let openInfoWindows = [];

    let iconIndex = 0;
    // Create markers with custom bin icons and open info windows by default
    binData.forEach(bin => {
        const marker = new google.maps.Marker({
            position: { lat: bin.lat, lng: bin.lng },
            map: map,
            title: bin.name + "\n" +bin.location,
            label: {
                text: bin.garbage_level + "%",            // The label text
                className: "custom-label",
                color: "white",
            },
            icon: bin.isFull ? fullBinIcon[bin.type][iconIndex] : emptyBinIcon[bin.type][iconIndex] // Set icon from the array
        });
        
        // Increment the icon index or reset it to 0
        iconIndex = (iconIndex + 1) % emptyBinIcon.green.length;

        if (bin.isFull) {
            const infoWindow = new google.maps.InfoWindow({
                content: `
                    <div class="info-window">
                        <h3>${bin.name} is full</h3>
                        <p>Location: ${bin.location}</p>
                        <p>Garbage Level: ${bin.garbage_level}%</p>
                        <a href="/details/?bin_id=${ bin.id }" target="_blank">Learn more</a>
                    </div>
                `
            });
            infoWindow.open(map, marker);
            openInfoWindows.push(infoWindow); // Add to the array of open info windows
            marker.setAnimation(google.maps.Animation.BOUNCE);
        }

        marker.addListener("click", () => {
            // Marker animation toggling
            if (marker.getAnimation() !== null) {
                marker.setAnimation(null);
            }

            //close status info windos
            let len = openInfoWindows.length;
            for(var i = 0; i < len; i++){
                var infoWin = openInfoWindows.pop();
                infoWin.close();
            }

            // Close previous info window
            if (currentInfoWindow) {
                currentInfoWindow.close();
            }

            // Remove previous directions renderer
            if (currentDirectionsRenderer) {
                currentDirectionsRenderer.setMap(null);
            }
            
            // Nearest bin calculation and directions rendering
            let nearestBinDistance = Number.MAX_SAFE_INTEGER; // Initialize with a large value
            let nearestBinLat = null;
            let nearestBinLng = null;
    
            // Calculate distance to all other bins
            binData.forEach(otherBin => {
                if (otherBin !== bin) {
                    const distance = google.maps.geometry.spherical.computeDistanceBetween(
                        new google.maps.LatLng(bin.lat, bin.lng),
                        new google.maps.LatLng(otherBin.lat, otherBin.lng)
                    );
    
                    if (distance < nearestBinDistance) {
                        nearestBinDistance = distance;
                        nearestBinLat = otherBin.lat;
                        nearestBinLng = otherBin.lng;
                    }
                }
            });
    
            if (nearestBinLat !== null && nearestBinLng !== null) {
                const directionsService = new google.maps.DirectionsService();
                const request = {
                    origin: new google.maps.LatLng(bin.lat, bin.lng),
                    destination: new google.maps.LatLng(nearestBinLat, nearestBinLng),
                    travelMode: google.maps.TravelMode.DRIVING,
                };
    
                directionsService.route(request, (result, status) => {
                    if (status === google.maps.DirectionsStatus.OK) {
                        const directionsRenderer = new google.maps.DirectionsRenderer();
                        directionsRenderer.setMap(map);
                        directionsRenderer.setDirections(result);
    
                        const distance = result.routes[0].legs[0].distance.text;
    
                        const infoWindow = new google.maps.InfoWindow({
                            content: `<div class="info-window">
                                        <h3>${bin.name}</h3>
                                        <p>Location: ${bin.location}</p>
                                        <p>Nearest bin is ${distance} away</p>
                                      </div>`
                        });

                        currentDirectionsRenderer = directionsRenderer;
                        currentInfoWindow = infoWindow;
    
                        infoWindow.open(map, marker);
                    } else {
                        console.error('Directions request failed:', status);
                    }
                });
            }
        });
        bounds.extend(marker.getPosition());
    });

    const padding = { top: 100, right: 0, bottom: 10, left: 0 }; // Adjust padding values as needed
    map.fitBounds(bounds, padding);
}

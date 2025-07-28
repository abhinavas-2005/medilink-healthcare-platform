// function getLocationAndFilter() {
//     if (navigator.geolocation) {
//         navigator.geolocation.getCurrentPosition(function (position) {
//             const userLat = position.coords.latitude;
//             const userLng = position.coords.longitude;
//             const radius = parseFloat(document.getElementById('radius').value) || 5;

//             const hospitals = document.querySelectorAll('#hospital-list li');
//             hospitals.forEach(hospital => {
//                 const lat = parseFloat(hospital.getAttribute('data-lat'));
//                 const lng = parseFloat(hospital.getAttribute('data-lng'));
//                 const distance = getDistanceFromLatLonInKm(userLat, userLng, lat, lng);

//                 if (distance <= radius) {
//                     hospital.style.display = 'list-item';
//                 } else {
//                     hospital.style.display = 'none';
//                 }
//             });

//             initMap(userLat, userLng);
//         });
//     }
// }

// function initMap(userLat, userLng) {
//     const map = new google.maps.Map(document.getElementById("map"), {
//         zoom: 12,
//         center: { lat: userLat, lng: userLng },
//     });

//     new google.maps.Marker({
//         position: { lat: userLat, lng: userLng },
//         map,
//         label: "You"
//     });

//     document.querySelectorAll('#hospital-list li').forEach(hospital => {
//         if (hospital.style.display !== 'none') {
//             const lat = parseFloat(hospital.getAttribute('data-lat'));
//             const lng = parseFloat(hospital.getAttribute('data-lng'));
//             new google.maps.Marker({
//                 position: { lat, lng },
//                 map,
//                 label: hospital.textContent.trim().split(' ')[0]
//             });
//         }
//     });
// }

// function getDistanceFromLatLonInKm(lat1, lon1, lat2, lon2) {
//     const R = 6371;
//     const dLat = deg2rad(lat2 - lat1);
//     const dLon = deg2rad(lon2 - lon1);
//     const a =
//         Math.sin(dLat / 2) * Math.sin(dLat / 2) +
//         Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) *
//         Math.sin(dLon / 2) * Math.sin(dLon / 2);
//     const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
//     return R * c;
// }

// function deg2rad(deg) {
//     return deg * (Math.PI / 180);
// }





// function initMap(userLat, userLng) {
//     const map = new google.maps.Map(document.getElementById("map"), {
//         zoom: 12,
//         center: { lat: userLat, lng: userLng },
//     });

//     new google.maps.Marker({
//         position: { lat: userLat, lng: userLng },
//         map,
//         label: "You"
//     });

//     const geocoder = new google.maps.Geocoder();

//     hospitalsFromServer.forEach(hospital => {
//         geocoder.geocode({ address: hospital.address }, (results, status) => {
//             if (status === "OK") {
//                 const marker = new google.maps.Marker({
//                     map: map,
//                     position: results[0].geometry.location,
//                     label: {
//                         text: hospital.name,
//                         className: 'hospital-label'
//                     }
//                 });

//                 const infoWindow = new google.maps.InfoWindow({
//                     content: `
//                         <strong>${hospital.name}</strong><br/>
//                         ${hospital.address}<br/>
//                         Beds: ${hospital.available_beds > 0 ? hospital.available_beds : "Fully Occupied"}
//                     `
//                 });

//                 marker.addListener("click", () => {
//                     infoWindow.open(map, marker);
//                 });

//             } else {
//                 console.warn(`Geocode failed for ${hospital.name}: ${status}`);
//             }
//         });
//     });
// }


// function getLocationAndFilter() {
//     if (navigator.geolocation) {
//         navigator.geolocation.getCurrentPosition(function (position) {
//             const userLat = position.coords.latitude;
//             const userLng = position.coords.longitude;
//             const radius = parseFloat(document.getElementById('radius').value) || 5; // default 5 km

//             initMap(userLat, userLng, radius);
//         });
//     } else {
//         alert("Geolocation is not supported by this browser.");
//     }
// }

// function initMap(userLat, userLng, radiusKm) {
//     const radiusKm = parseFloat(document.getElementById("radius").value) || 5;
//     const map = new google.maps.Map(document.getElementById("map"), {
//         zoom: 12,
//         center: { lat: userLat, lng: userLng },
//     });

//     // User location marker
//     new google.maps.Marker({
//         position: { lat: userLat, lng: userLng },
//         map,
//         label: "You"
//     });

//     const geocoder = new google.maps.Geocoder();


    
//     hospitalsFromServer.forEach(hospital => {
//         geocoder.geocode({ address: hospital.address }, (results, status) => {
//             if (status === "OK") {
//                 const location = results[0].geometry.location;
//                 const hospitalLat = location.lat();
//                 const hospitalLng = location.lng();

//                 const distance = getDistanceFromLatLonInKm(userLat, userLng, hospitalLat, hospitalLng);

//                 if (distance <= radiusKm) {
//                     const marker = new google.maps.Marker({
//                         map,
//                         position: location,
//                         label: {
//                             text: hospital.name,
//                             className: 'hospital-label'
//                         }
//                     });

//                     const infoWindow = new google.maps.InfoWindow({
//                         content: `
//                             <strong>${hospital.name}</strong><br/>
//                             ${hospital.address}<br/>
//                             Beds: ${hospital.available_beds > 0 ? hospital.available_beds : "Fully Occupied"}
//                         `
//                     });

//                     marker.addListener("click", () => {
//                         infoWindow.open(map, marker);
//                     });
//                 }
//             } else {
//                 console.warn(`Geocode failed for ${hospital.name}: ${status}`);
//             }
//         });
//     });
// }

// // Haversine formula to calculate distance
// function getDistanceFromLatLonInKm(lat1, lon1, lat2, lon2) {
//     const R = 6371; // Radius of the earth in km
//     const dLat = deg2rad(lat2 - lat1);
//     const dLon = deg2rad(lon2 - lon1);
//     const a =
//         Math.sin(dLat / 2) * Math.sin(dLat / 2) +
//         Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) *
//         Math.sin(dLon / 2) * Math.sin(dLon / 2);
//     const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
//     return R * c;
// }

// function deg2rad(deg) {
//     return deg * (Math.PI / 180);
// }



// function getDistanceFromLatLonInKm(lat1, lon1, lat2, lon2) {
//     const R = 6371; // Radius of Earth in km
//     const dLat = deg2rad(lat2 - lat1);
//     const dLon = deg2rad(lon2 - lon1);
//     const a =
//         Math.sin(dLat / 2) * Math.sin(dLat / 2) +
//         Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) *
//         Math.sin(dLon / 2) * Math.sin(dLon / 2);
//     const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
//     return R * c;
// }

// function deg2rad(deg) {
//     return deg * (Math.PI / 180);
// }

// function initMap(userLat, userLng) {
//     const radiusKm = parseFloat(document.getElementById("radius").value) || 5;

//     const map = new google.maps.Map(document.getElementById("map"), {
//         zoom: 12,
//         center: { lat: userLat, lng: userLng },
//     });

//     new google.maps.Marker({
//         position: { lat: userLat, lng: userLng },
//         map,
//         label: "You",
//     });

//     const geocoder = new google.maps.Geocoder();

//     // Rate limit handler
//     let index = 0;
//     function processNextHospital() {
//         if (index >= hospitalsFromServer.length) return;

//         const hospital = hospitalsFromServer[index];
//         geocoder.geocode({ address: hospital.address }, (results, status) => {
//             if (status === "OK" && results[0]) {
//                 const location = results[0].geometry.location;
//                 const hospitalLat = location.lat();
//                 const hospitalLng = location.lng();

//                 const distance = getDistanceFromLatLonInKm(userLat, userLng, hospitalLat, hospitalLng);

//                 if (distance <= radiusKm) {
//                     const marker = new google.maps.Marker({
//                         map,
//                         position: location,
//                         label: {
//                             text: hospital.name,
//                             className: 'hospital-label'
//                         }
//                     });

//                     const infoWindow = new google.maps.InfoWindow({
//                         content: `
//                             <strong>${hospital.name}</strong><br/>
//                             ${hospital.address}<br/>
//                             Beds: ${hospital.available_beds > 0 ? hospital.available_beds : "Fully Occupied"}
//                         `
//                     });

//                     marker.addListener("click", () => {
//                         infoWindow.open(map, marker);
//                     });
//                 }
//             } else {
//                 console.warn(`Geocode failed for ${hospital.name}: ${status}`);
//             }

//             index++;
//             setTimeout(processNextHospital, 200); // delay to avoid rate limit
//         });
//     }

//     processNextHospital(); // start processing
// }






function deg2rad(deg) {
    return deg * (Math.PI / 180);
}

function getDistanceFromLatLonInKm(lat1, lon1, lat2, lon2) {
    const R = 6371; // km
    const dLat = deg2rad(lat2 - lat1);
    const dLon = deg2rad(lon2 - lon1);
    const a =
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) *
        Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
}

function initMap(userLat, userLng) {
    const radiusKm = parseFloat(document.getElementById("radius").value) || 10;
    const map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: userLat, lng: userLng },
        zoom: 12
    });

    new google.maps.Marker({
        position: { lat: userLat, lng: userLng },
        map,
        label: "You"
    });

    const geocoder = new google.maps.Geocoder();
    let index = 0;

    function processNext() {
        if (index >= hospitalsFromServer.length) return;

        const hospital = hospitalsFromServer[index];
        geocoder.geocode({ address: hospital.address }, (results, status) => {
            if (status === "OK" && results[0]) {
                const location = results[0].geometry.location;
                const lat = location.lat();
                const lng = location.lng();
                const distance = getDistanceFromLatLonInKm(userLat, userLng, lat, lng);

                if (distance <= radiusKm) {
                    const marker = new google.maps.Marker({
                        map,
                        position: location,
                        label: {
                            text: hospital.name,
                            className: 'hospital-label'
                        }
                    });

                    const infoWindow = new google.maps.InfoWindow({
                        content: `
                            <strong>${hospital.name}</strong><br/>
                            ${hospital.address}<br/>
                            Beds: ${hospital.available_beds > 0 ? hospital.available_beds : "Fully Occupied"}
                        `
                    });

                    marker.addListener("click", () => infoWindow.open(map, marker));
                }
            } else {
                console.warn(`Geocode failed for ${hospital.name}: ${status}`);
            }

            index++;
            setTimeout(processNext, 200); // Prevent rate limiting
        });
    }

    processNext();
}

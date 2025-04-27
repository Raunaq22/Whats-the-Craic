document.addEventListener('DOMContentLoaded', function () {
     var map = L.map('map').setView([53.3498, -6.262], 11);

     L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
         attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
     }).addTo(map);

     var marker;

     map.on('click', function (e) {
         if (marker) {
             map.removeLayer(marker);
         }
         marker = L.marker(e.latlng).addTo(map);
         var selectedLocation = e.latlng.lat + ', ' + e.latlng.lng;
         document.getElementById('id_location').value = selectedLocation;
         document.getElementById('selected-location').value = selectedLocation;

         // Fetch address based on the selected location
         fetchAddress(e.latlng.lat, e.latlng.lng);
     });

     function fetchAddress(lat, lon) {
         fetch(`https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lon}&format=json`)
             .then(response => response.json())
             .then(data => {
                 if (data.display_name) {
                     document.getElementById('id_location').value = data.display_name;
                     document.getElementById('location-help').textContent = '';
                 } else {
                     document.getElementById('location-help').textContent = 'Please choose a valid place.';
                 }
             })
             .catch(error => {
                 console.error('Error fetching address:', error);
                 document.getElementById('location-help').textContent = 'Please choose a valid place.';
             });
     }
 });


$(document).on('change', '.custom-file-input', function (event) {
        $(this).next('.custom-file-label').html(event.target.files[0].name);
    });


$(document).ready(function() {
    var currentUrl = window.location.href;

    $('.navbar-nav .nav-link').each(function() {
        // Get the link's href attribute
        var linkHref = $(this).attr('href');

        // Check if the current URL contains the link's href
        if (currentUrl.indexOf(linkHref) !== -1 && linkHref !== '/') {
            // Add the active class to the link's parent list item
            $(this).closest('.nav-item').addClass('active');
        }
    });
});

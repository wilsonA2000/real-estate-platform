/**
 * Script para manejar la selección de ubicación en el formulario de propiedades
 */
document.addEventListener('DOMContentLoaded', function() {
    // Obtener referencias a los elementos del DOM
    const mapContainer = document.getElementById('mapbox-map');
    const geocoderContainer = document.getElementById('mapbox-geocoder');
    const exactAddressInput = document.getElementById('id_exact_address');
    const latitudeInput = document.getElementById('id_latitude');
    const longitudeInput = document.getElementById('id_longitude');
    const locationPreview = document.getElementById('location-preview');
    const selectedAddressSpan = document.getElementById('selected-address');
    
    // Verificar si estamos en la página del formulario de propiedades
    if (!mapContainer || !geocoderContainer) return;
    
    // Mostrar el contenedor de ubicación si ya hay coordenadas
    if (latitudeInput && latitudeInput.value && longitudeInput && longitudeInput.value) {
        locationPreview.style.display = 'block';
    }
    
    // Inicializar variables globales para coordenadas y dirección
    window.pendingCoords = null;
    window.pendingPlace = null;
    let marker;
    
    // Inicializar el mapa
    mapboxgl.accessToken = 'pk.eyJ1Ijoid2lsc29uYXJndWVsbG8yMDI1IiwiYSI6ImNtYm1zcmg1aDE0NTkyam9rZDRkNzF5YWoifQ.FgvTtKt3AK5uxcoz8BHtmw';
    const map = new mapboxgl.Map({
        container: 'mapbox-map',
        style: 'mapbox://styles/mapbox/streets-v11',
        center: [longitudeInput.value ? parseFloat(longitudeInput.value) : -74.297333, 
                latitudeInput.value ? parseFloat(latitudeInput.value) : 4.570868],
        zoom: (latitudeInput.value && longitudeInput.value) ? 15 : 5,
        locale: 'es-ES'
    });
    map.addControl(new mapboxgl.NavigationControl());

    // Geocoder para búsqueda de direcciones
    const geocoder = new MapboxGeocoder({
        accessToken: mapboxgl.accessToken,
        mapboxgl: mapboxgl,
        marker: false,
        language: 'es',
        placeholder: 'Buscar dirección en español...',
        countries: 'CO',
        bbox: [-81.0, -4.0, -66.0, 13.0] // Limita a Colombia
    });
    geocoderContainer.appendChild(geocoder.onAdd(map));

    // Evento al seleccionar una dirección
    geocoder.on('result', function(e) {
        const coords = e.result.center;
        const place = e.result.place_name;
        
        if (marker) marker.remove();
        marker = new mapboxgl.Marker({ draggable: true })
            .setLngLat(coords)
            .addTo(map);
        
        map.flyTo({ center: coords, zoom: 16 });
        
        // Actualizar el campo de dirección exacta automáticamente
        exactAddressInput.value = place;
        
        // Actualizar la vista previa
        locationPreview.style.display = 'block';
        selectedAddressSpan.textContent = place;
        
        // Guardar en variables globales para acceso desde otros scripts
        // Redondear coordenadas a 6 decimales usando Math.round
        const roundedLng = Math.round(coords[0] * 1000000) / 1000000;
        const roundedLat = Math.round(coords[1] * 1000000) / 1000000;
        window.pendingCoords = [roundedLng, roundedLat];
        window.pendingPlace = place;
        
        // Configurar el evento de arrastre del marcador
        setupMarkerDragEvent(marker);
    });

    // Mover marcador manualmente al hacer clic en el mapa
    map.on('click', function(e) {
        if (marker) {
            marker.setLngLat(e.lngLat);
        } else {
            marker = new mapboxgl.Marker({ draggable: true })
                .setLngLat(e.lngLat)
                .addTo(map);
                
            // Configurar el evento de arrastre del marcador
            setupMarkerDragEvent(marker);
        }
        
        // Redondear coordenadas a 6 decimales usando Math.round
        const roundedLng = Math.round(e.lngLat.lng * 1000000) / 1000000;
        const roundedLat = Math.round(e.lngLat.lat * 1000000) / 1000000;
        window.pendingCoords = [roundedLng, roundedLat];
        
        // Hacer reverse geocoding para obtener la dirección
        reverseGeocode(roundedLng, roundedLat);
    });

    // Función para configurar el evento de arrastre del marcador
    function setupMarkerDragEvent(marker) {
        marker.on('dragend', function() {
            const lngLat = marker.getLngLat();
            // Redondear coordenadas a 6 decimales usando Math.round
            const roundedLng = Math.round(lngLat.lng * 1000000) / 1000000;
            const roundedLat = Math.round(lngLat.lat * 1000000) / 1000000;
            window.pendingCoords = [roundedLng, roundedLat];
            
            // Hacer reverse geocoding para obtener la dirección
            reverseGeocode(roundedLng, roundedLat);
        });
    }

    // Función para hacer reverse geocoding
    function reverseGeocode(lng, lat) {
        // Asegurarse de que las coordenadas estén redondeadas a 6 decimales usando Math.round
        const roundedLng = Math.round(lng * 1000000) / 1000000;
        const roundedLat = Math.round(lat * 1000000) / 1000000;
        
        const reverseGeocodingUrl = `https://api.mapbox.com/geocoding/v5/mapbox.places/${roundedLng},${roundedLat}.json?access_token=${mapboxgl.accessToken}&language=es`;
        
        fetch(reverseGeocodingUrl)
            .then(response => response.json())
            .then(data => {
                if (data.features && data.features.length > 0) {
                    window.pendingPlace = data.features[0].place_name;
                } else {
                    window.pendingPlace = `Ubicación en ${roundedLat}, ${roundedLng}`;
                }
                
                selectedAddressSpan.textContent = window.pendingPlace;
                exactAddressInput.value = window.pendingPlace;
                
                // Mostrar el contenedor de ubicación
                locationPreview.style.display = 'block';
            })
            .catch(error => {
                window.pendingPlace = `Ubicación en ${roundedLat}, ${roundedLng}`;
                selectedAddressSpan.textContent = window.pendingPlace;
                exactAddressInput.value = window.pendingPlace;
                
                // Mostrar el contenedor de ubicación
                locationPreview.style.display = 'block';
            });
    }

    // Cargar marcador si hay coordenadas iniciales
    if (latitudeInput.value && longitudeInput.value) {
        const lng = parseFloat(longitudeInput.value);
        const lat = parseFloat(latitudeInput.value);
        
        // Asegurarse de que las coordenadas iniciales estén redondeadas a 6 decimales usando Math.round
        const roundedLng = Math.round(lng * 1000000) / 1000000;
        const roundedLat = Math.round(lat * 1000000) / 1000000;
        
        marker = new mapboxgl.Marker({ draggable: true })
            .setLngLat([roundedLng, roundedLat])
            .addTo(map);
        map.flyTo({ center: [roundedLng, roundedLat], zoom: 15 });
        
        // Configurar el evento de arrastre del marcador
        setupMarkerDragEvent(marker);
        
        // Establecer las coordenadas pendientes para que se puedan confirmar
        window.pendingCoords = [roundedLng, roundedLat];
        
        // Mostrar la dirección exacta si existe, o hacer reverse geocoding
        if (exactAddressInput.value) {
            window.pendingPlace = exactAddressInput.value;
            selectedAddressSpan.textContent = window.pendingPlace;
            locationPreview.style.display = 'block';
        } else {
            reverseGeocode(lng, lat);
        }
    }
});
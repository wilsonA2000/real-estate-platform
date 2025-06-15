/**
 * Script para renderizar el mapa de Mapbox en la vista detallada de propiedades
 */
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar el mapa con Mapbox si existe el contenedor
    if (document.getElementById('mapbox-detail-map')) {
        const mapContainer = document.getElementById('mapbox-detail-map');
        
        // Obtener las coordenadas del data-attribute o de las variables globales
        const lat = parseFloat(mapContainer.dataset.lat);
        const lng = parseFloat(mapContainer.dataset.lng);
        const address = mapContainer.dataset.address || '';
        
        if (!isNaN(lat) && !isNaN(lng)) {
            mapboxgl.accessToken = 'pk.eyJ1Ijoid2lsc29uYXJndWVsbG8yMDI1IiwiYSI6ImNtYm1zcmg1aDE0NTkyam9rZDRkNzF5YWoifQ.FgvTtKt3AK5uxcoz8BHtmw';
            
            // Crear el mapa
            const map = new mapboxgl.Map({
                container: 'mapbox-detail-map',
                style: 'mapbox://styles/mapbox/streets-v11',
                center: [lng, lat], // Usar las coordenadas guardadas
                zoom: 15,
                locale: 'es-ES'
            });
            
            // Añadir controles de navegación
            map.addControl(new mapboxgl.NavigationControl());
            
            // Añadir marcador en la ubicación exacta
            const marker = new mapboxgl.Marker({color: '#F59E0B'})
                .setLngLat([lng, lat])
                .addTo(map);
            
            // Añadir popup con la dirección exacta si existe
            if (address) {
                const popup = new mapboxgl.Popup({
                    offset: 25,
                    closeButton: false,
                    closeOnClick: false
                })
                .setLngLat([lng, lat])
                .setHTML(`<div class="font-medium text-gray-900 p-1">${address}</div>`)
                .addTo(map);
            }
            
            // Asegurar que el mapa se renderice correctamente
            map.on('load', function() {
                setTimeout(function() {
                    map.resize();
                }, 200);
            });
        } else {
            mapContainer.innerHTML = '<div class="flex items-center justify-center h-full bg-gray-100 text-gray-600 p-4 text-center">No se pudieron cargar las coordenadas del mapa</div>';
        }
    }
});
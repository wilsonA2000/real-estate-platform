/**
 * Script para mostrar el contenedor de ubicación en el formulario de propiedades
 */
document.addEventListener('DOMContentLoaded', function() {
    // Obtener referencias a los elementos del DOM
    const locationPreview = document.getElementById('location-preview');
    const latitudeInput = document.getElementById('id_latitude');
    const longitudeInput = document.getElementById('id_longitude');
    
    // Si no estamos en la página del formulario, salir
    if (!locationPreview || !latitudeInput || !longitudeInput) return;
    
    // Mostrar el contenedor de ubicación si ya hay coordenadas
    if (latitudeInput.value && longitudeInput.value) {
        locationPreview.style.display = 'block';
    }
    
    // Mostrar el contenedor cuando se hace clic en el mapa
    const mapContainer = document.getElementById('mapbox-map');
    if (mapContainer) {
        mapContainer.addEventListener('click', function() {
            setTimeout(function() {
                locationPreview.style.display = 'block';
            }, 500);
        });
    }
});
/**
 * Script para manejar la confirmación de ubicación en el formulario de propiedades
 */
document.addEventListener('DOMContentLoaded', function() {
    // Obtener referencias a los elementos del DOM
    const confirmBtn = document.getElementById('confirm-mapbox-location');
    const modal = document.getElementById('location-modal');
    const modalText = document.getElementById('modal-location-text');
    const modalYes = document.getElementById('modal-location-yes');
    const modalNo = document.getElementById('modal-location-no');
    const selectedAddressSpan = document.getElementById('selected-address');
    const confirmMsg = document.getElementById('confirm-address-message');
    const latitudeInput = document.getElementById('id_latitude');
    const longitudeInput = document.getElementById('id_longitude');
    const exactAddressInput = document.getElementById('id_exact_address');
    const locationPreview = document.getElementById('location-preview');
    const locationStatus = document.getElementById('location-status');
    
    // Si no estamos en la página del formulario, salir
    if (!confirmBtn || !modal || !selectedAddressSpan) return;
    
    // Mostrar el contenedor de ubicación si ya hay coordenadas
    if (latitudeInput && latitudeInput.value && longitudeInput && longitudeInput.value) {
        locationPreview.style.display = 'block';
        if (locationStatus) {
            locationStatus.innerHTML = '<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800"><svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path></svg>Dirección guardada</span>';
        }
        
        // Mostrar mensaje de confirmación
        confirmMsg.textContent = '✅ Ubicación guardada correctamente';
        confirmMsg.style.display = 'block';
        confirmMsg.style.color = '#10B981'; // Color verde
        confirmMsg.style.padding = '0.5rem';
        confirmMsg.style.borderRadius = '0.25rem';
        confirmMsg.style.backgroundColor = '#ECFDF5'; // Fondo verde claro
    }
    
    // Si existe el botón de confirmar ubicación
    confirmBtn.addEventListener('click', function() {
        const selectedAddress = selectedAddressSpan.textContent;
        if (selectedAddress !== 'No seleccionada') {
            // Mostrar modal de confirmación
            modalText.textContent = `¿Estás seguro de que quieres establecer la ubicación en "${selectedAddress}"?`;
            modal.style.display = 'flex';
            
            // Limpiar mensajes anteriores
            confirmMsg.style.display = 'none';
        } else {
            confirmMsg.textContent = 'Por favor, selecciona primero una ubicación en el mapa';
            confirmMsg.style.display = 'block';
            confirmMsg.style.color = '#EF4444'; // Color rojo
            confirmMsg.style.padding = '0.5rem';
            confirmMsg.style.borderRadius = '0.25rem';
            confirmMsg.style.backgroundColor = '#FEF2F2'; // Fondo rojo claro
        }
    });
    
    // Si existe el botón de confirmar en el modal
    modalYes.addEventListener('click', function() {
        modal.style.display = 'none';
        
        // Guardar coordenadas si están disponibles
        if (window.pendingCoords) {
            // Asegurarse de que las coordenadas estén redondeadas a exactamente 6 decimales usando Math.round
            const lat = Math.round(window.pendingCoords[1] * 1000000) / 1000000;
            const lng = Math.round(window.pendingCoords[0] * 1000000) / 1000000;
            
            // Establecer nuevos valores con formato fijo de 6 decimales
            latitudeInput.value = lat.toFixed(6);
            longitudeInput.value = lng.toFixed(6);
            
            console.log('Coordenadas redondeadas:', lat.toFixed(6), lng.toFixed(6));
            
            if (window.pendingPlace) {
                exactAddressInput.value = window.pendingPlace;
            }
            
            // Actualizar indicador de estado
            if (locationStatus) {
                locationStatus.innerHTML = '<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800"><svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path></svg>Dirección guardada</span>';
            }
            
            // Mostrar mensaje de confirmación
            confirmMsg.textContent = '✅ Ubicación guardada correctamente';
            confirmMsg.style.display = 'block';
            confirmMsg.style.color = '#10B981'; // Color verde
            confirmMsg.style.padding = '0.5rem';
            confirmMsg.style.borderRadius = '0.25rem';
            confirmMsg.style.backgroundColor = '#ECFDF5'; // Fondo verde claro
        }
    });
    
    // Si existe el botón de cancelar en el modal
    modalNo.addEventListener('click', function() {
        modal.style.display = 'none';
    });
});
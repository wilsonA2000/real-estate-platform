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
    
    // Variables para almacenar las coordenadas pendientes
    let pendingCoords = null;
    let pendingPlace = null;
    
    // Si existe el botón de confirmar ubicación
    if (confirmBtn) {
        confirmBtn.addEventListener('click', function() {
            const selectedAddress = selectedAddressSpan.textContent;
            if (selectedAddress !== 'No seleccionada') {
                // Mostrar modal de confirmación
                modalText.textContent = `¿Estás seguro de que quieres establecer la ubicación en "${selectedAddress}"?`;
                modal.style.display = 'flex';
                
                // Guardar las coordenadas pendientes
                if (window.pendingCoords) {
                    pendingCoords = window.pendingCoords;
                    pendingPlace = window.pendingPlace;
                }
            }
        });
    }
    
    // Si existe el botón de confirmar en el modal
    if (modalYes) {
        modalYes.addEventListener('click', function() {
            modal.style.display = 'none';
            
            // Guardar coordenadas si están disponibles
            if (pendingCoords) {
                latitudeInput.value = pendingCoords[1];
                longitudeInput.value = pendingCoords[0];
                if (pendingPlace) {
                    exactAddressInput.value = pendingPlace;
                }
            }
            
            // Mostrar mensaje de confirmación
            confirmMsg.textContent = '✅ Ubicación confirmada correctamente';
            confirmMsg.style.display = 'block';
            confirmMsg.style.color = '#10B981'; // Color verde
            confirmMsg.style.padding = '0.5rem';
            confirmMsg.style.borderRadius = '0.25rem';
            confirmMsg.style.backgroundColor = '#ECFDF5'; // Fondo verde claro
            
            // Ocultar el mensaje después de 3 segundos
            setTimeout(function() {
                confirmMsg.style.display = 'none';
            }, 3000);
        });
    }
    
    // Si existe el botón de cancelar en el modal
    if (modalNo) {
        modalNo.addEventListener('click', function() {
            modal.style.display = 'none';
        });
    }
});
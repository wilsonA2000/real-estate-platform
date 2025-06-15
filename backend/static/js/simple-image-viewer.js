// Script para el visor de imágenes mejorado
document.addEventListener('DOMContentLoaded', function() {
    // Crear el modal para las imágenes
    const modalContainer = document.createElement('div');
    modalContainer.id = 'image-modal';
    modalContainer.style.display = 'none';
    modalContainer.style.position = 'fixed';
    modalContainer.style.zIndex = '9999';
    modalContainer.style.left = '0';
    modalContainer.style.top = '0';
    modalContainer.style.width = '100%';
    modalContainer.style.height = '100%';
    modalContainer.style.backgroundColor = 'rgba(0,0,0,0.9)';
    modalContainer.style.alignItems = 'center';
    modalContainer.style.justifyContent = 'center';
    
    // Contenedor para la imagen y controles - maximizando el espacio
    const viewerContainer = document.createElement('div');
    viewerContainer.style.position = 'relative';
    viewerContainer.style.width = '100%';
    viewerContainer.style.height = '100%';
    viewerContainer.style.display = 'flex';
    viewerContainer.style.flexDirection = 'column';
    viewerContainer.style.alignItems = 'center';
    viewerContainer.style.justifyContent = 'center';
    
    // Imagen principal - Tamaño moderado (reducido en 30%)
    const modalImage = document.createElement('img');
    modalImage.id = 'modal-image';
    modalImage.style.width = '70%';
    modalImage.style.height = '70%';
    modalImage.style.objectFit = 'contain';
    modalImage.style.borderRadius = '4px';
    modalImage.style.boxShadow = '0 4px 12px rgba(0,0,0,0.5)';
    modalImage.style.transition = 'transform 0.3s ease';
    
    // Botones de navegación
    const prevButton = document.createElement('button');
    prevButton.id = 'prev-image';
    prevButton.innerHTML = '&#10094;';
    prevButton.style.position = 'absolute';
    prevButton.style.left = '20px';
    prevButton.style.top = '50%';
    prevButton.style.transform = 'translateY(-50%)';
    prevButton.style.backgroundColor = 'rgba(0,0,0,0.5)';
    prevButton.style.color = 'white';
    prevButton.style.border = 'none';
    prevButton.style.borderRadius = '50%';
    prevButton.style.width = '60px';
    prevButton.style.height = '60px';
    prevButton.style.fontSize = '24px';
    prevButton.style.cursor = 'pointer';
    prevButton.style.zIndex = '10000';
    
    const nextButton = document.createElement('button');
    nextButton.id = 'next-image';
    nextButton.innerHTML = '&#10095;';
    nextButton.style.position = 'absolute';
    nextButton.style.right = '20px';
    nextButton.style.top = '50%';
    nextButton.style.transform = 'translateY(-50%)';
    nextButton.style.backgroundColor = 'rgba(0,0,0,0.5)';
    nextButton.style.color = 'white';
    nextButton.style.border = 'none';
    nextButton.style.borderRadius = '50%';
    nextButton.style.width = '60px';
    nextButton.style.height = '60px';
    nextButton.style.fontSize = '24px';
    nextButton.style.cursor = 'pointer';
    nextButton.style.zIndex = '10000';
    
    // Contador de imágenes
    const imageCounter = document.createElement('div');
    imageCounter.id = 'image-counter';
    imageCounter.style.position = 'absolute';
    imageCounter.style.top = '20px';
    imageCounter.style.left = '20px';
    imageCounter.style.backgroundColor = 'rgba(0,0,0,0.6)';
    imageCounter.style.color = 'white';
    imageCounter.style.padding = '8px 15px';
    imageCounter.style.borderRadius = '20px';
    imageCounter.style.fontSize = '16px';
    imageCounter.style.fontWeight = 'bold';
    
    // Barra de herramientas simple
    const toolbar = document.createElement('div');
    toolbar.style.display = 'flex';
    toolbar.style.justifyContent = 'center';
    toolbar.style.gap = '20px';
    toolbar.style.marginTop = '15px';
    toolbar.style.position = 'absolute';
    toolbar.style.bottom = '30px';
    toolbar.style.left = '50%';
    toolbar.style.transform = 'translateX(-50%)';
    toolbar.style.zIndex = '10000';
    
    // Botón de zoom in
    const zoomInBtn = document.createElement('button');
    zoomInBtn.innerHTML = '+';
    zoomInBtn.style.backgroundColor = 'rgba(255,255,255,0.3)';
    zoomInBtn.style.border = 'none';
    zoomInBtn.style.borderRadius = '50%';
    zoomInBtn.style.width = '50px';
    zoomInBtn.style.height = '50px';
    zoomInBtn.style.fontSize = '24px';
    zoomInBtn.style.cursor = 'pointer';
    zoomInBtn.style.color = 'white';
    
    // Botón de zoom out
    const zoomOutBtn = document.createElement('button');
    zoomOutBtn.innerHTML = '-';
    zoomOutBtn.style.backgroundColor = 'rgba(255,255,255,0.3)';
    zoomOutBtn.style.border = 'none';
    zoomOutBtn.style.borderRadius = '50%';
    zoomOutBtn.style.width = '50px';
    zoomOutBtn.style.height = '50px';
    zoomOutBtn.style.fontSize = '24px';
    zoomOutBtn.style.cursor = 'pointer';
    zoomOutBtn.style.color = 'white';
    
    // Botón de rotación
    const rotateBtn = document.createElement('button');
    rotateBtn.innerHTML = '↻';
    rotateBtn.style.backgroundColor = 'rgba(255,255,255,0.3)';
    rotateBtn.style.border = 'none';
    rotateBtn.style.borderRadius = '50%';
    rotateBtn.style.width = '50px';
    rotateBtn.style.height = '50px';
    rotateBtn.style.fontSize = '24px';
    rotateBtn.style.cursor = 'pointer';
    rotateBtn.style.color = 'white';
    
    // Botón de cerrar
    const closeButton = document.createElement('button');
    closeButton.innerHTML = '×';
    closeButton.style.position = 'absolute';
    closeButton.style.top = '20px';
    closeButton.style.right = '20px';
    closeButton.style.backgroundColor = 'rgba(255,255,255,0.3)';
    closeButton.style.border = 'none';
    closeButton.style.borderRadius = '50%';
    closeButton.style.width = '50px';
    closeButton.style.height = '50px';
    closeButton.style.fontSize = '36px';
    closeButton.style.cursor = 'pointer';
    closeButton.style.color = 'white';
    closeButton.style.display = 'flex';
    closeButton.style.alignItems = 'center';
    closeButton.style.justifyContent = 'center';
    closeButton.style.zIndex = '10000';
    
    // Añadir botones a la barra de herramientas
    toolbar.appendChild(zoomInBtn);
    toolbar.appendChild(zoomOutBtn);
    toolbar.appendChild(rotateBtn);
    
    // Añadir elementos al contenedor
    viewerContainer.appendChild(modalImage);
    viewerContainer.appendChild(toolbar);
    viewerContainer.appendChild(imageCounter);
    viewerContainer.appendChild(prevButton);
    viewerContainer.appendChild(nextButton);
    viewerContainer.appendChild(closeButton);
    modalContainer.appendChild(viewerContainer);
    document.body.appendChild(modalContainer);
    
    // Variables para el zoom y rotación
    let currentZoom = 1;
    let currentRotation = 0;
    let currentImageIndex = 0;
    let galleryImages = [];
    
    // Recopilar todas las imágenes de la galería
    function collectGalleryImages() {
        const galleryItems = document.querySelectorAll('.gallery-item');
        galleryImages = Array.from(galleryItems).map(item => {
            const img = item.querySelector('img');
            return img ? img.getAttribute('src') : null;
        }).filter(Boolean);
    }
    
    // Llamar a la función para recopilar imágenes
    collectGalleryImages();
    
    // Funcionalidad de zoom in
    zoomInBtn.onclick = function(e) {
        e.stopPropagation();
        currentZoom += 0.25;
        if (currentZoom > 4) currentZoom = 4;
        modalImage.style.transform = `scale(${currentZoom}) rotate(${currentRotation}deg)`;
    };
    
    // Funcionalidad de zoom out
    zoomOutBtn.onclick = function(e) {
        e.stopPropagation();
        currentZoom -= 0.25;
        if (currentZoom < 0.5) currentZoom = 0.5;
        modalImage.style.transform = `scale(${currentZoom}) rotate(${currentRotation}deg)`;
    };
    
    // Funcionalidad de rotación
    rotateBtn.onclick = function(e) {
        e.stopPropagation();
        currentRotation += 90;
        if (currentRotation >= 360) currentRotation = 0;
        modalImage.style.transform = `scale(${currentZoom}) rotate(${currentRotation}deg)`;
    };
    
    // Navegación entre imágenes
    function showPrevImage(e) {
        if (e) e.stopPropagation();
        if (galleryImages.length <= 1) return;
        
        currentImageIndex = (currentImageIndex - 1 + galleryImages.length) % galleryImages.length;
        modalImage.src = galleryImages[currentImageIndex];
        imageCounter.textContent = `${currentImageIndex + 1} / ${galleryImages.length}`;
        
        // Mantener el zoom en 1.05 para todas las imágenes
        currentZoom = 1.05;
        currentRotation = 0;
        modalImage.style.transform = `scale(${currentZoom}) rotate(0deg)`;
    }
    
    function showNextImage(e) {
        if (e) e.stopPropagation();
        if (galleryImages.length <= 1) return;
        
        currentImageIndex = (currentImageIndex + 1) % galleryImages.length;
        modalImage.src = galleryImages[currentImageIndex];
        imageCounter.textContent = `${currentImageIndex + 1} / ${galleryImages.length}`;
        
        // Mantener el zoom en 1.05 para todas las imágenes
        currentZoom = 1.05;
        currentRotation = 0;
        modalImage.style.transform = `scale(${currentZoom}) rotate(0deg)`;
    }
    
    prevButton.onclick = showPrevImage;
    nextButton.onclick = showNextImage;
    
    // Cerrar el modal
    function closeModal() {
        modalContainer.style.display = 'none';
        document.body.style.overflow = 'auto';
        // Resetear zoom y rotación para la próxima apertura
        currentZoom = 1.05;
        currentRotation = 0;
        modalImage.style.transform = `scale(${currentZoom}) rotate(0deg)`;
        // Eliminar el event listener del teclado
        document.removeEventListener('keydown', handleKeyDown);
    }
    
    closeButton.onclick = function(e) {
        e.stopPropagation();
        closeModal();
    };
    
    // Cerrar al hacer clic fuera de la imagen
    modalContainer.onclick = function(event) {
        if (event.target === modalContainer) {
            closeModal();
        }
    };
    
    // Manejar eventos de teclado
    function handleKeyDown(e) {
        if (modalContainer.style.display === 'flex') {
            if (e.key === 'ArrowLeft') {
                showPrevImage();
            } else if (e.key === 'ArrowRight') {
                showNextImage();
            } else if (e.key === 'Escape') {
                closeModal();
            }
        }
    }
    
    // Función para abrir el modal con la imagen
    window.openImageModal = function(imageUrl) {
        // Recopilar imágenes nuevamente por si han cambiado
        collectGalleryImages();
        
        const modal = document.getElementById('image-modal');
        const modalImg = document.getElementById('modal-image');
        
        // Precargar la imagen para obtener sus dimensiones reales
        const img = new Image();
        img.onload = function() {
            // Iniciar con un zoom adecuado según las dimensiones de la imagen
            const viewportWidth = window.innerWidth * 0.95;
            const viewportHeight = window.innerHeight * 0.9;
            
            // Establecer un zoom inicial óptimo (reducido en 30%)
            currentZoom = 1.05;
            currentRotation = 0;
            
            modalImg.src = imageUrl;
            modalImg.style.transform = `scale(${currentZoom}) rotate(0deg)`;
            
            modal.style.display = 'flex';
            document.body.style.overflow = 'hidden';
            
            // Actualizar el índice actual
            currentImageIndex = galleryImages.indexOf(imageUrl);
            if (currentImageIndex === -1) currentImageIndex = 0;
            
            // Actualizar contador
            imageCounter.textContent = `${currentImageIndex + 1} / ${galleryImages.length}`;
            
            // Mostrar/ocultar botones de navegación según cantidad de imágenes
            if (galleryImages.length <= 1) {
                prevButton.style.display = 'none';
                nextButton.style.display = 'none';
            } else {
                prevButton.style.display = 'block';
                nextButton.style.display = 'block';
            }
            
            // Añadir event listener para el teclado
            document.addEventListener('keydown', handleKeyDown);
        };
        img.src = imageUrl;
    };
    
    // Añadir eventos de clic a todas las imágenes de la galería
    document.querySelectorAll('.gallery-item').forEach(function(item) {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            const img = this.querySelector('img');
            if (img) {
                openImageModal(img.src);
            }
        });
    });
});
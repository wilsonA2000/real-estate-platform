// Script para el visor de imágenes mejorado
document.addEventListener('DOMContentLoaded', function() {
    // Crear el modal para las imágenes con funcionalidades avanzadas
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
    
    // Contenedor para la imagen y controles
    const viewerContainer = document.createElement('div');
    viewerContainer.style.position = 'relative';
    viewerContainer.style.width = '90%';
    viewerContainer.style.height = '90%';
    viewerContainer.style.display = 'flex';
    viewerContainer.style.flexDirection = 'column';
    viewerContainer.style.alignItems = 'center';
    
    // Imagen principal
    const modalImage = document.createElement('img');
    modalImage.id = 'modal-image';
    modalImage.style.maxWidth = '100%';
    modalImage.style.maxHeight = '85%';
    modalImage.style.objectFit = 'contain';
    modalImage.style.border = '2px solid white';
    modalImage.style.borderRadius = '4px';
    modalImage.style.transition = 'transform 0.3s ease';
    
    // Contador de imágenes
    const imageCounter = document.createElement('div');
    imageCounter.id = 'image-counter';
    imageCounter.style.position = 'absolute';
    imageCounter.style.top = '20px';
    imageCounter.style.left = '20px';
    imageCounter.style.backgroundColor = 'rgba(0,0,0,0.6)';
    imageCounter.style.color = 'white';
    imageCounter.style.padding = '5px 10px';
    imageCounter.style.borderRadius = '15px';
    imageCounter.style.fontSize = '14px';
    
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
    prevButton.style.width = '50px';
    prevButton.style.height = '50px';
    prevButton.style.fontSize = '20px';
    prevButton.style.cursor = 'pointer';
    prevButton.style.transition = 'background-color 0.3s';
    
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
    nextButton.style.width = '50px';
    nextButton.style.height = '50px';
    nextButton.style.fontSize = '20px';
    nextButton.style.cursor = 'pointer';
    nextButton.style.transition = 'background-color 0.3s';
    
    // Hover effects para botones de navegación
    prevButton.onmouseover = function() {
        this.style.backgroundColor = 'rgba(0,0,0,0.8)';
    };
    prevButton.onmouseout = function() {
        this.style.backgroundColor = 'rgba(0,0,0,0.5)';
    };
    nextButton.onmouseover = function() {
        this.style.backgroundColor = 'rgba(0,0,0,0.8)';
    };
    nextButton.onmouseout = function() {
        this.style.backgroundColor = 'rgba(0,0,0,0.5)';
    };
    
    // Barra de herramientas
    const toolbar = document.createElement('div');
    toolbar.style.display = 'flex';
    toolbar.style.justifyContent = 'center';
    toolbar.style.gap = '15px';
    toolbar.style.marginTop = '15px';
    
    // Botón de zoom in
    const zoomInBtn = document.createElement('button');
    zoomInBtn.innerHTML = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><line x1="11" y1="8" x2="11" y2="14"/><line x1="8" y1="11" x2="14" y2="11"/></svg>';
    zoomInBtn.style.backgroundColor = 'rgba(255,255,255,0.2)';
    zoomInBtn.style.border = 'none';
    zoomInBtn.style.borderRadius = '50%';
    zoomInBtn.style.width = '40px';
    zoomInBtn.style.height = '40px';
    zoomInBtn.style.display = 'flex';
    zoomInBtn.style.alignItems = 'center';
    zoomInBtn.style.justifyContent = 'center';
    zoomInBtn.style.cursor = 'pointer';
    zoomInBtn.style.color = 'white';
    zoomInBtn.style.transition = 'background-color 0.3s';
    
    // Botón de zoom out
    const zoomOutBtn = document.createElement('button');
    zoomOutBtn.innerHTML = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><line x1="8" y1="11" x2="14" y2="11"/></svg>';
    zoomOutBtn.style.backgroundColor = 'rgba(255,255,255,0.2)';
    zoomOutBtn.style.border = 'none';
    zoomOutBtn.style.borderRadius = '50%';
    zoomOutBtn.style.width = '40px';
    zoomOutBtn.style.height = '40px';
    zoomOutBtn.style.display = 'flex';
    zoomOutBtn.style.alignItems = 'center';
    zoomOutBtn.style.justifyContent = 'center';
    zoomOutBtn.style.cursor = 'pointer';
    zoomOutBtn.style.color = 'white';
    zoomOutBtn.style.transition = 'background-color 0.3s';
    
    // Botón de rotación
    const rotateBtn = document.createElement('button');
    rotateBtn.innerHTML = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M23 4v6h-6"/><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/></svg>';
    rotateBtn.style.backgroundColor = 'rgba(255,255,255,0.2)';
    rotateBtn.style.border = 'none';
    rotateBtn.style.borderRadius = '50%';
    rotateBtn.style.width = '40px';
    rotateBtn.style.height = '40px';
    rotateBtn.style.display = 'flex';
    rotateBtn.style.alignItems = 'center';
    rotateBtn.style.justifyContent = 'center';
    rotateBtn.style.cursor = 'pointer';
    rotateBtn.style.color = 'white';
    rotateBtn.style.transition = 'background-color 0.3s';
    
    // Botón de descarga
    const downloadBtn = document.createElement('button');
    downloadBtn.innerHTML = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>';
    downloadBtn.style.backgroundColor = 'rgba(255,255,255,0.2)';
    downloadBtn.style.border = 'none';
    downloadBtn.style.borderRadius = '50%';
    downloadBtn.style.width = '40px';
    downloadBtn.style.height = '40px';
    downloadBtn.style.display = 'flex';
    downloadBtn.style.alignItems = 'center';
    downloadBtn.style.justifyContent = 'center';
    downloadBtn.style.cursor = 'pointer';
    downloadBtn.style.color = 'white';
    downloadBtn.style.transition = 'background-color 0.3s';
    
    // Botón de pantalla completa
    const fullscreenBtn = document.createElement('button');
    fullscreenBtn.innerHTML = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"/></svg>';
    fullscreenBtn.style.backgroundColor = 'rgba(255,255,255,0.2)';
    fullscreenBtn.style.border = 'none';
    fullscreenBtn.style.borderRadius = '50%';
    fullscreenBtn.style.width = '40px';
    fullscreenBtn.style.height = '40px';
    fullscreenBtn.style.display = 'flex';
    fullscreenBtn.style.alignItems = 'center';
    fullscreenBtn.style.justifyContent = 'center';
    fullscreenBtn.style.cursor = 'pointer';
    fullscreenBtn.style.color = 'white';
    fullscreenBtn.style.transition = 'background-color 0.3s';
    
    // Hover effects para botones de la barra
    [zoomInBtn, zoomOutBtn, rotateBtn, downloadBtn, fullscreenBtn].forEach(btn => {
        btn.onmouseover = function() {
            this.style.backgroundColor = 'rgba(255,255,255,0.4)';
        };
        btn.onmouseout = function() {
            this.style.backgroundColor = 'rgba(255,255,255,0.2)';
        };
    });
    
    // Botón de cerrar
    const closeButton = document.createElement('button');
    closeButton.innerHTML = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>';
    closeButton.style.position = 'absolute';
    closeButton.style.top = '20px';
    closeButton.style.right = '20px';
    closeButton.style.backgroundColor = 'rgba(255,255,255,0.2)';
    closeButton.style.border = 'none';
    closeButton.style.borderRadius = '50%';
    closeButton.style.width = '40px';
    closeButton.style.height = '40px';
    closeButton.style.display = 'flex';
    closeButton.style.alignItems = 'center';
    closeButton.style.justifyContent = 'center';
    closeButton.style.cursor = 'pointer';
    closeButton.style.color = 'white';
    closeButton.style.transition = 'background-color 0.3s';
    
    closeButton.onmouseover = function() {
        this.style.backgroundColor = 'rgba(255,0,0,0.6)';
    };
    closeButton.onmouseout = function() {
        this.style.backgroundColor = 'rgba(255,255,255,0.2)';
    };
    
    // Añadir botones a la barra de herramientas
    toolbar.appendChild(zoomInBtn);
    toolbar.appendChild(zoomOutBtn);
    toolbar.appendChild(rotateBtn);
    toolbar.appendChild(downloadBtn);
    toolbar.appendChild(fullscreenBtn);
    
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
            // Si el elemento es un enlace, obtener el href
            if (item.tagName === 'A') {
                return item.getAttribute('href');
            }
            // Si es un div con una imagen, obtener el src de la imagen
            const img = item.querySelector('img');
            return img ? img.getAttribute('src') : null;
        }).filter(Boolean); // Eliminar valores nulos
    }
    
    // Llamar a la función para recopilar imágenes
    collectGalleryImages();
    
    // Funcionalidad de zoom in
    zoomInBtn.onclick = function(e) {
        e.stopPropagation();
        currentZoom += 0.25;
        if (currentZoom > 3) currentZoom = 3;
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
    
    // Funcionalidad de descarga
    downloadBtn.onclick = function(e) {
        e.stopPropagation();
        if (modalImage.src) {
            const link = document.createElement('a');
            link.href = modalImage.src;
            link.download = 'imagen-propiedad-' + (currentImageIndex + 1) + '.jpg';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    };
    
    // Funcionalidad de pantalla completa
    fullscreenBtn.onclick = function(e) {
        e.stopPropagation();
        if (!document.fullscreenElement) {
            modalContainer.requestFullscreen().catch(err => {
                console.error(`Error al intentar pantalla completa: ${err.message}`);
            });
        } else {
            document.exitFullscreen();
        }
    };
    
    // Navegación entre imágenes
    prevButton.onclick = function(e) {
        e.stopPropagation();
        if (galleryImages.length <= 1) return;
        
        currentImageIndex = (currentImageIndex - 1 + galleryImages.length) % galleryImages.length;
        modalImage.src = galleryImages[currentImageIndex];
        imageCounter.textContent = `${currentImageIndex + 1} / ${galleryImages.length}`;
        
        // Resetear zoom y rotación
        currentZoom = 1;
        currentRotation = 0;
        modalImage.style.transform = 'scale(1) rotate(0deg)';
    };
    
    nextButton.onclick = function(e) {
        e.stopPropagation();
        if (galleryImages.length <= 1) return;
        
        currentImageIndex = (currentImageIndex + 1) % galleryImages.length;
        modalImage.src = galleryImages[currentImageIndex];
        imageCounter.textContent = `${currentImageIndex + 1} / ${galleryImages.length}`;
        
        // Resetear zoom y rotación
        currentZoom = 1;
        currentRotation = 0;
        modalImage.style.transform = 'scale(1) rotate(0deg)';
    };
    
    // Navegación con teclado
    document.addEventListener('keydown', function(e) {
        if (modalContainer.style.display !== 'flex') return;
        
        if (e.key === 'ArrowLeft') {
            prevButton.click();
        } else if (e.key === 'ArrowRight') {
            nextButton.click();
        } else if (e.key === 'Escape') {
            closeButton.click();
        } else if (e.key === '+') {
            zoomInBtn.click();
        } else if (e.key === '-') {
            zoomOutBtn.click();
        } else if (e.key === 'r') {
            rotateBtn.click();
        } else if (e.key === 'f') {
            fullscreenBtn.click();
        }
    });
    
    // Cerrar el modal
    closeButton.onclick = function(e) {
        e.stopPropagation();
        modalContainer.style.display = 'none';
        document.body.style.overflow = 'auto';
        // Resetear zoom y rotación
        currentZoom = 1;
        currentRotation = 0;
        modalImage.style.transform = 'scale(1) rotate(0deg)';
    };
    
    // Cerrar al hacer clic fuera de la imagen
    modalContainer.onclick = function(event) {
        if (event.target === modalContainer) {
            modalContainer.style.display = 'none';
            document.body.style.overflow = 'auto';
            // Resetear zoom y rotación
            currentZoom = 1;
            currentRotation = 0;
            modalImage.style.transform = 'scale(1) rotate(0deg)';
        }
    };
    
    // Función para abrir el modal con la imagen
    window.openImageModal = function(imageUrl) {
        // Recopilar imágenes nuevamente por si han cambiado
        collectGalleryImages();
        
        const modal = document.getElementById('image-modal');
        const modalImg = document.getElementById('modal-image');
        modalImg.src = imageUrl;
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
        
        // Resetear zoom y rotación
        currentZoom = 1;
        currentRotation = 0;
        modalImg.style.transform = 'scale(1) rotate(0deg)';
        
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
    };
    
    // Añadir eventos de clic a todas las imágenes de la galería
    document.querySelectorAll('.gallery-item').forEach(function(item) {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            let imageUrl;
            
            // Si el elemento es un enlace, obtener el href
            if (this.tagName === 'A') {
                imageUrl = this.getAttribute('href');
            } else {
                // Si es un div con una imagen, obtener el src de la imagen
                const img = this.querySelector('img');
                imageUrl = img ? img.getAttribute('src') : null;
            }
            
            if (imageUrl) {
                openImageModal(imageUrl);
            }
        });
    });
});
// Script para inicializar Fancybox de manera simple y directa
document.addEventListener('DOMContentLoaded', function() {
    // Seleccionar todas las imágenes de la galería
    const galleryItems = document.querySelectorAll('.gallery-item');
    
    // Añadir evento de clic a cada imagen
    galleryItems.forEach(function(item) {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            const imageUrl = this.getAttribute('href');
            
            // Abrir la imagen en una ventana modal simple
            const modal = document.createElement('div');
            modal.style.position = 'fixed';
            modal.style.top = '0';
            modal.style.left = '0';
            modal.style.width = '100%';
            modal.style.height = '100%';
            modal.style.backgroundColor = 'rgba(0,0,0,0.9)';
            modal.style.display = 'flex';
            modal.style.alignItems = 'center';
            modal.style.justifyContent = 'center';
            modal.style.zIndex = '9999';
            
            // Crear la imagen dentro del modal
            const img = document.createElement('img');
            img.src = imageUrl;
            img.style.maxWidth = '90%';
            img.style.maxHeight = '90%';
            img.style.objectFit = 'contain';
            img.style.border = '2px solid white';
            img.style.borderRadius = '4px';
            
            // Añadir botón de cierre
            const closeBtn = document.createElement('button');
            closeBtn.innerHTML = '×';
            closeBtn.style.position = 'absolute';
            closeBtn.style.top = '20px';
            closeBtn.style.right = '20px';
            closeBtn.style.fontSize = '30px';
            closeBtn.style.color = 'white';
            closeBtn.style.background = 'none';
            closeBtn.style.border = 'none';
            closeBtn.style.cursor = 'pointer';
            
            // Cerrar el modal al hacer clic en el botón o fuera de la imagen
            closeBtn.addEventListener('click', function() {
                document.body.removeChild(modal);
            });
            
            modal.addEventListener('click', function(e) {
                if (e.target === modal) {
                    document.body.removeChild(modal);
                }
            });
            
            // Añadir elementos al DOM
            modal.appendChild(img);
            modal.appendChild(closeBtn);
            document.body.appendChild(modal);
        });
    });
});
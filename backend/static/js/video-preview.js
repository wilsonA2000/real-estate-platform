// Script para previsualizar videos en el formulario de propiedades
document.addEventListener('DOMContentLoaded', function() {
    // Referencias a elementos
    const videoUrlInput = document.getElementById('id_video_content');
    const videoFileInput = document.getElementById('video-file-upload');
    const videoPreview = document.getElementById('video-preview');
    const selectedFileName = document.getElementById('selected-file-name');
    const videoField = document.getElementById('id_video');
    const videoUrlField = document.getElementById('id_video_url');
    const previewUrlBtn = document.getElementById('preview-url-btn');
    let lastLocalUrl = null;
    
    // Función para previsualizar video desde URL
    function previewVideoFromUrl(url) {
        if (!url || url.trim() === '') {
            videoPreview.innerHTML = '<div class="flex items-center justify-center h-full text-gray-500">Ingresa una URL de YouTube o Vimeo para previsualizar</div>';
            return;
        }
        
        // Limpiar previsualización anterior
        videoPreview.innerHTML = '<div class="flex items-center justify-center h-full"><div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div></div>';
        
        // Detectar tipo de URL
        let ytMatch = url.match(/(?:youtube\.com\/(?:watch\?v=|embed\/)|youtu\.be\/)([a-zA-Z0-9_-]{11})/);
        let vimeoMatch = url.match(/vimeo\.com\/(\d+)/);
        
        if (ytMatch) {
            // YouTube embed
            const ytId = ytMatch[1];
            videoPreview.innerHTML = `<div class="video-container" style="width:100%;height:100%"><div id="yt-preview" data-plyr-provider="youtube" data-plyr-embed-id="${ytId}" style="width:100%;height:100%"></div></div>`;
            setTimeout(function() { 
                new Plyr('#yt-preview', {
                    hideControls: false, 
                    theme: 'dark',
                    controls: ['play-large', 'play', 'progress', 'current-time', 'mute', 'volume', 'fullscreen']
                }); 
            }, 200);
            
            // Actualizar campo oculto
            if (videoUrlField) videoUrlField.value = url;
            if (videoField) videoField.value = '';
        } else if (vimeoMatch) {
            // Vimeo embed
            const vimeoId = vimeoMatch[1];
            videoPreview.innerHTML = `<div class="video-container" style="width:100%;height:100%"><div id="vimeo-preview" data-plyr-provider="vimeo" data-plyr-embed-id="${vimeoId}" style="width:100%;height:100%"></div></div>`;
            setTimeout(function() { 
                new Plyr('#vimeo-preview', {
                    hideControls: false, 
                    theme: 'dark',
                    controls: ['play-large', 'play', 'progress', 'current-time', 'mute', 'volume', 'fullscreen']
                }); 
            }, 200);
            
            // Actualizar campo oculto
            if (videoUrlField) videoUrlField.value = url;
            if (videoField) videoField.value = '';
        } else {
            videoPreview.innerHTML = `<div class="bg-yellow-100 text-yellow-800 rounded p-3 flex items-center justify-center h-full">
                <div>
                    <p class="font-bold">URL no válida</p>
                    <p>Por favor, ingresa una URL de YouTube (ej: https://youtube.com/watch?v=XXXX) o Vimeo (ej: https://vimeo.com/XXXX)</p>
                </div>
            </div>`;
        }
    }
    
    // Función para previsualizar video desde archivo
    function previewVideoFromFile(file) {
        if (!file) {
            return;
        }
        
        // Limpiar previsualización anterior
        videoPreview.innerHTML = '<div class="flex items-center justify-center h-full"><div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div></div>';
        
        if (lastLocalUrl) {
            URL.revokeObjectURL(lastLocalUrl);
            lastLocalUrl = null;
        }
        
        // Verificar que sea un archivo de video
        if (file.type.startsWith('video/')) {
            const url = URL.createObjectURL(file);
            lastLocalUrl = url;
            videoPreview.innerHTML = `<video id="local-video-preview" controls style="width:100%;height:100%;border-radius:18px;"><source src="${url}" type="${file.type}">Tu navegador no soporta la reproducción de video.</video>`;
            setTimeout(function() { 
                new Plyr('#local-video-preview', {
                    hideControls: false, 
                    theme: 'dark',
                    controls: ['play-large', 'play', 'progress', 'current-time', 'mute', 'volume', 'fullscreen']
                }); 
            }, 200);
            
            // Actualizar campos ocultos
            if (videoField) {
                const dataTransfer = new DataTransfer();
                dataTransfer.items.add(file);
                videoField.files = dataTransfer.files;
            }
            if (videoUrlField) videoUrlField.value = '';
            
            // Mostrar nombre del archivo
            if (selectedFileName) selectedFileName.textContent = file.name;
            
            // Limpiar campo de URL si existe
            if (videoUrlInput) videoUrlInput.value = '';
        } else {
            videoPreview.innerHTML = `<div class="bg-red-100 text-red-800 rounded p-3 flex items-center justify-center h-full">
                <div>
                    <p class="font-bold">Formato no soportado</p>
                    <p>Por favor, sube un archivo de video en formato MP4, MOV o AVI.</p>
                </div>
            </div>`;
            if (selectedFileName) selectedFileName.textContent = '';
        }
    }
    
    // Event listeners
    if (previewUrlBtn) {
        previewUrlBtn.addEventListener('click', function() {
            if (videoUrlInput) {
                previewVideoFromUrl(videoUrlInput.value);
            }
        });
    }
    
    if (videoFileInput) {
        videoFileInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                previewVideoFromFile(this.files[0]);
            }
        });
    }
    
    // Mensaje inicial
    if (videoPreview && videoPreview.innerHTML === '') {
        videoPreview.innerHTML = '<div class="flex items-center justify-center h-full text-gray-500">Ingresa una URL o sube un archivo para previsualizar el video</div>';
    }
});
// Función para manejar la navegación sin recargar la página
document.addEventListener('DOMContentLoaded', function() {
    // Asegurarse de que todos los recursos estén cargados
    window.addEventListener('load', function() {
        // Inicializar GSAP si está disponible
        if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {
            gsap.registerPlugin(ScrollTrigger);
            initAnimations();
        }
    });
});

// Función para inicializar animaciones
function initAnimations() {
    gsap.from(".content", { 
        opacity: 0, 
        y: 50, 
        duration: 1, 
        scrollTrigger: ".content" 
    });
}

// Función para forzar la recarga de scripts después de la navegación
function reloadScripts() {
    // Recargar FancyBox si está presente
    if (typeof Fancybox !== 'undefined') {
        Fancybox.bind("[data-fancybox]", {
            Toolbar: {
                display: {
                    left: ["infobar"],
                    middle: ["zoomIn", "zoomOut", "toggle1to1", "rotateCCW", "rotateCW"],
                    right: ["slideshow", "fullscreen", "thumbs", "close"],
                },
            },
            closeButton: true,
            click: "close",
            dragToClose: true,
            Navigation: {
                prevTpl: '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg>',
                nextTpl: '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>',
            },
            mainClass: "fancybox-custom",
        });
    }
    
    // Reinicializar animaciones
    if (typeof gsap !== 'undefined') {
        initAnimations();
    }
}
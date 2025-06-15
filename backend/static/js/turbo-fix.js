// Este script soluciona el problema de carga de páginas sin necesidad de actualizar
document.addEventListener('DOMContentLoaded', function() {
    // Referencias a los elementos de carga
    const loadingBar = document.getElementById('loading-bar');
    const loadingSpinner = document.getElementById('loading-spinner');
    const overlay = document.getElementById('page-transition-overlay');
    
    // Capturar todos los enlaces internos
    document.body.addEventListener('click', function(event) {
        // Verificar si el clic fue en un enlace
        let target = event.target;
        while (target && target.tagName !== 'A') {
            target = target.parentNode;
            if (!target || target === document.body) break;
        }
        
        // Si es un enlace interno, manejar la navegación
        if (target && target.tagName === 'A' && 
            target.href && 
            target.href.startsWith(window.location.origin) && 
            !target.getAttribute('download') && 
            !target.getAttribute('target')) {
            
            event.preventDefault();
            
            // Mostrar indicadores de carga
            loadingBar.style.width = '0%';
            loadingSpinner.classList.add('active');
            overlay.classList.add('active');
            
            // Animar la barra de progreso
            setTimeout(() => { loadingBar.style.width = '30%'; }, 100);
            setTimeout(() => { loadingBar.style.width = '60%'; }, 300);
            
            // Cargar la nueva página
            fetch(target.href)
                .then(response => response.text())
                .then(html => {
                    // Completar la barra de progreso
                    loadingBar.style.width = '100%';
                    
                    // Parsear el HTML
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, 'text/html');
                    
                    // Actualizar el título
                    document.title = doc.title;
                    
                    // Actualizar el contenido principal
                    const newContent = doc.querySelector('.content');
                    if (newContent) {
                        document.querySelector('.content').innerHTML = newContent.innerHTML;
                    }
                    
                    // Actualizar la URL
                    history.pushState({}, doc.title, target.href);
                    
                    // Ejecutar scripts en el nuevo contenido
                    const scripts = Array.from(doc.querySelectorAll('.content script'));
                    scripts.forEach(script => {
                        const newScript = document.createElement('script');
                        Array.from(script.attributes).forEach(attr => {
                            newScript.setAttribute(attr.name, attr.value);
                        });
                        newScript.textContent = script.textContent;
                        document.querySelector('.content').appendChild(newScript);
                    });
                    
                    // Recargar scripts globales
                    if (typeof reloadScripts === 'function') {
                        reloadScripts();
                    }
                    
                    // Ocultar indicadores de carga
                    setTimeout(() => {
                        loadingBar.style.width = '0%';
                        loadingSpinner.classList.remove('active');
                        overlay.classList.remove('active');
                    }, 300);
                    
                    // Desplazarse al inicio de la página
                    window.scrollTo(0, 0);
                    
                    // Reinicializar FancyBox si está presente
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
                    
                    // Reinicializar GSAP si está presente
                    if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {
                        gsap.registerPlugin(ScrollTrigger);
                        gsap.from(".content", { 
                            opacity: 0, 
                            y: 50, 
                            duration: 1, 
                            scrollTrigger: ".content" 
                        });
                    }
                })
                .catch(error => {
                    console.error('Error al cargar la página:', error);
                    // En caso de error, redirigir normalmente
                    window.location.href = target.href;
                });
        }
    });
    
    // Manejar la navegación con los botones de atrás y adelante del navegador
    window.addEventListener('popstate', function() {
        // Mostrar indicadores de carga
        loadingBar.style.width = '0%';
        loadingSpinner.classList.add('active');
        overlay.classList.add('active');
        
        // Cargar la página actual
        fetch(window.location.href)
            .then(response => response.text())
            .then(html => {
                // Completar la barra de progreso
                loadingBar.style.width = '100%';
                
                // Parsear el HTML
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                
                // Actualizar el título
                document.title = doc.title;
                
                // Actualizar el contenido principal
                const newContent = doc.querySelector('.content');
                if (newContent) {
                    document.querySelector('.content').innerHTML = newContent.innerHTML;
                }
                
                // Ocultar indicadores de carga
                setTimeout(() => {
                    loadingBar.style.width = '0%';
                    loadingSpinner.classList.remove('active');
                    overlay.classList.remove('active');
                }, 300);
                
                // Reinicializar scripts
                if (typeof reloadScripts === 'function') {
                    reloadScripts();
                }
                
                // Reinicializar FancyBox y GSAP
                if (typeof Fancybox !== 'undefined') {
                    Fancybox.bind("[data-fancybox]");
                }
                
                if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {
                    gsap.registerPlugin(ScrollTrigger);
                    gsap.from(".content", { opacity: 0, y: 50, duration: 1, scrollTrigger: ".content" });
                }
            })
            .catch(error => {
                console.error('Error al cargar la página:', error);
                window.location.reload();
            });
    });
});
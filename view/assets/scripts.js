// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Get references to DOM elements
    const getStartedBtn = document.getElementById('getStartedBtn');
    const planeContainer = document.getElementById('planeContainer');
    const plane = document.getElementById('plane');
    
    // Add click event listener to the Get Started button
    getStartedBtn.addEventListener('click', function() {
        // Trigger plane animation
        animatePlane();
        
        // Add a subtle button effect
        this.style.transform = 'scale(0.95)';
        setTimeout(() => {
            this.style.transform = 'scale(1)';
        }, 150);
    });
    
    // Function to animate the plane
    function animatePlane() {
        // Show the plane container
        planeContainer.style.opacity = '1';
        
        // Add flying class to trigger CSS animation
        plane.classList.add('flying');
        
        // Reset animation after completion
        setTimeout(() => {
            plane.classList.remove('flying');
            planeContainer.style.opacity = '0';
        }, 4000); // Match the CSS animation duration
    }
    
    // Add some interactive effects to monuments
    const monuments = document.querySelectorAll('.monument');
    
    monuments.forEach(monument => {
        // Add subtle hover animations
        monument.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.1) rotate(2deg)';
        });
        
        monument.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1) rotate(0deg)';
        });
        
        // Add click effect for monuments
        monument.addEventListener('click', function() {
            // Create a ripple effect
            const ripple = document.createElement('div');
            ripple.style.position = 'absolute';
            ripple.style.width = '20px';
            ripple.style.height = '20px';
            ripple.style.background = 'rgba(139, 92, 246, 0.6)';
            ripple.style.borderRadius = '50%';
            ripple.style.pointerEvents = 'none';
            ripple.style.animation = 'ripple 0.6s linear';
            
            // Position ripple at click point
            const rect = this.getBoundingClientRect();
            ripple.style.left = '50%';
            ripple.style.top = '50%';
            ripple.style.transform = 'translate(-50%, -50%)';
            
            this.appendChild(ripple);
            
            // Remove ripple after animation
            setTimeout(() => {
                if (ripple.parentNode) {
                    ripple.parentNode.removeChild(ripple);
                }
            }, 600);
        });
    });
    
    // Add CSS for ripple effect
    const style = document.createElement('style');
    style.textContent = `
        @keyframes ripple {
            0% {
                transform: translate(-50%, -50%) scale(0);
                opacity: 1;
            }
            100% {
                transform: translate(-50%, -50%) scale(4);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
    
    // Add parallax effect to particles on mouse move
    document.addEventListener('mousemove', function(e) {
        const particles = document.querySelectorAll('.particle');
        const mouseX = e.clientX / window.innerWidth;
        const mouseY = e.clientY / window.innerHeight;
        
        particles.forEach((particle, index) => {
            const speed = (index + 1) * 0.5;
            const x = (mouseX - 0.5) * speed;
            const y = (mouseY - 0.5) * speed;
            
            particle.style.transform = `translate(${x}px, ${y}px)`;
        });
    });
    
    // Add smooth scroll effect for better UX
    getStartedBtn.addEventListener('click', function() {
        // Smooth scroll to a section if needed
        const globeSection = document.querySelector('.globe-section');
        if (globeSection) {
            globeSection.scrollIntoView({
                behavior: 'smooth',
                block: 'center'
            });
        }
    });
    
    // Add loading animation for better performance
    window.addEventListener('load', function() {
        // Add fade-in effect to all elements
        const elements = document.querySelectorAll('.header, .globe-section, .monuments-container');
        elements.forEach((element, index) => {
            element.style.opacity = '0';
            element.style.transform = 'translateY(20px)';
            element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            
            setTimeout(() => {
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }, index * 200);
        });
    });
    
    // Add keyboard navigation support
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' || e.key === ' ') {
            // Trigger plane animation on Enter or Space
            animatePlane();
        }
    });
    
    // Add touch support for mobile devices
    let touchStartY = 0;
    let touchEndY = 0;
    
    document.addEventListener('touchstart', function(e) {
        touchStartY = e.changedTouches[0].screenY;
    });
    
    document.addEventListener('touchend', function(e) {
        touchEndY = e.changedTouches[0].screenY;
        handleSwipe();
    });
    
    function handleSwipe() {
        const swipeThreshold = 50;
        const diff = touchStartY - touchEndY;
        
        if (Math.abs(diff) > swipeThreshold) {
            if (diff > 0) {
                // Swipe up - could trigger plane animation
                animatePlane();
            }
        }
    }
});

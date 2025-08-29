// AI-Advanced Interface System
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Neural Network Canvas
    initNeuralNetwork();
    
    // Get references to DOM elements
    const getStartedBtn = document.getElementById('getStartedBtn');
    const planeContainer = document.getElementById('planeContainer');
    const plane = document.getElementById('plane');
    const controlIndicators = document.querySelectorAll('.control-indicator');
    const monumentCards = document.querySelectorAll('.monument-card');
    
    // Neural Network Animation
    function initNeuralNetwork() {
        const canvas = document.getElementById('neuralCanvas');
        const ctx = canvas.getContext('2d');
        
        // Set canvas size
        function resizeCanvas() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }
        
        resizeCanvas();
        window.addEventListener('resize', resizeCanvas);
        
        // Neural network nodes and connections
        const nodes = [];
        const connections = [];
        const nodeCount = 15;
        const connectionCount = 25;
        
        // Create nodes
        for (let i = 0; i < nodeCount; i++) {
            nodes.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                vx: (Math.random() - 0.5) * 0.5,
                vy: (Math.random() - 0.5) * 0.5,
                size: Math.random() * 3 + 1,
                pulse: Math.random() * Math.PI * 2
            });
        }
        
        // Create connections
        for (let i = 0; i < connectionCount; i++) {
            connections.push({
                from: Math.floor(Math.random() * nodeCount),
                to: Math.floor(Math.random() * nodeCount),
                strength: Math.random() * 0.5 + 0.1
            });
        }
        
        // Animation loop
        function animate() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            // Update nodes
            nodes.forEach(node => {
                node.x += node.vx;
                node.y += node.vy;
                node.pulse += 0.05;
                
                // Bounce off edges
                if (node.x < 0 || node.x > canvas.width) node.vx *= -1;
                if (node.y < 0 || node.y > canvas.height) node.vy *= -1;
                
                // Draw nodes
                const alpha = 0.3 + 0.4 * Math.sin(node.pulse);
                ctx.beginPath();
                ctx.arc(node.x, node.y, node.size, 0, Math.PI * 2);
                ctx.fillStyle = `rgba(0, 255, 255, ${alpha})`;
                ctx.fill();
                
                // Node glow
                ctx.beginPath();
                ctx.arc(node.x, node.y, node.size * 2, 0, Math.PI * 2);
                ctx.strokeStyle = `rgba(0, 255, 255, ${alpha * 0.3})`;
                ctx.lineWidth = 1;
                ctx.stroke();
            });
            
            // Draw connections
            connections.forEach(conn => {
                const from = nodes[conn.from];
                const to = nodes[conn.to];
                const distance = Math.sqrt((from.x - to.x) ** 2 + (from.y - to.y) ** 2);
                
                if (distance < 200) {
                    const alpha = (1 - distance / 200) * conn.strength;
                    ctx.beginPath();
                    ctx.moveTo(from.x, from.y);
                    ctx.lineTo(to.x, to.y);
                    ctx.strokeStyle = `rgba(0, 255, 255, ${alpha})`;
                    ctx.lineWidth = 1;
                    ctx.stroke();
                }
            });
            
            requestAnimationFrame(animate);
        }
        
        animate();
    }
    
    // AI Activate Button with enhanced effects
    getStartedBtn.addEventListener('click', function() {
        // Trigger AI activation sequence
        activateAI();
        
        // Button press effect
        this.style.transform = 'scale(0.95)';
        setTimeout(() => {
            this.style.transform = 'scale(1)';
        }, 150);
    });
    
    // AI Activation Sequence
    function activateAI() {
        // Activate control indicators
        controlIndicators.forEach((indicator, index) => {
            setTimeout(() => {
                indicator.classList.add('active');
            }, index * 500);
        });
        
        // Trigger flight animation
        setTimeout(() => {
            animateAICraft();
        }, 1500);
        
        // Update status values
        updateStatusValues();
        
        // Redirect to PlanningPage after all animations complete
        setTimeout(() => {
            window.location.href = '/planning';
        }, 6000); // Total time for all animations: 1.5s + 4s flight + 0.5s buffer
    }
    
    // Enhanced AI Craft Animation
    function animateAICraft() {
        planeContainer.style.opacity = '1';
        plane.classList.add('flying');
        
        // Add trajectory effects
        const trajectory = document.querySelector('.trajectory-line');
        trajectory.style.animation = 'trajectoryGlow 2s ease-in-out infinite';
        
        setTimeout(() => {
            plane.classList.remove('flying');
            planeContainer.style.opacity = '0';
            trajectory.style.animation = '';
        }, 4000);
    }
    
    // Update Status Values
    function updateStatusValues() {
        const statusValues = document.querySelectorAll('.status-value');
        const values = ['ONLINE', 'ACTIVE', 'SYNCED'];
        
        statusValues.forEach((value, index) => {
            setTimeout(() => {
                value.textContent = values[index];
                value.style.animation = 'statusBlink 3s ease-in-out infinite';
            }, index * 800);
        });
    }
    
    // Enhanced Monument Card Interactions
    monumentCards.forEach(card => {
        // Hover effects
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px) scale(1.05)';
            
            // Add scanning effect
            const scanLine = document.createElement('div');
            scanLine.style.position = 'absolute';
            scanLine.style.top = '0';
            scanLine.style.left = '0';
            scanLine.style.width = '100%';
            scanLine.style.height = '2px';
            scanLine.style.background = 'linear-gradient(90deg, transparent, #00ffff, transparent)';
            scanLine.style.animation = 'scanLine 1s ease-in-out';
            scanLine.style.zIndex = '10';
            
            this.appendChild(scanLine);
            
            setTimeout(() => {
                if (scanLine.parentNode) {
                    scanLine.parentNode.removeChild(scanLine);
                }
            }, 1000);
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
        
        // Click effects with data visualization
        card.addEventListener('click', function() {
            const location = this.dataset.location;
            
            // Create data popup
            const popup = document.createElement('div');
            popup.style.position = 'fixed';
            popup.style.top = '50%';
            popup.style.left = '50%';
            popup.style.transform = 'translate(-50%, -50%)';
            popup.style.background = 'rgba(0, 0, 0, 0.9)';
            popup.style.border = '1px solid #00ffff';
            popup.style.borderRadius = '15px';
            popup.style.padding = '30px';
            popup.style.color = '#00ffff';
            popup.style.fontFamily = 'Orbitron, monospace';
            popup.style.zIndex = '1000';
            popup.style.backdropFilter = 'blur(10px)';
            popup.style.animation = 'fadeIn 0.3s ease-in-out';
            
            popup.innerHTML = `
                <h3 style="margin-bottom: 15px; color: #00ffff;">${location.replace('-', ' ').toUpperCase()}</h3>
                <div style="margin-bottom: 10px;">
                    <span style="color: #80ffff;">AI Analysis:</span>
                    <span style="color: #00ffff;">Processing...</span>
                </div>
                <div style="margin-bottom: 10px;">
                    <span style="color: #80ffff;">Optimal Route:</span>
                    <span style="color: #00ffff;">Calculating...</span>
                </div>
                <div style="margin-bottom: 20px;">
                    <span style="color: #80ffff;">Travel Time:</span>
                    <span style="color: #00ffff;">Estimating...</span>
                </div>
                <button onclick="this.parentElement.remove()" style="
                    background: linear-gradient(45deg, #00ffff, #0080ff);
                    color: #000;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 25px;
                    cursor: pointer;
                    font-family: 'Orbitron', monospace;
                    font-weight: 600;
                ">CLOSE</button>
            `;
            
            document.body.appendChild(popup);
            
            // Simulate AI processing
            setTimeout(() => {
                const analysis = popup.querySelector('span:nth-child(2)');
                analysis.textContent = 'Complete';
                analysis.style.color = '#00ff00';
            }, 1000);
            
            setTimeout(() => {
                const route = popup.querySelector('span:nth-child(4)');
                route.textContent = 'Optimized';
                route.style.color = '#00ff00';
            }, 2000);
            
            setTimeout(() => {
                const time = popup.querySelector('span:nth-child(6)');
                time.textContent = '12h 34m';
                time.style.color = '#00ff00';
            }, 3000);
        });
    });
    
    // Add CSS for new animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fadeIn {
            from { opacity: 0; transform: translate(-50%, -50%) scale(0.8); }
            to { opacity: 1; transform: translate(-50%, -50%) scale(1); }
        }
        
        @keyframes scanLine {
            0% { top: 0; opacity: 0; }
            50% { opacity: 1; }
            100% { top: 100%; opacity: 0; }
        }
        
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
    
    // Parallax effect for particles
    document.addEventListener('mousemove', function(e) {
        const particleClusters = document.querySelectorAll('.particle-cluster');
        const mouseX = e.clientX / window.innerWidth;
        const mouseY = e.clientY / window.innerHeight;
        
        particleClusters.forEach((cluster, index) => {
            const speed = (index + 1) * 0.3;
            const x = (mouseX - 0.5) * speed;
            const y = (mouseY - 0.5) * speed;
            
            cluster.style.transform = `translate(${x}px, ${y}px)`;
        });
    });
    
    // Keyboard navigation
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            activateAI();
        }
    });
    
    // Touch support for mobile
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
                activateAI();
            }
        }
    }
    
    // Loading animation
    window.addEventListener('load', function() {
        const elements = document.querySelectorAll('.ai-header, .ai-globe-section, .ai-data-viz, .ai-monuments');
        elements.forEach((element, index) => {
            element.style.opacity = '0';
            element.style.transform = 'translateY(30px)';
            element.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
            
            setTimeout(() => {
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }, index * 200);
        });
    });
    
    // Real-time data updates
    setInterval(() => {
        const streamValues = document.querySelectorAll('.stream-value');
        const values = ['Neural Analysis', 'Route Calculation', 'Travel Patterns', 'Data Processing', 'AI Optimization'];
        
        streamValues.forEach((value, index) => {
            if (Math.random() > 0.7) {
                const randomValue = values[Math.floor(Math.random() * values.length)];
                value.textContent = randomValue;
                value.style.animation = 'streamUpdate 0.5s ease-in-out';
            }
        });
    }, 3000);
});

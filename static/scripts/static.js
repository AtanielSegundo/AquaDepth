function startProcessing() {
    hideOtherElements(); 
    rotateShip(); 
    simulateImageProcessing()
        .then(() => {
            stopRotateShip();
            showOtherElements(); 
        })
        .catch((error) => {
            console.error("Error during image processing:", error);
            stopRotateShip(); 
            showOtherElements(); 
        });
}


function hideOtherElements() {
    const allElements = document.body.children;
    for (let i = 0; i < allElements.length; i++) {
        const element = allElements[i];
        if (element.tagName !== 'SCRIPT' && !element.classList.contains('blue-rectangle')) {
            element.style.display = 'none';
        }
    }
}


function showOtherElements() {
    const allElements = document.body.children;
    for (let i = 0; i < allElements.length; i++) {
        const element = allElements[i];
        if (element.tagName !== 'SCRIPT' && !element.classList.contains('blue-rectangle')) {
            element.style.display = ''; 
        }
    }
}

function simulateImageProcessing() {
    return new Promise((resolve) => {
        setTimeout(() => {
            console.log("Image processing complete");
            resolve();
        }, 5000);
    });
}

let rotateShipInterval;
function rotateShip() {
    let dot_repeat = 1;
    const loadingMessage = document.createElement('p');
    loadingMessage.id = 'loading_message';
    loadingMessage.style.position = 'fixed';
    loadingMessage.textContent = 'Processando' + '.'.repeat(dot_repeat);
    loadingMessage.style.top = '70%';  
    loadingMessage.style.left = '50%';
    loadingMessage.style.fontSize = '30px';
    loadingMessage.style.transform = 'translateX(-50%)';
    document.body.appendChild(loadingMessage);
    
    const shipImage = document.createElement('img');
    shipImage.src = ship_image_path;
    shipImage.className = 'ship_image';
    document.body.appendChild(shipImage);
    
    let currentRotation = 0;    
    let rotationDirection = 0.4;
    let rotationLimit = 2;
    let dampingFactor = 0.985;
    let resetThreshold = 0.1;
    
    shipImage.style.position = "absolute"; 
    shipImage.style.top = '50%'; 
    shipImage.style.left = '50%'; 
    
    rotateShipInterval = setInterval(() => {
        if (currentRotation >= rotationLimit || currentRotation <= -rotationLimit) {
            rotationDirection *= -1;
        }
        
        currentRotation += rotationDirection;
        rotationDirection *= dampingFactor;
        
        if (Math.abs(rotationDirection) < resetThreshold) {
            rotationDirection = 0.4;
        }
        
        shipImage.style.transition = 'transform 0.3s ease';
        shipImage.style.transform = `rotate(${currentRotation}deg)`;
        
    }, 60);
    
    setInterval(() => {
        dot_repeat = (dot_repeat + 1) % 4;
        loadingMessage.textContent = 'Processando' + '.'.repeat(dot_repeat);
    }, 600);  
    
}

function stopRotateShip() {
    clearInterval(rotateShipInterval);
    const shipImage = document.querySelector('.ship_image');
    const loadingMessage = document.getElementById("loading_message");
    if (shipImage && shipImage.parentNode) {
        shipImage.parentNode.removeChild(shipImage);
    }

    if (loadingMessage && loadingMessage.parentNode) {
        loadingMessage.parentNode.removeChild(loadingMessage);
    }
}

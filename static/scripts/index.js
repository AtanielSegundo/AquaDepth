var ShipFrameChanged = false;

function change_frame() {
    var shipFrame = document.getElementById("ShipFrame");
    if (ShipFrameChanged) {
        shipFrame.innerHTML = "<p>Aqua Depth</p>";
        shipFrame.className = "data_ship_frame";
        ShipFrameChanged = false;
    } else {
        fetch(HomeUrl + "/log/json")
            .then(response => response.json())
            .then(data => {
                const listItems = Object.entries(data).map(([key, value]) => `
                    <div class = 'log_item'>${value}</div>`);
                shipFrame.innerHTML = listItems.join('');
                shipFrame.className = "log_frame";
                ShipFrameChanged = true;
            })
            .catch(error => {
                shipFrame.innerHTML = `
                    <div>
                        <pre>Error fetching ${HomeUrl} JSON,${error}</pre>
                    </div>`;
                shipFrame.className = "log_frame";
                ShipFrameChanged = true;
            });
    }
}

function rotateShip() {
    const shipImage = document.querySelector('.ship_image');
    let currentRotation = 0;
    let rotationDirection = 0.2; 
    let rotationLimit = 1.4;
    let dampingFactor = 0.98; 
    let resetThreshold = 0.1; 

    setInterval(() => {
        if (currentRotation >= rotationLimit || currentRotation <= -rotationLimit) {
            rotationDirection *= -1;
        }

        currentRotation += rotationDirection;
        rotationDirection *= dampingFactor;
        if (Math.abs(rotationDirection) < resetThreshold) {
            rotationDirection = 0.2;
        }

        shipImage.style.transition = 'transform 0.2s ease'; 
        shipImage.style.transform = `translateX(-50%) rotate(${currentRotation}deg)`;
    }, 60);
}

document.addEventListener('DOMContentLoaded', rotateShip);

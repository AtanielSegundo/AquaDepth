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
                // Create a list of <div> elements for each item in the JSON data
                const listItems = Object.entries(data).map(([key, value]) => `
                    <div class = 'log_item'>${value}</div>`);

                // Set the shipFrame content as a joined string of the list items
                shipFrame.innerHTML = listItems.join('');
                
                shipFrame.className = "log_frame";
                ShipFrameChanged = true;
            })
            .catch(error => {
                // Display an error message in case of a fetch error
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
    let dampingFactor = 0.98; // Adjust as needed
    let resetThreshold = 0.1; // Adjust as needed

    setInterval(() => {
        if (currentRotation >= rotationLimit || currentRotation <= -rotationLimit) {
            rotationDirection *= -1;
        }

        currentRotation += rotationDirection;

        // Apply damping
        rotationDirection *= dampingFactor;

        // Reset rotation direction if it becomes too small
        if (Math.abs(rotationDirection) < resetThreshold) {
            rotationDirection = 0.2;
        }

        shipImage.style.transition = 'transform 0.5s ease'; 
        shipImage.style.transform = `translateX(-50%) rotate(${currentRotation}deg)`;
    }, 60);
}

document.addEventListener('DOMContentLoaded', rotateShip);

let selectionButtons = ["imagens_btn", "apresentacao_btn", "video_btn"];
let selectionObjects = selectionButtons.map(string => document.getElementById(string));
const getSectionName = string => string.split("_")[0];
const getBtnName = string => string === "" ? "" : string+"_btn";
const MatchList = [["imagens","camera_hover.png","logo-imagens"],
                   ["apresentacao","presentation_white.png","logos"],
                   ["video","video_white.png","logos"]
                  ];


function handleImagensSection(show=true) {
    const dropzone = document.getElementsByClassName("dropzone-container")[0];
    if (show){
        dropzone.style.visibility = "visible";
    }
    else{
        dropzone.style.visibility = "hidden";
    }
}
function handleApresentacaoSection() {
    console.log("todo".toUpperCase())
}
function handleVideoSection() {
    console.log("todo".toUpperCase())
}

const methodsMap = {
    "imagens" : handleImagensSection, 
    "apresentacao" : handleApresentacaoSection,
    "video" : handleVideoSection
}

let sectionsObjects = selectionButtons.map(
    string => document.getElementsByClassName(getSectionName(string)));
var lastBtn = "";

function handleSectionLogos(clickedId){
    for (const tuple of MatchList) {
        const sectionName = getSectionName(clickedId);
        
        if ( sectionName === tuple[0]){
            const sectionObject = document.getElementsByClassName(tuple[0])[0];
            const innerImageId = tuple[0] + "_inner_image";
            const innerImageElement = document.getElementById(innerImageId);
            if (innerImageElement) {
                sectionObject.removeChild(innerImageElement);
            }
            methodsMap[sectionName]();
        }
        else{
            methodsMap[tuple[0]](false);
            const innerImageId = tuple[0] + "_inner_image";
            const sectionObject = document.getElementsByClassName(tuple[0])[0];
            const innerImageElement = document.getElementById(innerImageId);
            if (innerImageElement){
                sectionObject.removeChild(innerImageElement);
            }
            const img = document.createElement('img');
            img.id  = innerImageId; 
            img.src = `static/images/` + tuple[1];
            img.className = tuple[2];
            sectionObject.appendChild(img);
        }
    }
}
handleSectionLogos("");

function handleHoverInversion(sectionName) {
    for (const tuple of MatchList) {
        const innerImageId = tuple[0] + "_inner_image";
        const innerImageElement = document.getElementById(innerImageId);
        if (innerImageElement) {
            const isInversed = !(tuple[0] === sectionName);
            innerImageElement.style.filter = isInversed ? "invert(0.5)" : "none";
            innerImageElement.style.maxHeight = isInversed ? "25vh" : "30vh";
            innerImageElement.style.maxWidth = isInversed ? "25%" : "30%";
        }
    }

}

for (const section of sectionsObjects) {
    const sectionName = section[0].className;
    section[0].addEventListener('click', function (event) {
        const innerImage = document.getElementById(sectionName+"_inner_image");
        if (event.target === section[0] || event.target === innerImage) {
            handleButtonClick(getBtnName(sectionName));
        }
    });

    section[0].addEventListener('mouseenter', function () {
        handleHoverInversion(getSectionName(sectionName));
    });
    section[0].addEventListener('mouseleave', function () {
        handleHoverInversion(getSectionName(sectionName));
    });
}

function handleButtonClick(clickedId) {
    const sectionName = getSectionName(clickedId);
    handleSectionLogos(clickedId);    
    for (const button of selectionObjects) {
        button.style.textDecoration = "none";
        button.style.flex = 1;
    }

    for (const section of sectionsObjects) {
            section[0].style.flex = 1;
            section[0].style.backgroundColor = "rgba(0, 0, 0, 0.75)";
            
        }
        
    if (!(clickedId === lastBtn)){
        for (const i in selectionObjects) {
            const isClickedButton = selectionObjects[i].id === clickedId;
            selectionObjects[i].style.textDecoration = isClickedButton ? "underline" : "none";
            selectionObjects[i].style.flex = isClickedButton ? 4 : 1;
        }
        
        for (const i in sectionsObjects) {
            const isSection = sectionsObjects[i][0].className === getSectionName(clickedId);
            sectionsObjects[i][0].style.flex = isSection ? 4 : 1;
            if (isSection){
                sectionsObjects[i][0].style.backgroundColor = "rgba(0, 0, 0, 0.0)";
            }
        }
        lastBtn = clickedId;
    }
    else{
        lastBtn = "";        
    }
    handleSectionLogos(lastBtn);
}   




function startProcessing() {
    hideOtherElements(); 
    rotateShip(); 
    ImagesProcessing()
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
    const dz_images = document.getElementsByClassName("dz-preview dz-processing dz-success dz-complete dz-image-preview")
    const dzImagesArray = Array.from(dz_images);
    dzImagesArray.forEach(image => {
    image.parentNode.removeChild(image);
    })

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

function ImagesProcessing() {
    return new Promise((resolve, reject) => {
        fetch(HomeUrl + "/process")
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json(); 
            })
            .then(data => {
                console.log("Image processing complete", data);
                resolve(data);
            })
            .catch(error => {
                console.error("Error during image processing:", error);
                reject(error);
            });
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
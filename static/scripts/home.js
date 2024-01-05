let selectionButtons = ["imagens_btn", "apresentacao_btn", "video_btn"];
let selectionObjects = selectionButtons.map(string => document.getElementById(string));
const getSectionName = string => string.split("_")[0];
const getBtnName = string => string === "" ? "" : string+"_btn";
const MatchList = [["imagens","camera_hover.png"],
                   ["apresentacao","presentation_white.png"],
                   ["video","video_white.png"]
                  ];


function handleImagensSection() {
    console.log("todo".toUpperCase())
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
            const innerImageId = tuple[0] + "_inner_image";
            const sectionObject = document.getElementsByClassName(tuple[0])[0];
            const innerImageElement = document.getElementById(innerImageId);
            if (innerImageElement){
                sectionObject.removeChild(innerImageElement);
            }
            const img = document.createElement('img');
            img.id  = innerImageId; 
            img.src = `static/images/` + tuple[1];
            img.className = "logos";
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
    section[0].addEventListener('click', function () {
        handleButtonClick(getBtnName(sectionName))     
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
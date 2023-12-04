var ShipFrameChanged = false;

function change_frame() {
    var shipFrame = document.getElementById("ShipFrame");
    if (ShipFrameChanged){
        shipFrame.innerHTML = "<p>Aqua Depth</p>";
        shipFrame.className = "data_ship_frame";
        ShipFrameChanged = false;
    }
    else{
        shipFrame.innerHTML = "<p>Aqua Depth 7</p>";
        shipFrame.className = "log_frame";
        ShipFrameChanged = true;
    }
}

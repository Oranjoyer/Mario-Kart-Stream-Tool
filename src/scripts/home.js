var hueRotate = 0;
var saturation = 100;
var brightness = 100;
var colorPrev;
var hueRotationInput;

console.log("Page")
    console.log("PageIsHere")
    colorPrev = document.getElementById("colorModPreview")
    document.getElementById("hueRotationIn").addEventListener("change",()=>{hueRotate=document.getElementById("hueRotationIn").value;colorAdjustment(colorPrev,hueRotate,saturation,brightness)})
    document.getElementById("hueRotationSlider").addEventListener("change",()=>{hueRotate=document.getElementById("hueRotationSlider").value;colorAdjustment(colorPrev,hueRotate,saturation,brightness)})

    document.getElementById("saturationIn").addEventListener("change",()=>{saturation=document.getElementById("saturationIn").value;colorAdjustment(colorPrev,hueRotate,saturation,brightness)})
    document.getElementById("saturationSlider").addEventListener("change",()=>{saturation=document.getElementById("saturationSlider").value;colorAdjustment(colorPrev,hueRotate,saturation,brightness)})

    document.getElementById("lightnessIn").addEventListener("change",()=>{brightness=document.getElementById("lightnessIn").value;colorAdjustment(colorPrev,hueRotate,saturation,brightness)})
    document.getElementById("lightnessSlider").addEventListener("change",()=>{brightness=document.getElementById("lightnessSlider").value;colorAdjustment(colorPrev,hueRotate,saturation,brightness)})


function colorAdjustment(imageElement,H,S,L)
{
    imageElement.style.filter ="hue-rotate("+H+"deg) saturate("+S+"%) brightness("+L+"%)";

    return imageElement
}

function setPlayerColor()
{
    let hue = document.getElementById("hueRotationIn").value
    let saturation = document.getElementById("saturationIn").value
    let brightness = document.getElementById("brightnessIn").value

    window.electronAPI.setColor([null,{H:hue,S:saturation,L:brightness}]);
}
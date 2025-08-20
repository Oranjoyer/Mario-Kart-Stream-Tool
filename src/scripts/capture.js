{
let capSelected = false
// function loadCapture(capId)
// {
//     window.electronAPI.getCapFromId(capId)
// }
async function selectCapture(id) {
    capture = window.electronAPI.getCapDetails(id)

    document.getElementById("selectCapture").value = id

    // document.getElementById("name") = capture.name
    document.getElementById("heightRes") = capture.height
    document.getElementById("widthRes") = capture.width
    document.getElementById("fps") = capture.framerate
    document.getElementById("port") = capture.port

}

async function loadCameras()
{
    let camBox = document.getElementById("cameraSelect")
    let cams = await window.electronAPI.getOpenCams()
    console.log(cams)
    camBox.innerHTML = ""
    for(let i = 0; i < cams.length;i++)
    {
        let option = document.createElement("option")
        option.value = cams[i].id;
        option.innerHTML = cams[i].name;
        camBox.appendChild(option)
        
    }
}
async function setupPage()
{
    loadCameras()
    setPlaceholderPort()
    loadCaptureList()

}
async function startCapture()
{
    if(capSelected)
    {
        return
    }
    let camera = document.getElementById("cameraSelect").value
    console.log(camera)
    let height = document.getElementById("heightRes").value
    let width = document.getElementById("widthRes").value
    let port = document.getElementById("port").value
    let fps = document.getElementById("fps").value

    window.electronAPI.createCapture(camera,height,width,fps,port).then((cap)=>{loadCaptureList();loadCameras();selectCapture(cap.id)})
    
}
async function loadCaptureList() {
    let capBox = document.getElementById("selectCapture")
    let caps = await window.electronAPI.getCaptures()
    console.log(caps)
    capBox.innerHTML = ""
    for(let i = 0; i < caps.length;i++)
    {
        let option = document.createElement("option")
        option.value = caps[i][1]
        option.innerHTML = caps[i][0]
        capBox.appendChild(option)
        
    }
}
async function setPlaceholderPort()
{
    document.getElementById("port").placeholder = await window.electronAPI.getDefPort()
}
document.getElementById("pickVideoFile").addEventListener("click",()=>{
    window.electronAPI.pickFile().then((file)=>{
        if(!file.canceled){
            let camBox = document.getElementById("cameraSelect")
            let elem = document.createElement("option")
            elem.value = file.filePaths[0]
            elem.innerText = file.filePaths[0]
            camBox.appendChild(elem)

        }

    })
})
document.getElementById("startCapture").addEventListener("click",startCapture)
setupPage()
}
{
// function loadCapture(capId)
// {
//     window.electronAPI.getCapFromId(capId)
// }
async function selectCapture(id) {
    let capture = await window.electronAPI.getCapDetails(id)
    console.log(capture)

    let form = document.forms["capForm"]


    document.getElementById("selectCapture").value = id
    document.getElementById("cameraSelect").value = "unchanged"

    // document.getElementById("name") = capture.name
    form.height.value = capture.height
    form.width.value = capture.width
    form.framerate.value = capture.framerate
    form.port.value = capture.port

    if(capture.proc != null)
    {
        setActive(true)
    }

}
function getFormElem(form,id){
    return form.getElementById(id)
}
function setActive(opt) {
    if(opt){
    document.getElementById("startCapture").display = "block"
    document.getElementById("stopCapture").display = "none"
    return
    }
    
    document.getElementById("startCapture").display = "none"
    document.getElementById("stopCapture").display = "block"

}

async function loadCameras()
{
    let camBox = document.getElementById("cameraSelect")
    let cams = await window.electronAPI.getOpenCams()
    console.log(cams)
    camBox.innerHTML = ""
    {
    let option = document.createElement("option")
        option.value = "unchanged";
        option.innerHTML = "Unchanged";
        camBox.appendChild(option)
    }
    for(let i = 0; i < cams.length;i++)
    {
        let option = document.createElement("option")
        option.value = cams[i].id;
        option.innerHTML = cams[i].name;
        camBox.appendChild(option)
        
    }
}
async function loadCapturePage()
{
    loadCameras()
    setPlaceholderPort()
    loadCaptureList()

}

async function startCapture()
{
    if(document.getElementById("selectCapture").value != "new")
    {
        let form = document.getElementById("capForm")
        let attr = {height:form["height"],width:form["width"],framerate:form["framerate"]}
        if(document.getElementById("cameraSelect").value!="unchanged")
            attr.camera = document.getElementById("cameraSelect").value
        window.electronAPI.modifyCapture(document.getElementById("capForm").value,attr)
        return
    }
    if(document.getElementById("cameraSelect").value=="unchanged")
        return
    let camera = document.getElementById("cameraSelect").value
    console.log(camera)
    let height = document.getElementById("heightRes").value
    let width = document.getElementById("widthRes").value
    let port = document.getElementById("port").value
    let fps = document.getElementById("fps").value

    window.electronAPI.createCapture(camera,width,height,fps,port).then((cap)=>{loadCaptureList();loadCameras();selectCapture(cap.id)})
    
}
async function loadCaptureList() {
    let capBox = document.getElementById("selectCapture")
    let caps = await window.electronAPI.getCaptures()
    console.log(caps)
    capBox.innerHTML = ""
    {
        let option = document.createElement("option")
        option.value = "new"
        option.innerHTML = "New Capture"
        capBox.appendChild(option)
    }
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
document.getElementById("selectInstance").addEventListener("click",()=>selectCapture(document.getElementById("selectCapture").value))
loadCapturePage()

}
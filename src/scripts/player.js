{

async function enablePlayer()
{
    // if(document.getElementById("selectCapture").value != "new")
    // {
    //     let form = document.getElementById("capForm")
    //     let attr = {height:form["height"],width:form["width"],framerate:form["framerate"]}
    //     if(document.getElementById("cameraSelect").value!="unchanged")
    //         attr.camera = document.getElementById("cameraSelect").value
    //     window.electronAPI.modifyCapture(document.getElementById("capForm").value,attr)
    //     return
    // }
    let capture = document.getElementById("selectCapture").value
    let playerName = document.getElementById("name").value
    // console.log(capture)

    window.electronAPI.createPlayer(playerName,capture).then(()=>{loadPlayerList();loadCaptureList()})
    
}

async function loadCaptureList() {
    let capBox = document.getElementById("selectCapture")
    let caps = await window.electronAPI.getCaptures()
    console.log(caps)
    capBox.innerHTML = ""
    {
        let option = document.createElement("option")
        option.value = null
        option.innerHTML = "None"
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

async function loadPlayerList() {
    let playerBox = document.getElementById("selectPlayer")
    let players = await window.electronAPI.getPlayers()
    console.log(players)

    playerBox.innerHTML = ""
    {
        let option = document.createElement("option")
        option.value = null
        option.innerHTML = "New"
        playerBox.appendChild(option)
    }
    for(let i = 0; i < players.length;i++)
    {
        let option = document.createElement("option")
        option.value = players[i].id
        option.innerHTML = players[i].name
        playerBox.appendChild(option)
    }
}

function loadPlayerPage()
{
    loadCaptureList()
    loadPlayerList()
}
document.getElementById("enablePlayer").addEventListener("click",enablePlayer)

loadPlayerPage()
}
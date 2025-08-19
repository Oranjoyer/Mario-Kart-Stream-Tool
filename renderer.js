
var playerList = []
var cameraList = []
var pageContents;
const parser = new DOMParser();
var pages = {}

document.addEventListener("DOMContentLoaded",()=>{
    pageContents = document.getElementById("pageContents")
    indexPages()
    loadPage("home")

})

function indexPages(){
    let templates = document.querySelectorAll("link[rel=import]")
    console.log(templates)
    templates.forEach((temp)=>{
        // temp = document.importNode(temp)
        let template = temp.import()
        console.log(temp)
        pages[template.pageName] = template
    })
}

async function loadPage(name)
{
    window.versions.node()
    let pag = document.importNode(pages[name],true)
    pageContents.innerHTML = ""
    pageContents.appendChild(pag)
}
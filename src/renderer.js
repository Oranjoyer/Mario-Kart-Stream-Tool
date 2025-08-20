var playerList = []
var cameraList = []
var pageContents;
const parser = new DOMParser();
var pages = {}

document.addEventListener("DOMContentLoaded",()=>{
    pageContents = document.getElementById("pageContents")
    indexPages().then(()=>{
        loadPage("Home")

    }) 

})

async function indexPages(){
    let templates = document.querySelectorAll("link[rel=import]")
        for(let temp of templates)
        {
            // temp = document.importNode(temp)
            let resp = await fetch(temp.href)
            let ret = await resp.text()
                console.log(ret)
                let parsed = parser.parseFromString(ret,"text/html").getElementsByTagName("template")[0]
                let pageName = parsed.getAttribute("pageName")
                console.log(parsed.getAttribute("listPage"))
            if(parsed.getAttribute("listPage")=="true"){
                let link = document.createElement("button");
                link.addEventListener("click",()=>{
                    loadPage(pageName)
                })
                link.innerHTML = pageName
                link.className = "toolbarButton"
                document.getElementById("toolbar").appendChild(link)
            }
                pages[pageName] = parsed
                console.log(parsed)
        }
        
    
}

async function loadPage(name)
{
    let pag = pages[name].content.cloneNode(true)
    pageContents.innerHTML = ""
    // console.log(pages[name])
    // pageContents.appendChild(pages[name])
    pageContents.appendChild(pag)
    // pageContents.innerHTML = pages
}
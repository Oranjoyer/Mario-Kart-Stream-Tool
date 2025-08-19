const { app, BrowserWindow, Menu, ipcMain } = require('electron/main')
const { create } = require('node:domain')
const path = require('node:path')
const pyInterface = require("./pythonInterface.js")

function createWindow()
{
    const win= new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences:{
            preload: path.join(__dirname, 'preload.js')
        }
    })
    // win.setMenu(Menu)
    // win.setMenuBarVisibility(true)
    win.webContents.openDevTools()
    win.loadFile("index.html")
}


app.whenReady().then(()=>{
    ipcMain.on("log",(mess)=>{console.log("EEEEE\n"+mess)})

    
    createWindow()
    pyInterface.init().then(()=>{
        console.log("Interface Started");
    })



})
app.on("window-all-closed",()=>{
    pyInterface.shutdown()
})
process.on('SIGINT', function() {
    pyInterface.shutdown()
    app.exit()
});


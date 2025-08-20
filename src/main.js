const { dialog } = require('electron')
const { app, BrowserWindow, Menu, ipcMain } = require('electron/main')
const { create } = require('node:domain')
const path = require('node:path')
const pyInterface = require(path.join(__dirname, 'pythonInterface.js'))
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
    win.loadFile(path.join(__dirname,"index.html"))
}


app.whenReady().then(()=>{
    ipcMain.on("log",(mess)=>{console.log(mess)})
    ipcMain.handle("createCapture",(_event,camera,width,height,framerate,preset="ultrafast")=>{return pyInterface.invokeRequest("createCapture",[camera,width,height,framerate,preset="ultrafast"])})
    ipcMain.handle("pickFile",()=>{return dialog.showOpenDialog({properties: ['openFile']})})
    ipcMain.handle("getCams",()=>{return pyInterface.invokeRequest("getCams")})
    ipcMain.handle("getCaptures",()=>{return pyInterface.invokeRequest("getCaptures")})
    ipcMain.handle("getFreeCaps",()=>{return pyInterface.invokeRequest("getFreeCaps")})
    ipcMain.handle("getPlayers",()=>{return pyInterface.invokeRequest("getPlayers")})
    ipcMain.handle("createPlayer",(_event,name,camera)=>{return pyInterface.invokeRequest("createPlayer",[name,camera])})
    ipcMain.on("setColor",(player,color)=>{pyInterface.makeRequest("setColor",null,[player,color])})
    ipcMain.handle("getCapDetails",(_group,id)=>{return pyInterface.invokeRequest("getCapDetails",[id])})
    ipcMain.handle("getDefPort",()=>{return pyInterface.invokeRequest("currentPort")})
    ipcMain.handle("getOpenCams",()=>{return pyInterface.invokeRequest("getOpenCams")})
    createWindow()
    pyInterface.init().then(()=>{
        console.log("Interface Started");
        console.log(__dirname)
    })



})
app.on("window-all-closed",()=>{
    pyInterface.shutdown()
})
process.on('SIGINT', function() {
    pyInterface.shutdown()
    app.exit()
});


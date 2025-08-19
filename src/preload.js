const { contextBridge, contentTracing, ipcRenderer } = require('electron/renderer')
// const { promises } = require('original-fs')

contextBridge.exposeInMainWorld('versions',{
    node: () => process.versions.node,
    chrome: () => process.versions.chrome,
    electron: () => process.versions.electron,
})

contextBridge.exposeInMainWorld('electronAPI',{
    getPlayerList: () => ipcRenderer.send("getPlayers"),
    createPlayer: (name,capture) => ipcRenderer.invoke("createPlayer",name,capture),
    modifyPlayer: (id,attributes)=>  ipcRenderer.send("modifyPlayer",id,attributes),
    removePlayer: (id)=> ipcRenderer.send("removePlayer",id),
    getCams: () => ipcRenderer.invoke("getCams"),
    getCapList: () => ipcRenderer.invoke("getCapList"),
    createCapture: (camera,width,height,framerate,preset="ultrafast") => ipcRenderer.send("createCapture",camera,width,height,framerate,preset),
    modifyCapture: (id,attributes) => ipcRenderer.send("modifyCapture",id,attributes),
    getMenu: (path) => ipcRenderer.invoke("getMenu",path),
    log: (mess) => ipcRenderer.send("log",mess)
})
var interface = require("./pythonInterface.js")
interface.init(main)

function main()
{
let start = Date.now()
interface.makeRequest("foo",function(){
    console.log(Date.now()-start)
})
console.log("starting")
interface.makeRequest("getCams",console.log)
interface.sendCommand("createCapture",["mkVid.mkv"])
interface.sendCommand("createPlayer",["Red",0])
interface.sendCommand("modifyPlayer",[0,{"colorAdj":{"H":0,"S":100,"L":100}}])
interface.sendCommand("createPlayer",["White",0])
interface.sendCommand("createPlayer",["Orange",0])
interface.sendCommand("modifyPlayer",[2,{"colorAdj":{"H":28,"S":100,"L":100}}])
let hue = 0
setInterval(()=>{interface.sendCommand("modifyPlayer",[2,{"colorAdj":{"H":hue++,"S":100,"L":100}}])},100)
setTimeout(()=>{interface.sendCommand("createPlayer",["Random",0])},Math.random()*5000+5000)
setTimeout(()=>{interface.sendCommand("removePlayer",[1])},Math.random()*10000+50000)
setTimeout(()=>{interface.sendCommand("modifyPlayer",[0,{"name":"John","place":12,"finished":true}])},60000)


}
let compSys = require('os');
const { spawn } = require('node:child_process');
const { rootCertificates } = require('node:tls');
const { json, buffer } = require('node:stream/consumers');
const { callbackify } = require('node:util');
const { read } = require('node:fs');
const { Readline } = require('node:readline/promises');
const { time } = require('node:console');
const path = require('node:path')

let sendQueue = []
var pyServer;

let pyFunc = {};

let dataStart = ":CMDSTART:";
let dataEnd = ":CMDEND:";
let currentReqNo = 0

let requestQueue = []
let lastPulse = -1

let initResolve
let initialized = new Promise((res)=>{initResolve=res})

class WaitingRequest
{
    constructor(id,callback)
    {
        this.id = id
        this.callback = callback
    }
}
function fulfillRequests(receivedResponse)
{
    if(typeof(receivedResponse) == String)
        receivedResponse = JSON.parse(receivedResponse);
    
    for(let i = requestQueue.length-1; i >= 0; i--)
    {
        let req = requestQueue[i]
        if(receivedResponse.requestId==req.id)
            {
                requestQueue.splice(i,1)
                req.callback(receivedResponse.response)
            }
        }
        // console.log("---")
}

async function init(callback=null)
{
    // setInterval(releaseData,1000*(1/2))
    let prom = new Promise((resolve)=>{
    initialized.then((res)=>{
        setInterval(pulse,2500)
        
        // pythonFunctionSystem(res)
        // pyFunc.heartbeat().then(console.log)
        if(callback)
            callback()
        resolve()
    })})
    spawnServer()
    return prom
    
}
function sendCommand(functionName,args=[],requestId=-1)
{
    jsonData = {"functionName" : functionName, "args":args,"requestId":requestId}
    sendData(JSON.stringify(jsonData));
}
function makeRequest(functionName,callback,args=[])
{
    let requestId = -1
    if(callback!=null)
    {
        requestId = Math.floor(Math.random()*Number.MAX_SAFE_INTEGER)
        for(let r of requestQueue)
        {
            if(requestId==r.requestId)
            {
                requestId=++currentReqNo
            }
        }
        if(currentReqNo>=Number.MAX_SAFE_INTEGER)
            currentReqNo = 0
    }
    if(requestId!=-1)
        requestQueue.push(new WaitingRequest(requestId,callback));
    sendCommand(functionName,args,requestId)
    return true;
}
async function invokeRequest(functionName,args=[])
{
    let prom = new Promise((resolve)=>makeRequest(functionName,resolve,args))
    return prom
}
function sendData(data)
{
    if(!pyServer)
    {
        // console.log("pyServer not active")
        return
    }
    data = Buffer.from(data).toString("base64");
    pyServer.stdin.write("\n"+dataStart+data+dataEnd+"\n");
    // sendQueue.push(data)
    

}
// function releaseData()
// {
//     if(pyServer==null)
//         return
//     if(sendQueue.length!=0 && pyServer != null)
//     {
//         let data = sendQueue.pop()
//         pyServer.stdin.write("\n"+dataStart+data+dataEnd+"\n");
//     }
// }
function getDataBounds(data)
{
    let start = data.indexOf(dataStart) +dataStart.length;
    let end = data.indexOf(dataEnd);
    if(start==-1||end==-1)
        return [0,0];
    return [start,end];
}
function decodeData(data)
{
    let bounds = getDataBounds(data)
    data = data.substring(bounds[0],bounds[1]);
    return Buffer.from(data, 'base64').toString('utf8');
}
async function readData(recData)
{
    // let recData = pyServer.stdin.read()
    if(recData==null)
        {
            return
        }
    recData = decodeData(recData);
    if(recData.length == 0)
        return
        
    try
    {
    let data = JSON.parse(recData)
    if(data.requestId==-2)
    {
        log(data.response)
    }
    else if(data.requestId==-3)
    {
        // console.log("ee")
        
        initResolve(data.response)
    }
    else{
        fulfillRequests(data)
    }
    }
    catch(e)
    {
        console.log(e)
        return
    }
    
}
function spawnServer()
{
    if(pyServer!=null)
        return
    // console.log(path.join(__dirname,"pySrc",'app.py'))
    pyServer = spawn("python", [path.join(__dirname,"pySrc",'app.py')],{cwd:__dirname,env:process.env})
    // pyServer.stdin.setEncoding('utf-8')
    pyServer.stdout.on("data",(data)=>{
        // console.log(data)
        let dataArr = Buffer.from(data).toString().split("\n")
        // log(data)
        for(let dt of dataArr)
            readData(dt)
    })
    pyServer.stderr.on("data",(data)=>{
        data = Buffer.from(data).toString()
        log(data)
    })
}
function pythonFunctionSystem(functions){
    functions.forEach(f => {
        (function(f){
        pyFunc[f]=(args)=>{return new Promise( (resolve)=>{
            console.log(args)
            makeRequest(pyFunc[f],resolve,args)})
        }}(f))
    });
}
function stopServer()
{
    makeRequest("getpid",(val)=>{process.kill(val,'SIGTERM')})
    sendCommand("stop")
    log("Python Server Stopped")
    pyServer = null
}

// Designed for logs in the future
function log(string)
{
    console.log(string)
}
function print(string)
{
    log(string)
}

function main()
{
    
}
function pulse()
{
makeRequest("pulse",function(){
    lastPulse = Date.now()
})
if(lastPulse!=-1 && Date.now()-lastPulse>5000)
{
    shutdown()
}
}
process.on('SIGINT', function() {
    shutdown()
});

function shutdown()
{
    console.log("Shutting Down")
    pyServer.on("exit",function(){process.exit(0)})
    stopServer()
}
// init()
// while(true)
// {
//     sendCommand("heartbeat")
// }
module.exports = {init,sendCommand,makeRequest,shutdown,invokeRequest}



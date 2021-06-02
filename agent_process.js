const { workerData, parentPort } = require('worker_threads')
const Agent = require('./agent')
const { agents } = require('./examples/config1')
const colours = require('./utils')


const configFilePath = workerData.configFilePath;
const agentName = workerData.agentName

const agent = new Agent(configFilePath, agentName)

parentPort.on("message", message => {
    //messageFromParent
    let com = message.command
    let splittedCom = com.split(' ')
    if(splittedCom.length == 2){
        agent.setKBValue(splittedCom[0], splittedCom[1])
        agent.debug()
    }
    else{
        process.stderr.write(colours.red + "Poorly formatted command")
    }
    // GET THE COMMAND FROM THE OBJECT; PARSE IT; CHANGE THE KB OF THE BOT, FOR EXAMPLE
})

setTimeout(()=>agent.start(), 1000)

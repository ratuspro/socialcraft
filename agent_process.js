const { workerData, parentPort } = require('worker_threads')
const Agent = require('./agent')

const configFilePath = workerData.configFilePath;
const agentName = workerData.agentName

const agent = new Agent(configFilePath, agentName)


parentPort.on("message", incoming => {
    // GET THE COMMAND FROM THE OBJECT; PARSE IT; CHANGE THE KB OF THE BOT, FOR EXAMPLE
})


agent.connect()
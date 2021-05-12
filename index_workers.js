const { Worker } = require('worker_threads')
const colours = require('./utils')

const configFilePath = process.argv.slice(2)[0];
const configuration = require(configFilePath);

let workers = []

process.on('message', (m) => {
    //console.log('CHILD got message from parent: ', m); //Receiving message from parent
    let foundAnyTarget = false
    for(let obj of workers){
        if(Object.keys(obj)[0].toLowerCase() == m.target.toLowerCase()){
            let worker = Object.values(obj)[0]
            process.stdout.write(colours.yellow + JSON.stringify(m) + colours.normal + "\n")
            worker.postMessage(m)
            foundAnyTarget = true
        }
    }
    if(!foundAnyTarget){
        process.stderr.write(colours.red + "There is no target with the specified name!\n" + colours.normal)
    }else{
        //process.stdout.write("Target Found\n") Tudo correu bem, se calhar não é necessário loggar
    }
    //process.send("ACK") //Sending message to parent
});

function launchAgentProcess(data) {
    return new Promise((resolve, reject) => {
        const worker = new Worker('./agent_process.js', { workerData: data});
        worker.on("message", incoming => console.log({ incoming }));
        const key = data.agentName
        const obj = {}
        obj[key] = worker
        workers.push(obj)
    })
}

function run() {

    for (let agent of configuration["agents"]){

        let agentProcessData= {
            configFilePath: configFilePath,
            agentName: agent['name'],
        }

        launchAgentProcess(agentProcessData)
    }
}

run()
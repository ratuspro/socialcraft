const { Worker } = require('worker_threads');

const configFilePath = process.argv.slice(2)[0];
const configuration = require(configFilePath);

let workers = []

process.on('message', (m) => {
    //console.log('CHILD got message from parent: ', m); //Receiving message from parent

    for(let obj of workers){
        if(Object.keys(obj)[0].toLowerCase() == m.target.toLowerCase()){
            let worker = Object.values(obj)[0]
            worker.postMessage(m)
        }
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
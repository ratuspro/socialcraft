const { Worker } = require('worker_threads');

const configFilePath = process.argv.slice(2)[0];
const configuration = require(configFilePath);

function launchAgentProcess(workerData) {
    return new Promise((resolve, reject) => {
        const worker = new Worker('./agent_process.js', { workerData });
    })
}

function run() {
    let identities = configuration["identities"];

    for (let agent of configuration["agents"]){

        let agentProcessData= {
            configFilePath: configFilePath,
            agentName: agent['name'],
        }

        launchAgentProcess(agentProcessData)
    }
}

run();
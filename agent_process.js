const { workerData, parentPort } = require('worker_threads')

const configFilePath = workerData.configFilePath;
const agentName = workerData.agentName;

const agent = {};
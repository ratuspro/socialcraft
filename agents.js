const mineflayer = require('mineflayer')
const { pathfinder, Movements, goals } = require('mineflayer-pathfinder')

const configPath = './examples/config1.js'
const configuration = require(configPath)

const agentName = process.argv[2]

function getRelevantInformation(agentName){
    let agent = configuration["agents"].filter(agent => agent["name"] == agentName)[0]

    let identities = configuration["identities"].filter(identity => agent["identities"].includes(identity["name"]))

    let checkedIdentities = identities.filter(identity => identity["variables"]["necessary"].every(field => field in agent["knowledge_base"]))

    if(JSON.stringify(checkedIdentities) == JSON.stringify(identities)){
        console.log("All identities are able to be performed!")

    }
    else{
        console.log("Not all identities are able to be performed!")
    }

    return {"agent": agent, "identities": checkedIdentities}
}

function getMostSalientIdentity(agentAndIds){
    let mostSalientIdentity = null
    let biggestSalienceValue = -1
    let identities = agentAndIds.identities
    let agent = agentAndIds.agent
    for(let i=0; i<identities.length; i++){
        for(let j=0; j<identities[i]["salience"].length; j++){
            let salianceValue = identities[i]["salience"][j].call(this, agent.knowledge_base)
            if(salianceValue >= biggestSalienceValue){
                biggestSalienceValue = salianceValue
                mostSalientIdentity = identities[i]["name"]
            }
            console.log("Identity -> " + identities[i]["name"])
            console.log("Saliance Value -> " + salianceValue)
            console.log("----------------")
        }
    }
}

let agentAndIdentities = getRelevantInformation(agentName)

getMostSalientIdentity(agentAndIdentities)

//const bot = mineflayer.createBot({
//    host: 'localhost',
//    port: 8080,
//    username: agentName,
//})
//
//bot.loadPlugin(pathfinder)
//
//bot.on('time', async() =>{
//
//})

// MINEFLAYER CONTENT --> on time, calcular a saliencia de todas as identidades possiveis
//                        Se a ação se mantiver a mesma, continuar a fazê-la.
//                        Caso contrário, mudar.
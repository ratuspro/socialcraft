const mineflayer = require('mineflayer')

const configPath = './examples/config1.js'
const configuration = require(configPath)

const agentName = process.argv[2]

function getRelevantInformation(agentName){
    let agent = configuration["agents"].filter(agent => agent["name"] == agentName)[0]

    let identities = configuration["identities"].filter(identity => agent["identities"].includes(identity["name"]))

    let checkedIdentities = identities.filter(identity => identity["variables"]["necessary"].every(field => field in agent["knowledge_base"][0]))

    if(JSON.stringify(checkedIdentities) == JSON.stringify(identities)){
        console.log("All identities are able to be performed!")

    }
    else{
        console.log("Not all identities are able to be performed!")
    }

    return [agent, checkedIdentities]
}

let a = getRelevantInformation(agentName)

console.log(a)


// MINEFLAYER CONTENT --> on time, calcular a saliencia de todas as identidades possiveis
//                        Se a ação se mantiver a mesma, continuar a fazê-la.
//                        Caso contrário, mudar.
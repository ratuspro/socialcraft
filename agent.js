const mineflayer = require('mineflayer')
const {Vec3} = require('vec3')
const colours = require('./utils')
const { pathfinder, Movements, goals } = require('mineflayer-pathfinder')

class Agent{
    constructor(cFPath, aName){

        const configuration = require(cFPath)     
        let agent = configuration["agents"].filter(agent => agent["name"] == aName)[0] 
        let identities = configuration["identities"].filter(identity => agent["identities"].includes(identity["name"]))
        let checkedIdentities = identities.filter(identity => identity["variables"]["necessary"].every(field => field in agent["knowledge_base"]))
        let agentHouse = configuration["houses"].filter(house => house.agents.includes(aName))
        let othersBBoxes = []
        configuration["houses"].filter(house => !house.agents.includes(aName)).forEach(element => {
            othersBBoxes.push(element.bbox)
        });

        this.agentName = aName
        this.possibleIdentities = checkedIdentities
        this.KB = agent.knowledge_base
        this.house = agentHouse
        this.neighbourBBoxes = othersBBoxes

        this.getMostSalientIdentity()
    }

    get get_name(){
        return this.agentName
    }
    get get_identities(){
        return this.possibleIdentities
    }
    get get_knowledge_base(){
        return this.KB
    }
    get get_house(){
        return this.house
    }
    get get_neighbourBBoxes(){
        return this.neighbourBBoxes
    }

    getMostSalientIdentity(){
        let mostSalientIdentity = null
        let biggestSalienceValue = -1
        for(let i=0; i < this.possibleIdentities.length; i++){
            for(let j=0; j < this.possibleIdentities[i]["salience"].length; j++){
                let salianceValue = this.possibleIdentities[i]["salience"][j].call(this)
                if(salianceValue >= biggestSalienceValue){
                    biggestSalienceValue = salianceValue
                    mostSalientIdentity = this.possibleIdentities[i]
                }
            }
        }
        this.mostSalientIdentity = mostSalientIdentity
    }

    debug(){
        this.mostSalientIdentity.execute.call(this)
    }

    setKBValue(property, value){
        console.log(this.KB)
        if(property in this.KB)
            this.KB[property] = value
        else
            console.error(colours.red + "That property is not a part of the KB." + colours.normal)
        console.log(this.KB)
    }

    connect(){
        const bot = mineflayer.createBot({
            host: 'localhost',
            port: 8080,
            username: this.agentName,
        })
        
        bot.loadPlugin(pathfinder)
        
        bot.on('time', async() =>{
            let currentActivity = this.mostSalientIdentity
            this.getMostSalientIdentity()
            if(currentActivity == this.mostSalientIdentity){
                ()=>{}
            }
            else{
                this.mostSalientIdentity.execute.call(this)
            }
        })
    }
}

module.exports = Agent
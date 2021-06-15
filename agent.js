const mineflayer = require('mineflayer')
const {Vec3} = require('vec3')
const colours = require('./utils')
const { pathfinder, Movements, goals } = require('mineflayer-pathfinder')
const GoalNoTespassing = require('./GoalNoTrespassing').GoalNoTespassing
const GoalFollow = goals.GoalFollow
var mcData = require('minecraft-data')('1.16.1')

class Agent{
    constructor(cFPath, aName){

        const configuration = require(cFPath)     
        let agent = configuration["agents"].filter(agent => agent["name"] == aName)[0] 
        let identities = configuration["identities"].filter(identity => agent["identities"].includes(identity["name"]))
        let checkedIdentities = identities.filter(identity => identity["variables"]["necessary"].every(field => agent["knowledge_base"].inKB(field)))
        let agentHouse = configuration["places"]["houses"].filter(house => house.agents.includes(aName))
        let othersBBoxes = []
        configuration["places"]["houses"].filter(house => !house.agents.includes(aName)).forEach(element => {
            othersBBoxes.push(element.bbox)
        });
        let forestBBox = configuration["places"]["forest"]

        this.agentName = aName
        this.possibleIdentities = checkedIdentities
        this.kb = agent.knowledge_base
        this.house = agentHouse
        this.neighbourBBoxes = othersBBoxes
        this.forest = forestBBox
        this.bot = mineflayer.createBot({
            host: configuration["serverProperties"]["host"],
            port: configuration["serverProperties"]["port"],
            username: this.agentName,
        })
        this.bot.loadPlugin(pathfinder)
        
        this.kb.set_kb('bot', this.bot)
        this.kb.set_kb('name', this.agentName)

        this.bot.on('chat', (username,message) => {
            if(username === this.aName) return
            if(message == "gospawn") this.bot.chat("/home")
        })
        //this.bot.on('chat', (username,message) => {
        //    if(username === this.aName) return
        //    if(message == "setspawn") this.bot.chat("/sethome")
        //}) sets the spawn for all the bots, they have to be home before using this
    }

    get get_name(){
        return this.agentName
    }
    get get_identities(){
        return this.possibleIdentities
    }
    get get_knowledge_base(){
        return this.kb
    }
    get get_house(){
        return this.house
    }
    get get_neighbourBBoxes(){
        return this.neighbourBBoxes
    }
    get get_Forest(){
        return this.forest
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

    getSalianceValues(){
        for(let i=0; i < this.possibleIdentities.length; i++){
            for(let j=0; j < this.possibleIdentities[i]["salience"].length; j++){
                let salianceValue = this.possibleIdentities[i]["salience"][j].call(this)
                console.log(this.possibleIdentities[i]["name"] + " --> " + salianceValue)
            }
        }
    }

    setKBValue(property, value){
        //process.stdout.write(JSON.stringify(this.kb, null, 2))
        if(this.get_knowledge_base.inKB(property))
            this.kb.set_kb(property, value)
        else
            process.stderr.write(colours.red + "That property is not a part of the KB." + colours.normal)
        //process.stdout.write(JSON.stringify(this.kb, null, 2))
    }

    locateExactBlock(exactBlock){
        const mcData = require('minecraft-data')(this.bot.version)   
        const movements = new Movements(this.bot, mcData)
        var block = null
        movements.canDig = false
        this.bot.pathfinder.setMovements(movements)

        if(exactBlock != null){
            block = exactBlock
        }

        if (!block){
            this.bot.chat("I cannot see the block you wanted me to locate!")
            return
        }

        try{
            const tool = this.bot.pathfinder.bestHarvestTool(this.bot.blockAt(block))
            this.bot.equip(tool, "hand", (err)=>{})
        } catch(e){
            process.stderr.write("unable to equip the tool :(\n" + e)
        }

        const x = block.x 
        const y = block.y 
        const z = block.z

        const goal = new GoalNoTespassing(x,y,z,this.neighbourBBoxes)
        this.bot.pathfinder.setGoal(goal)
    }

    locateBlock(matchingBlocks){
        const mcData = require('minecraft-data')(this.bot.version)   
        const movements = new Movements(this.bot, mcData)
        var block = null
        movements.canDig = false
        this.bot.pathfinder.setMovements(movements)

        if(matchingBlocks != null){
            const blocks = this.bot.findBlocks({
                matching: matchingBlocks,
                maxDistance: 200,
                count: 100
            })

            block = blocks[0]
        }

        if (!block){
            this.bot.chat("I cannot see the block you wanted me to locate!")
            return
        }

        try{
            const tool = this.bot.pathfinder.bestHarvestTool(this.bot.blockAt(block))
            this.bot.equip(tool, "hand", (err)=>{})
        } catch(e){
            process.stderr.write("unable to equip the tool :(\n" + e)
        }

        const x = block.x 
        const y = block.y 
        const z = block.z

        const goal = new GoalNoTespassing(x,y,z,this.neighbourBBoxes)
        this.bot.pathfinder.setGoal(goal)
    }

    locateBlockInArea(matchingBlocks, areaBBox){
        const mcData = require('minecraft-data')(this.bot.version)   
        const movements = new Movements(this.bot, mcData)
        var block = null
        movements.canDig = false
        this.bot.pathfinder.setMovements(movements)

        if(matchingBlocks != null){
            const blocks = this.bot.findBlocks({
                matching: matchingBlocks,
                useExtraInfo: (block) => areaBBox.inBBox(block.position),
                maxDistance: 200,
                count: 100
            })

            block = blocks[0]
        }

        if (!block){
            this.bot.chat("I cannot see the block you wanted me to locate!")
            return
        }

        try{
            const tool = this.bot.pathfinder.bestHarvestTool(this.bot.blockAt(block))
            this.bot.equip(tool, "hand", (err)=>{})
        } catch(e){
            process.stderr.write("unable to equip the tool :(\n" + e)
        }

        const x = block.x 
        const y = block.y 
        const z = block.z

        const goal = new GoalNoTespassing(x,y,z,this.neighbourBBoxes)
        this.bot.pathfinder.setGoal(goal)
    }

    digBlock(matchingBlocks, forestBBox){
        this.bot.on('goal_reached', async(goal) => {
            if(this.bot.canDigBlock(this.bot.blockAt(new Vec3(goal.x,goal.y,goal.z)))){
                await this.bot.dig(this.bot.blockAt(new Vec3(goal.x,goal.y,goal.z)))
            }
            this.locateBlockInArea(matchingBlocks, forestBBox)
        })
    }

    sleep(){
        this.bot.on('goal_reached', async(goal) => {
            if(this.bot.isABed(bot.blockAt(new Vec3(goal.x, goal.y, goal.z)))){
                try{
                    await this.bot.sleep(bot.blockAt(new Vec3(goal.x, goal.y, goal.z)))
                } catch(err){
                    this.bot.chat(`I cannot sleep: ${err.message}`)
                }
            }
            else{
                this.bot.chat('No bed nearby!')
            }
        })
    }
    
    async eat(){
        var data = mcData.foodsArray
        var names = data.map((item) => item.name)

        var found_food = this.bot.inventory.items().filter((item) => names.includes(item.name))

        if (found_food.length === 0 || !found_food) {
			process.stderr.write('No Food found.')
            return
		}

        var available_food = []

		this.bot.inventory.items().forEach((element) => {
			if (names.includes(element.name)) available_food.push(element)
		})

        var bestFood = null

        if(available_food.length <= 0){
            process.stderr.write("No available food! :(")
            return
        }

        if(this.kb.inKB("favourite_food")){
            var favFood = this.kb.getValue("favourite_food")
            if(names.includes(favFood)){
                bestFood = available_food.find(element => element.name == favFood)
            }
            else{
                bestFood = available_food[Math.floor(Math.random() * available_food.length)]
            }
        }
        else{
            bestFood = available_food[Math.floor(Math.random() * available_food.length)]
        }

        let b = this.bot

        b.equip(bestFood, 'hand', function (error){
            if(error){
                process.stderr.write(colours.red + error + colours.normal)
                return
            }
            else{
                b.consume(function(err){
                    if(err){
                        process.stderr.write(colours.red + err + colours.normal)
                        return
                    }
                })
            }
        })
    }

    debug(){
        this.getSalianceValues()
    }

    followme(){
        const me = this.bot.players["SilverLugia94"]
        const movements = new Movements(this.bot, mcData)
        this.bot.pathfinder.setMovements(movements)

        const goal = new GoalFollow(me.entity, 1)
        this.bot.pathfinder.setGoal(goal, true)
    }

    start(){
        this.bot.on('time', async() =>{
            let currentActivity = this.mostSalientIdentity
            this.getMostSalientIdentity()
            this.kb.updateTime()

            if(this.kb.getValue('energy') > 0){
                this.kb.set_kb('energy', this.kb.getValue('energy') - 1)
            }

            
            if(this.kb.getValue('hunger') < 1000){
                this.kb.set_kb('hunger', this.kb.getValue('hunger') + 1)
            }

            if(currentActivity == this.mostSalientIdentity){
                //console.log("NOOP")
            }
            else{
                //console.log("OP")
                this.bot.removeAllListeners('goal_reached')
                //this.mostSalientIdentity.execute.call(this)
            }
        })
    }
}

module.exports = Agent
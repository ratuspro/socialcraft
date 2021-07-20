const colours = require('./utils')

class KB{
    constructor(data){
        this.knowledge_base = data
    }

    get get_kb(){
        return this.knowledge_base
    }

    inKB(varName){
        if(varName in this.knowledge_base){
            return true
        }
        else{
            return false
        }
    }
    set_kb(prop, value){
        this.knowledge_base[prop] = value
    }
    getValue(varName){
        if(varName in this.knowledge_base) return this.knowledge_base[varName]
        else return null
    }
    wasPerceived(){
        return 1
    }
    wasPerceivedVicinity(block_name){
        const mcData = require('minecraft-data')("1.16.1")
        if(mcData.blocksByName[block_name] != undefined){
            const blocks = this.knowledge_base["bot"].findBlocks({
                matching: mcData.blocksByName[block_name].id,
                maxDistance: 20,
                count: 10
            })

            if(blocks.length > 0){
                return 1
            }
            else{
                return 0
            }
        }
        else{
            process.stderr.write(colours.red + "Item does not exist!" + colours.normal)
        }
    }
    wasPerceivedInventory(block_name){
        let items = this.knowledge_base["bot"].inventory.items().map(item => item.name)
        if(items.includes(block_name)){
            return 1
        }
        else{
            return 0
        }
    }
    agentsVicinity(){
        let kb = this.knowledge_base
        let players = this.knowledge_base["bot"].players
        let nearbyPlayers = []
        Object.keys(players).forEach(function(key){
            let value = players[key]
            if(key != kb["name"]){
                const myPos = players[kb["name"]].entity.position
                const otherPos = value.entity.position
                let distance = Math.sqrt( (Math.pow((myPos.x - otherPos.x), 2)) + (Math.pow((myPos.y - otherPos.y), 2)) + (Math.pow((myPos.z - otherPos.z), 2)) )
                if(distance < 15){
                    nearbyPlayers.push(value)
                }
            }
        })
        return nearbyPlayers
    }

    isFriendInVicinity(){
        let agentsInVicinity = this.agentsVicinity()
        agentsInVicinity.forEach((ag) => {
            if(this.getValue("friend_list").includes(ag.username)){
                return 1
            }
        })
        return 0
    }

    isNightTime(){
        if(this.getValue('time') < 0 || this.getValue('time') > 14000){
            return 1
        }
        else{
            return 0
        }
    }
    
    updateTime(){
        this.set_kb("time", this.knowledge_base["bot"].time.timeOfDay)   
    }
}

module.exports = KB
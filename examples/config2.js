/****** CONFIG 2 ******/
/* Launch 20 bots
/* Launch 20 bots
/* Launch 20 bots
/* Launch 20 bots
/* Launch 20 bots
/* Launch 20 bots
/* Launch 20 bots
/* Launch 20 bots
/* Launch 20 bots
*/
const {Vec3} = require('vec3')
const BoundingBox = require('../BoundingBox')
const KB = require('../KB')

 const config = {
    serverProperties : {
        host: 'localhost',
        port: 8080,
    },
    identities: [
        {
            name: "Lumberjack",
            variables: {
                necessary: ["wood_stock"],
                optional : ["favourite_wood"]
            },
            salience: [
                function() {
                    if(this.kb.getValue('energy') > 30){ //how much it wastes to mine a block
                        return (this.kb.getValue("wood_stock") > 15 ? 0 : 0.6)
                    }
                    else{
                        return 0
                    }
                },
                function() {
                    if(this.kb.getValue('energy') > 30){
                        return this.kb.wasPerceivedVicinity(this.kb.getValue("favourite_wood")) * 0.9
                    }
                    else{
                        return 0
                    }
                }
            ],
            execute: function () {
                const woodBlocks = [35, 36, 37, 38, 39, 40, 46, 41, 42, 43, 44, 45] /*wood blocks ids*/
                this.locateBlockInArea(woodBlocks, this.get_Forest)
                this.digBlock(woodBlocks, this.get_Forest)
            }
        }
    ],
    agents: [
        {
            name: '0', identities: ['Lumberjack'], knowledge_base: new KB({'favourite_wood': "acacia_log",'energy': 1000, 'energy_threshold': 300, 'wood_stock': 0}),
        },{
            name: '1', identities: ['Lumberjack'], knowledge_base: new KB({'favourite_wood': "acacia_log",'energy': 1000, 'energy_threshold': 300, 'wood_stock': 0}),
        },{
            name: '2', identities: ['Lumberjack'], knowledge_base: new KB({'favourite_wood': "acacia_log",'energy': 1000, 'energy_threshold': 300, 'wood_stock': 0}),
        },{
            name: '3', identities: ['Lumberjack'], knowledge_base: new KB({'favourite_wood': "acacia_log",'energy': 1000, 'energy_threshold': 300, 'wood_stock': 0}),
        },{
            name: '4', identities: ['Lumberjack'], knowledge_base: new KB({'favourite_wood': "acacia_log",'energy': 1000, 'energy_threshold': 300, 'wood_stock': 0}),
        },{
            name: '5', identities: ['Lumberjack'], knowledge_base: new KB({'favourite_wood': "acacia_log",'energy': 1000, 'energy_threshold': 300, 'wood_stock': 0}),
        },{
            name: '6', identities: ['Lumberjack'], knowledge_base: new KB({'favourite_wood': "acacia_log",'energy': 1000, 'energy_threshold': 300, 'wood_stock': 0}),
        },{
            name: '7', identities: ['Lumberjack'], knowledge_base: new KB({'favourite_wood': "acacia_log",'energy': 1000, 'energy_threshold': 300, 'wood_stock': 0}),
        },{
            name: '8', identities: ['Lumberjack'], knowledge_base: new KB({'favourite_wood': "acacia_log",'energy': 1000, 'energy_threshold': 300, 'wood_stock': 0}),
        },{
            name: '9', identities: ['Lumberjack'], knowledge_base: new KB({'favourite_wood': "acacia_log",'energy': 1000, 'energy_threshold': 300, 'wood_stock': 0}),
        }
    ],
    places: {
        houses: [],
        forest: new BoundingBox(new Vec3(-166, 69, 2), new Vec3(-181, 71, -8)),
    }
}

module.exports = config;
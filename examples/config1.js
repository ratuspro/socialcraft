/****** CONFIG 1 ******/
/* Identities:
/* - Sleep: when the agents energy levels goes beneath a threshold, the agent goes to sleep.
/* - Eat: when the agent sees its favourite food, it eats the food. Or, when the agent hunger passes a certain threshold, the agent eats something.
/* - Lumberjack: when the agent sees his favourite wood, chops it of and saves it. Or, when the agent has a low stock of wood, chops and collects any wood.
/* Agents:
/* - Jane Doe: has the identities Eat and Sleep and her favourite food is carrots
/* - John Doe: has the identities Sleep and Lumberjack and his favourite wood is oak
/* IMPORTANT NOTE : Names for the KB that represent in-game items, like the favourite food or wood have to have the correct name. Check blocksByName.txt file to make sure it exists.
/* IMPORTANT NOTE (CONT): There seem to be some incosistencies with names (for example, in inventory, the item 'carrot' is singular, but as a member in blocksByName object it is plural ('carrots'))
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
            name: "Sleep",
            variables: {
                necessary : ["energy", "energy_threshold", "bed"],
                optional: []
            },
            salience: [
                function() {
                    if(this.kb.isNightTime())
                        return Math.max(0,((this.kb.getValue("energy_threshold") - this.kb.getValue("energy"))/this.kb.getValue("energy_threshold")) * (1 / (1 + (this.kb.agentsVicinity().length == 0 ? 0 : 1) )));
                    else
                        return 0
                }
            ],
            execute: function () {
                const bedBlock = this.kb.getValue("bed")
                this.locateExactBlock(bedBlock)
                this.sleep()
            }
        }, {
            name: "Eat",
            variables: {
                necessary : ["hunger", "hunger_threshold"],
                optional: ["favourite_food"]
            },
            salience: [
                function() {
                    return Math.max(0,(this.kb.getValue("hunger") - this.kb.getValue("hunger_threshold"))/this.kb.getValue("hunger"));
                },
                function() {
                    return Math.min(0, Math.max(1,(this.kb.wasPerceivedInventory(this.kb.getValue("favourite_food")) * 2 * (this.kb.getValue("hunger") - this.kb.getValue("hunger_threshold"))/this.kb.getValue("hunger"))));
                }
            ],
            execute: function () {
                this.locateBlockInBBox(this.restaurant)
                this.eat()
            }
        },{
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
        }, {
            name: "Socialize",
            variables:{
                necessary: [],
                optional: [],
            },
            salience: [
                function(){
                    return 0.1
                },
                function(){
                    if(this.kb.isFriendInVicinity()){
                        return 0.7
                    }
                    else{
                        return 0
                    }
                }
            ],
            execute: function(){
                this.locateBlockInBBox(this.socialPlace)
                this.socialize()
            }
        }
    ],
    agents: [
        {
            name: "Jane Doe",
            identities: ["Eat","Sleep","Socialize"],
            knowledge_base: new KB({"hunger": 200, "hunger_threshold": 500,
                                    "favourite_food": "carrot", "energy": 1000,
                                    "energy_threshold": 300, "bed": new Vec3(-176,72,211),
                                    "friend_list": ["Jane Doe"]
                                }),
        }, {
            name: "John Doe",
            identities: ["Lumberjack","Sleep","Socialize"],
            knowledge_base: new KB({"energy": 1000, "energy_threshold": 400,
                                    "wood_stock": 0, "favourite_wood": "oak_log",
                                    "bed": new Vec3(-159,72,223), "friend_list": ["John Doe"]
                                }),
        }
    ],
    places: {
        houses: [
            {
                agents : ["Jane Doe"],
                bbox : new BoundingBox(new Vec3(-169,71,206), new Vec3(-182,77,216)),
                beds : [new Vec3(-176,72,211)],
            },{
                agents : ["John Doe"],
                bbox : new BoundingBox(new Vec3(-164,71,217), new Vec3(-154,78,228)),
                beds : [new Vec3(-159,72,223)],
            }
        ],
        forest: new BoundingBox(new Vec3(-137, 72, 251), new Vec3(-116, 74, 271)),
        socialPlace : new BoundingBox(new Vec3(-140,73,213), new Vec3(-136,73,217)),
        restaurant: new BoundingBox(new Vec3(-163, 72, 241), new Vec3(-165, 72, 251))
    }
}

module.exports = config;
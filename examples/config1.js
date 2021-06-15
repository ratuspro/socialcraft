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
                    return Math.max(0,((this.kb.getValue("energy_threshold") - this.kb.getValue("energy"))/this.kb.getValue("energy_threshold")) * (1 / (1 + this.kb.hasAgentsVicinity())) * ((1 + this.kb.isNightTime() / 2)));
                }
            ],
            execute: function () {
                const bedBlock = this.kb.getValue("bed")
                this.locateExactBlock(bedBlock)
                this.sleep()
                this.kb.set_kb('energy', 1000)
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
                    return this.kb.wasPerceivedInventory(this.kb.getValue("favourite_food")) * 0.9;
                }
            ],
            execute: function () {
                this.eat()
                this.kb.set_kb('hunger', 0)
            }
        },{
            name: "Lumberjack",
            variables: {
                necessary: ["wood_stock"],
                optional : ["favourite_wood"]
            },
            salience: [
                function() {
                    return (this.kb.getValue("wood_stock") > 0 ? 0 : 0.6);
                },
                function() {
                    return this.kb.wasPerceivedVicinity(this.kb.getValue("favourite_wood")) * 0.9;
                }
            ],
            execute: function () {
                const woodBlocks = [35, 36, 37, 38, 39, 40, 46, 41, 42, 43, 44, 45] /*wood blocks ids*/
                this.locateBlockInArea(woodBlocks, this.get_Forest)
                this.digBlock(woodBlocks, this.get_Forest)
                this.kb.set_kb('energy', this.kb.getValue('energy') - 30)
            }
        }
    ],
    agents: [
        {
            name: "Jane Doe",
            identities: ["Eat","Sleep"],
            knowledge_base: new KB({"hunger": 200, "hunger_threshold": 500,
                                    "favourite_food": "carrot", "energy": 1000,
                                    "energy_threshold": 300, "bed": new Vec3(-176,72,211)
                                }),
        }, {
            name: "John Doe",
            identities: ["Lumberjack","Sleep"],
            knowledge_base: new KB({"energy": 1000, "energy_threshold": 400,
                                    "wood_stock": 0, "favourite_wood": "oak_log",
                                    "bed": new Vec3(-159,72,223),
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
        forest: new BoundingBox(new Vec3(-137, 72, 251), new Vec3(-116, 74, 271))
    }
}

module.exports = config;
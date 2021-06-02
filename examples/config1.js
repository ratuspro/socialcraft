/****** CONFIG 1 ******/
/* Identities:
/* - Sleep: when the agents energy levels goes beneath a threshold, the agent goes to sleep.
/* - Eat: when the agent sees its favourite food, it eats the food. Or, when the agent hunger passes a certain threshold, the agent eats something.
/* - Lumberjack: when the agent sees his favourite wood, chops it of and saves it. Or, when the agent has a low stock of wood, chops and collects any wood.
/* Agents:
/* - Jane Doe: has the identities Eat and Sleep and her favourite food is carrots
/* - John Doe: has the identities Sleep and Lumberjack and his favourite wood is oak
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
                    return Math.max(0,(this.kb.getValue("energy_threshold") - this.kb.getValue("energy"))/this.kb.getValue("energy_threshold"));
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
                    return this.kb.wasPerceived(this.kb.getValue("favourite_food")) * 0.9;
                }
            ],
            execute: function () {
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
                    return (this.kb.getValue("wood_stock") > 0 ? 0 : 0.5);
                },
                function() {
                    return this.kb.wasPerceived(this.kb.getValue("favourite_wood")) * 0.9;
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
            name: "Jane Doe",
            identities: ["Eat","Sleep"],
            knowledge_base: new KB({"hunger": 100, "hunger_threshold": 60,
                                    "favourite_food": "carrot", "energy": 50,
                                    "energy_threshold": 30, "bed": new Vec3(-176,72,211)
                                }),
        }, {
            name: "John Doe",
            identities: ["Lumberjack","Sleep"],
            knowledge_base: new KB({"energy": 50, "energy_threshold": 30,
                                    "wood_stock": 0, "favourite_wood": "oak",
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
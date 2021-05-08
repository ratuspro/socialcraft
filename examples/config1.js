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

 const config = {
    identities: [
        {
            name: "Sleep",
            variables: {
                necessary : ["energy", "energy_threshold"],
                optional: []
            },
            salience: [
                function(KB) {
                    return Math.max(0,(KB.getValue("energy_threshold") - KB.getValue("energy"))/KB.getValue("energy_threshold"));
                }
            ],
            execute: function (KB) {
                //TODO: Implement Game Logic
            }
        }, {
            name: "Eat",
            variables: {
                necessary : ["hunger", "hunger_threshold"],
                optional: ["favourite_food"]
            },
            salience: [
                function(KB) {
                    return Math.max(0,(KB.getValue("hunger") - KB.getValue("hunger_threshold"))/KB.getValue("hunger"));
                },
                function(KB) {
                    return KB.wasPerceived(KB.getValue("favourite_food")) * 1.0;
                }
            ],
            execute: function (KB) {
                //TODO: Implement Game Logic
            }
        },{
            name: "Lumberjack",
            variables: {
                necessary: ["wood_stock"],
                optional : ["favourite_wood"]
            },
            salience: [
                function(KB) {
                    return (KB.getValue("wood_stock") > 0 ? 0 : 0.5);
                },
                function(KB) {
                    return KB.wasPerceived(KB.getValue("favourite_oak")) * 1.0;
                }
            ],
            execute: function (KB) {
                //TODO: Implement Game Logic
            }
        }
    ],
    agents: [
        {
            name: "Jane Doe",
            identities: ["Eat","Sleep"],
            knowledge_base:{
                "hunger": 100,
                "hunger_threshold": 60,
                "favourite_food": "carrot",
                "energy": 50,
                "energy_threshold": 30,
                getValue: function(varName) {
                    if(varName in this) return this[varName]
                    else return null
                },
                wasPerceived: function(varName){
                    return 1 //como é que integro isto com as percecoes dos bots?
                },
            },
        }, {
            name: "John Doe",
            identities: ["Lumberjack","Sleep"],
            knowledge_base:{
                "energy": 50,
                "energy_threshold": 30,
                "wood_stock": 0,
                "favourite_wood": "oak",
                getValue: function(varName) {
                    if(varName in this) return this[varName]
                    else return null
                },
                wasPerceived: function(varName){
                    return 1 //como é que integro isto com as percecoes dos bots?
                },
            }
        }
    ],
    houses: [
        {
            agents : ["Jane Doe"],
            bbox : new BoundingBox(new Vec3(-169,71,206), new Vec3(-182,77,216)),
            beds : [new Vec3(-176,72,211)], //devia estar na KB dos agentes?
        }
    ]
}

module.exports = config;
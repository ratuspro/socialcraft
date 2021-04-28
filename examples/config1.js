/****** CONFIG 1 ******/
/* Identities:
/* - Sleep: when the agents energy levels goes beneath a threshold, the agent goes to sleep.
/* - Eat: when the agent sees its favourite food, it eats the food. Or, when the agent hunger passes a certain threshold, the agent eats something.
/* - Lumberjack: when the agent sees his favourite wood, chops it of and saves it. Or, when the agent has a low stock of wood, chops and collects any wood.
/* Agents:
/* - Jane Doe: has the identities Eat and Sleep and her favourite food is carrots
/* - John Doe: has the identities Sleep and Lumberjack and his favourite wood is oak
*/

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
                    return Math.min(0,KB.getValue("energy_threshold") - KB.getValue("energy"));
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
                    return Math.min(0,KB.getValue("hunger_threshold") - KB.getValue("hunger"));
                },
                function(KB) {
                    return KB.wasPerceived(KB.getValue("favourite_food") * 1.0);
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
                    return (KB.getValue("wood_stock") > 0 ? 0.5 : 0);
                },
                function(KB) {
                    return KB.wasPerceived(KB.getValue("favourite_oak") * 0.8);
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
            knowledge_base: [
                {"hunger": 100},
                {"hunger_threshold": 60},
                {"favourite_food": "carrot"},
                {"energy": 50},
                {"energy_threshold": 30},
            ]
        }, {
            name: "John Doe",
            identities: ["Lumberjack","Sleep"],
            knowledge_base: [
                {"energy": 50},
                {"energy_threshold": 30},
                {"wood_stock": 0},
                {"favourite_wood": "oak"}
            ]
        }
    ]
}

module.exports = config;
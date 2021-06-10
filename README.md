# SocialCraft ReadMe

**SocialCraft** is a tool that enables the easy launching of agents (or bots) into Minecraft with the usage of a single configuration file. Its main use is to help level and game designers with their authoring process through various abstractions, only needing the creation of the configuration file.

# Hierarchy
**SocialCraft**'s hierarchy is as shown in the following diagram
```
SocialCraft
|___examples/
|	|
|	|___configFile1.js
|	|___...
|	|___configFileN.js
|	
|___agent_process.js
|___agent.js
|___BoundingBox.js
|___CLI.js
|___GoalNoTrespassing.js
|___index_workers.js
|___KB.js
|___utils.js
```

# How to run the program
The first thing you will have to do to run the program is to have **Node.js** installed. You can find the most recent version in [the official website](https://nodejs.org/en/).
At the time of creating the tool, **Mineflayer**, the tool used to customize the agents supported the versions of Minecraft up to version `1.16`, so we will also need a **server that runs in that version of the game**. `Spigot` was the one used during development due to the accessibility of plugins and ease-of-use, but it is crucial that in the ***server.properties*** file, the `online-mode` value is set to `false`, otherwise the bots will not be able to connect.
Once those things are done, open up a terminal in the root of the project and type: `node CLI.js`


## How to interact with it

The main entry points to **SocialCraft** are the configuration files. It is by creating new files that you can make more agents, more identities or actions, define more interest places in the world (such as houses or workplaces) and even change the server properties. It is important that the same structure that was used in ***config1.js*** is followed.
However, the addition of a new file **does not suffice**. We will now take a look at how you launch the program and what you need to change to achieve what you want.

### Interaction pre-runtime and during runtime

By typing the instruction `node CLI.js`, we have launched a *CLI* (command line interface) and various subprocesses, each one handling one agent. During runtime, it is possible to interact with the agents by typing a message with the following format: `(AGENT_NAME) | (KB_PROPERTY) (NEW_VALUE)`, which will send the message to the the agent `AGENT_NAME` if it exists, changing its `KB_PROPERTY` value to `NEW_VALUE`, if the said property also exists.
Pre-runtime is where the bulk of the changes need to be made. After the creation a new config file, the line `const  main = fork("./index_workers.js", ["./examples/config1.js"])` in the file `CLI.js` should be changed to have the correct name of the configuration file. In the `agent_process.js` file there is also a line that can be changed in order to try and debug the behavior of the agents: `setTimeout(()=>agent.start(), 1000)` - this line starts the function `agent.start()` after 1 second, and it could be useful to call maybe some other function.
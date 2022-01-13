# SocialCraft

## Usage

To use the socialcraft library, the user needs to have a Docker-Engine (local or remote) and a Minecraft server (local or remote).

### Create an Agent Manager
```
agent_manager = AgentManager(docker_url="...", minecraft_server_url="...")
```

### Create an agent template
```
agent_blueprint = manager.create_blueprint(source_path)
```

### Create an agent instance based on a template
```
agent = agent_manager.create_agent("Maria1", agent_blueprint)
```

### Deploy the agent into the Minecraft Server
```
agent.deploy() 
```
or 
```
agent_manager.deploy_agent(agent.name)
```

## Deploy Minecraft Server

### Using docker

```
docker run -d -p 25565:25565 -e MODE=creative -e MAX_WORLD_SIZE=1 -e GENERATE_STRUCTURES=false -e SPAWN_ANIMALS=false -e SPAWN_MONSTERS=false -e SPAWN_NPCS=false -e LEVEL_TYPE=flat -e EULA=TRUE -e ONLINE_MODE=FALSE -e MAX_PLAYERS=50 -e VERSION=1.17 --name mc itzg/minecraft-server
```

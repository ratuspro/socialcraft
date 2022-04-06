const pathfinder = require("mineflayer-pathfinder")
const mineflayer = require("mineflayer")
require('dotenv').config();

class SocialcraftHandler {
    constructor() {

        this.botConfig = {}

        if ("MINECRAFT_USERNAME" in process.env) {
            this.botConfig["username"] = process.env.MINECRAFT_USERNAME
        } else if ("AGENT_NAME" in process.env) {
            this.botConfig["username"] = process.env.AGENT_NAME
        }


        this.botConfig["host"] = "MINECRAFT_HOST" in process.env ? process.env.MINECRAFT_HOST : "localhost"
        this.botConfig["port"] = "MINECRAFT_PORT" in process.env ? process.env.MINECRAFT_PORT : "25565"
        this.botConfig["password"] = "MINECRAFT_PORT" in process.env ? process.env.MINECRAFT_PASSWORD : ""
        this.botConfig["version"] = "MINECRAFT_VERSION" in process.env ? process.env.MINECRAFT_VERSION : False
        this.botConfig["brooker_host"] = "RABBITMQ_HOST" in process.env ? process.env.RABBITMQ_HOST : "localhost"
        this.botConfig["brooker_port"] = "RABBITMQ_PORT" in process.env ? process.env.RABBITMQ_PORT : 5672
        this.botConfig["brooker_virtual_host"] = "RABBITMQ_VIRTUAL_HOST" in process.env ? process.env.RABBITMQ_VIRTUAL_HOST : "  "

        console.log("### Agent Setup Configuration:")
        console.log(`Minecraft Host: ${this.botConfig['host']}`)
        console.log(`Minecraft Port: ${this.botConfig['port']}`)
        console.log(`Minecraft Version: ${this.botConfig['version']}`)
        console.log(`Minecraft Username: ${this.botConfig['username']}`)
        console.log(`Minecraft Password: ${this.botConfig['username']}`)
        console.log(`Agent Name: ${this.botConfig['username']}`)
        console.log(`Brooker Host: ${this.botConfig['brooker_host']}`)
        console.log(`Brooker Port: ${this.botConfig['brooker_port']}`)
        console.log(`Brooker Virtual Host: ${this.botConfig['brooker_virtual_host']}`)
    }

    connect() {
        console.log("Creating Bot...")
        this.bot = mineflayer.createBot(this.botConfig)

        console.log("Loading plugins...")
        this.bot.loadPlugin(pathfinder.pathfinder)

        console.log("Waiting for bot to spawn...")
        this.bot.on("spawn", () => {
            console.log("Bot sucessfully spawned!")

            console.log("Setting up mineflayer-pathfinder...")
            this.mcData = require("minecraft-data")(this.bot.version)
            movements = new pathfinder.Movements(this.bot, this.mcData)
            movements.allowSprinting = false
            movements.canDig = false
            this.bot.pathfinder.setMovements(movements)

            console.log("Waiting for pathfinder...")
            console.log("Pathfinder ready!")
        })
    }

    name() {
        return this.botConfig["username"]
    }

    get_bot() {
        if (this.bot == null) {
            this.logger.error("Trying to get bot without establishing a connection first")
        }
        return this.bot
    }

    has_init_env_variable(name) {
        return "SOCIALCRAFT_INIT_${name}" in process.env
    }

    get_init_env_variable() {
        return process.env["SOCIALCRAFT_INIT_${name}"]
    }
}
module.exports = SocialcraftHandler;
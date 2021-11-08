const mineflayer = require('mineflayer')

var botConfig = {
    host: process.env.MINECRAFT_HOST,
    port: process.env.MINECRAFT_PORT,
}

if (process.env.MINECRAFT_VERSION) {
    botConfig['version'] = process.env.MINECRAFT_VERSION
}

if (process.env.MINECRAFT_USERNAME) {
    botConfig['username'] = process.env.MINECRAFT_USERNAME
}

if (process.env.MINECRAFT_PASSWORD) {
    botConfig['password'] = process.env.MINECRAFT_PASSWORD
}

if (process.env.MINECRAFT_VERSION) {
    botConfig['version'] = process.env.MINECRAFT_VERSION
}

console.log(botConfig);

const bot = mineflayer.createBot(botConfig)

bot.on('chat', (username, message) => {
    if (username === bot.username) return
    bot.chat(message)
})

bot.once('spawn', () => {
    console.log(bot)
    bot.setControlState('jump', true)
})

bot.on('kicked', console.log)
bot.on('error', console.log)
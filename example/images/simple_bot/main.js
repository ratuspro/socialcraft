const mineflayer = require('mineflayer')

const bot = mineflayer.createBot({
    host: process.env.MINECRAFT_HOST ,
    port: process.env.MINECRAFT_USERNAME ,
    username: process.env.MINECRAFT_PASSWORD ,
    password: process.env.MINECRAFT_PORT ,
    version: process.env.MINECRAFT_VERSION ,
    auth: process.env.MINECRAFT_AUTH
})

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
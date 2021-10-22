const mineflayer = require('mineflayer')

const bot = mineflayer.createBot({
    host: process.env.SOCIALCRAFT_MINECRAFTSERVER_URL || 'localhost',
    port: process.env.SOCIALCRAFT_MINECRAFTSERVER_PORT || 25565,
    username: process.env.SOCIALCRAFT_MINECRAFTSERVER_USER || 'email@example.com',
    password: process.env.SOCIALCRAFT_MINECRAFTSERVER_PASSWORD || '12345678',
    version: process.env.SOCIALCRAFT_MINECRAFTSERVER_VERSION || false,
    auth: process.env.SOCIALCRAFT_MINECRAFTSERVER_AUTH || 'mojang'
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
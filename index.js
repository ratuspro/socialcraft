const {exec}= require('child_process')
const fs = require('fs')

const configPath = './examples/config1.js'
const configuration = require(configPath)

const packagePath = './package.json'

let rawData = fs.readFileSync(packagePath)
let jsonString = JSON.parse(rawData)

jsonString["scripts"]["start"] = "run-s "
for(var i=0; i<configuration["agents"].length; i++){
    jsonString["scripts"]["start"] += "tab:launch:" + configuration["agents"][i]["name"] + " "
    jsonString["scripts"]["launch:"+ configuration["agents"][i]["name"]] = "node agents.js " +  configuration["agents"][i]["name"] // THE COMMAND EACH BOT RUNS! HAS TO THEN CALL THE SCRIPT THAT CONTROLS THEM
    jsonString["scripts"]["tab:launch:"+ configuration["agents"][i]["name"]] = "wttab -t " + configuration["agents"][i]["name"] + " npm run " + "launch:"+configuration["agents"][i]["name"]
}
jsonString["scripts"]["start"] = jsonString["scripts"]["start"].trimEnd()

let data = JSON.stringify(jsonString, null, 2)
fs.writeFileSync(packagePath, data)

exec("npm start", {'shell': 'powershell.exe'})
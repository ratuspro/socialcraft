const { fork } = require('child_process');

const readline = require('readline');
const colours = require('./utils')

const main = fork("./index_workers.js", ["./examples/config1.js"])
 

main.on('message', message => {
    //Receive message from child
});

function askQuestion(query) {
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout,
    });

    return new Promise(resolve => rl.question(query, ans => {
        rl.close();
        resolve(ans);
    }))
}

setTimeout(async() => {
    while(true){
        const ans = await askQuestion(colours.blue + "Write any command " + colours.normal + "[" + colours.green + "FORMAT: (Target)|(KB Property) (Value)" + colours.normal + "]: ")
        if(ans){
            const command = ans.split('|')
            if(command.length == 2){
                main.send({target:command[0].trimEnd().trimStart(), command:command[1].trimEnd().trimStart()}) //////////////////// Send message to the fork process
            }
            else{
                console.error(colours.red, "Poorly formatted input.")
            }
        } 
    }
}, 1000)
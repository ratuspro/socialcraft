const { fork } = require('child_process');

const readline = require('readline');

const main = fork("./index_workers.js", ["./examples/config1.js"])

main.on('message', message => {
  console.log('message from child:', message);  // Receiving message from fork process
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

setTimeout(async() => 
    {
        while(true){
            const ans = await askQuestion("Write any command [FORMAT : (target) | (command)]: ")
            if(ans){
                const command = ans.split('|')
                if(command.length == 2){
                    main.send({target:command[0].trimEnd().trimStart(), command:command[1].trimEnd().trimStart()}) //////////////////// Send message to the fork process
                }
            }
        }
    }
, 1000)
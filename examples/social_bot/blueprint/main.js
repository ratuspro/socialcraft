const mineflayer = require('mineflayer')
const socialcraft = require('./socialcraft.js')

socialcraft.todo()

var botConfig = {
    host: process.env.MINECRAFT_HOST,
    port: process.env.MINECRAFT_PORT,
}

if (process.env.MINECRAFT_VERSION) {
    botConfig['version'] = process.env.MINECRAFT_VERSION
}

if (process.env.MINECRAFT_USERNAME) {
    botConfig['username'] = process.env.MINECRAFT_USERNAME
} else if (process.env.AGENT_NAME) {
    botConfig['username'] = process.env.AGENT_NAME
}

if (process.env.MINECRAFT_PASSWORD) {
    botConfig['password'] = process.env.MINECRAFT_PASSWORD
}

if (process.env.MINECRAFT_VERSION) {
    botConfig['version'] = process.env.MINECRAFT_VERSION
}


const bot = mineflayer.createBot(botConfig)


// Load your dependency plugins.
bot.loadPlugin(require('mineflayer-pathfinder').pathfinder);

// Import required behaviors.
const {
    StateTransition,
    BotStateMachine,
    EntityFilters,
    BehaviorFollowEntity,
    BehaviorLookAtEntity,
    BehaviorGetClosestEntity,
    NestedStateMachine } = require("mineflayer-statemachine");


bot.on('chat', (username, message) => {
    if (username === bot.username) return
    bot.chat(message)
})

// Possible Plans
bot.once('spawn', () => {
    
    const targets = {};

    // Create our states
    const getClosestPlayer = new BehaviorGetClosestEntity(bot, targets, EntityFilters().PlayersOnly);
    const lookAtPlayer = new BehaviorLookAtEntity(bot, targets);
    const greetPlayer = Math.random() > 0.5 ? new BehaviourJumpingGreetPlayer(bot, targets) : new BehaviourCrounchGreetPlayer(bot, targets);


    // Create our transitions
    const transitions = [

        new StateTransition({
            parent: getClosestPlayer,
            child: lookAtPlayer,
            shouldTransition: () => true,
        }),

        new StateTransition({
            parent: lookAtPlayer,
            child: greetPlayer,
            shouldTransition: () => lookAtPlayer.distanceToTarget() <= 5,
        }),

        new StateTransition({
            parent: greetPlayer,
            child: getClosestPlayer,
            shouldTransition: () => greetPlayer.isGreetingCompleted(),
        }),

    ];

    // Now we just wrap our transition list in a nested state machine layer. We want the bot
    // to start on the getClosestPlayer state, so we'll specify that here.
    const rootLayer = new NestedStateMachine(transitions, getClosestPlayer);
    
    // We can start our state machine simply by creating a new instance.
    new BotStateMachine(bot, rootLayer);
    
})

bot.on('kicked', console.log)
bot.on('error', console.log)



//Implement this
const BehaviourWaitForNearbyEntity = (function(){

    const maxJumps = 2;
    function BehaviourJumpingGreetPlayer(bot, targets)
    {
        this.bot = bot;
        this.active = false;
        this.stateName = 'GreetOther';
        this.targets = targets;
        this.counter = 0;
        this.alreadyGreeted = false;
    }

    BehaviourJumpingGreetPlayer.prototype.reset = function () {
        this.counter = 0;
    };

    BehaviourJumpingGreetPlayer.prototype.onStateEntered = function () {
        if(this.alreadyGreeted){
            return;
        }
        this.reset();
        this.bot.setControlState("jump", true);
        
    };
    BehaviourJumpingGreetPlayer.prototype.onStateExited = function () {
        console.log(`${bot.username} has left the ${this.myStateName} state.`);
        this.bot.setControlState("jump", false);
    };

    BehaviourJumpingGreetPlayer.prototype.update = function () {
        if(!this.bot.entity.onGround){
            this.bot.setControlState("jump", false);
        }else{
            this.counter +=1;
            if(this.counter <= maxJumps){
                this.bot.setControlState("jump", true);
            }
        }
    };

    BehaviourJumpingGreetPlayer.prototype.isGreetingCompleted = function(){
        const entity = this.targets.entity;

        if(this.alreadyGreeted || this.counter >= maxJumps && this.bot.entity.onGround){
            this.alreadyGreeted = true;
            return true;
        }

        return false;
    }

    return BehaviourJumpingGreetPlayer;
}());



const BehaviourJumpingGreetPlayer = (function(){

    const maxJumps = 2;
    function BehaviourJumpingGreetPlayer(bot, targets)
    {
        this.bot = bot;
        this.active = false;
        this.stateName = 'GreetOther';
        this.targets = targets;
        this.counter = 0;
        this.alreadyGreeted = false;
    }

    BehaviourJumpingGreetPlayer.prototype.reset = function () {
        this.counter = 0;
    };

    BehaviourJumpingGreetPlayer.prototype.onStateEntered = function () {
        if(this.alreadyGreeted){
            return;
        }
        this.reset();
        this.bot.setControlState("jump", true);
        
    };
    BehaviourJumpingGreetPlayer.prototype.onStateExited = function () {
        console.log(`${bot.username} has left the ${this.myStateName} state.`);
        this.bot.setControlState("jump", false);
    };

    BehaviourJumpingGreetPlayer.prototype.update = function () {
        if(!this.bot.entity.onGround){
            this.bot.setControlState("jump", false);
        }else{
            this.counter +=1;
            if(this.counter <= maxJumps){
                this.bot.setControlState("jump", true);
            }
        }
    };

    BehaviourJumpingGreetPlayer.prototype.isGreetingCompleted = function(){
        const entity = this.targets.entity;

        if(this.alreadyGreeted || this.counter >= maxJumps && this.bot.entity.onGround){
            this.alreadyGreeted = true;
            return true;
        }

        return false;
    }

    return BehaviourJumpingGreetPlayer;
}());


const BehaviourCrounchGreetPlayer = (function(){

    const maxCrouchs = 2;
    const crounchingTicks = 4;
    const idleTicks = 6;
    function BehaviourCrounchGreetPlayer(bot, targets)
    {
        this.bot = bot;
        this.active = false;
        this.stateName = 'GreetOther';
        this.targets = targets;
        this.counter = 0;
        this.crounchingTimer = -1;
        this.idleTimer = -1;
        this.alreadyGreeted = false;
    }

    BehaviourCrounchGreetPlayer.prototype.reset = function () {
        this.counter = 0;
        this.crounchingTimer = -1;
        this.idleTimer = -1;
    };

    BehaviourCrounchGreetPlayer.prototype.onStateEntered = function () {
        if(this.alreadyGreeted){
            return;
        }

        console.log(`${bot.username} has entered the ${this.myStateName} state.`);
        this.bot.setControlState("sneak", true);
        this.crounchingTimer = crounchingTicks;
    };
    BehaviourCrounchGreetPlayer.prototype.onStateExited = function () {
        console.log(`${bot.username} has left the ${this.myStateName} state.`);
        this.bot.setControlState("sneak", false);
    };

    BehaviourCrounchGreetPlayer.prototype.update = function () {
        if(this.bot.getControlState("sneak")){
            this.crounchingTimer -= 1;

            if(this.crounchingTimer <= 0){
                this.bot.setControlState("sneak", false);
                this.idleTimer = idleTicks;
                this.counter += 1;
            }
        }else{
            this.idleTimer -= 1;

            if(this.idleTimer <= 0 && this.counter <=maxCrouchs){
                this.bot.setControlState("sneak", true);
                this.crounchingTimer = crounchingTicks;
            }
        }

    };

    BehaviourCrounchGreetPlayer.prototype.isGreetingCompleted = function(){
        if(this.alreadyGreeted || this.counter >= maxCrouchs && this.bot.getControlState('sneak', false)){
            this.alreadyGreeted = true;
            return true;
        }

        return false;
    }

    return BehaviourCrounchGreetPlayer;
}());
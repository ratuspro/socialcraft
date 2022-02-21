from javascript import eval_js


def perceive_blocks(bot):
    output = eval_js(
        """
        const vec3 = require('vec3')
        let eyes_position = bot.entity.position
        let min_pitch = -4
        let max_pitch = 4
        let min_yaw = -9
        let max_yaw = 9

        let pitchs = []
        let yaws = []

        for (let index = min_yaw; index <= max_yaw; index++) { 
            let yaw = bot.entity.yaw + index * 0.125
            yaws.push([-Math.sin(yaw), -Math.cos(yaw)])
        }

        for (let index = min_pitch; index <= max_pitch; index++) {
            let pitch = bot.entity.pitch + index * 0.125
            pitchs.push(Math.sin(pitch))
        }

        let blocks_position = {}
        let blocks_by_type = {}

        
        for (let i_yaw = 0; i_yaw < yaws.length; i_yaw++) {
            const yaw = yaws[i_yaw];
            for (let i_pitch = 0; i_pitch < pitchs.length; i_pitch++) {
            const pitch = pitchs[i_pitch];
            let bot_facing_direction = vec3(yaw[0], pitch, yaw[1]).normalize()
            let block = bot.world.raycast(eyes_position, bot_facing_direction, 15)
            if(block != null && !(block.position in blocks_position)){
                blocks_position[block.position] = block.displayName
                if(!(block.displayName in blocks_by_type)){
                blocks_by_type[block.displayName] = []
                }
                blocks_by_type[block.displayName].push(block.position)
            }
            }
        }
        return [blocks_position, blocks_by_type]
        """
    )
    return output


def perceive_players(bot):

    output = eval_js(
        """
        let players = []

        for (const entity of Object.values(bot.entities)) {
            if (entity === bot.entity || entity.type != 'player') {
            continue
            }

            if(bot.entity.position.distanceSquared(entity.position) < 100){
            players.push(entity)
            } 
        }

        return players
    """
    )

    return output

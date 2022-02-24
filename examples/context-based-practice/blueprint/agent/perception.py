from typing import Tuple, Dict, List
from javascript import eval_js
from vector3 import Vector3
from practices import Player, Block


def perceive_blocks(bot) -> Dict[Vector3, Block]:
    blocks_by_position = {}
    eval_js(
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

        
        for (let i_yaw = 0; i_yaw < yaws.length; i_yaw++) {
            const yaw = yaws[i_yaw];
            for (let i_pitch = 0; i_pitch < pitchs.length; i_pitch++) {
                const pitch = pitchs[i_pitch];
                let bot_facing_direction = vec3(yaw[0], pitch, yaw[1]).normalize()
                let block = bot.world.raycast(eyes_position, bot_facing_direction, 15)
                if(block != null && !(block.position in blocks_by_position)){
                    blocks_by_position[block.position] = block.displayName
                }
            }
        }
    """
    )
    output = {}
    for block, value in blocks_by_position.items():
        position = Vector3(tuple(map(int, block.replace("(", "").replace(")", "").split(", "))))
        block_obj = Block(value, position)
        output[position] = block_obj
    return output


def perceive_players(bot) -> List[Player]:
    players = []
    eval_js(
        """
        for (const entity of Object.values(bot.entities)) {
            if (entity === bot.entity || entity.type != 'player') {
            continue
            }

            if(bot.entity.position.distanceSquared(entity.position) < 100){
                await players.append(entity)
            } 
        }
    """
    )

    output = []
    for player in players:
        output.append(Player(player.username, Vector3(player.position)))
    return output

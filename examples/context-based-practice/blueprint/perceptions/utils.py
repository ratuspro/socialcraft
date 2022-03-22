from datetime import datetime
from typing import Tuple, Dict, List
from javascript import eval_js
from vector3 import Vector3
from .models import Player, Block, Perception


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
                await players.append([entity.username, entity.position.x,entity.position.y,entity.position.z])
            } 
        }
    """
    )

    output = []
    for player in players:
        output.append(Player(player[0], Vector3(player[1], player[2], player[3])))
    return output


def perceive_world_state(bot) -> List[Perception]:
    perceptions = []
    time_of_day = int(bot.time.timeOfDay)
    is_day = bool(bot.time.isDay)
    perceptions.append(Perception("TIME", time_of_day / 24000, None))
    perceptions.append(Perception("ISDAY", 1 if is_day else 0, None))
    perceptions.append(Perception("ISNIGHT", 1 if not is_day else 0, None))
    perceptions.append(Perception("RAIN", bot.rainState, None))
    perceptions.append(Perception("THUNDER", bot.thunderState, None))
    return perceptions

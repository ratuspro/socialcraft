const {Vec3} = require('vec3')
const Goal = require('mineflayer-pathfinder').goals.Goal

function distanceXZ (dx, dz) {
    dx = Math.abs(dx)
    dz = Math.abs(dz)
    return Math.abs(dx - dz) + Math.min(dx, dz) * Math.SQRT2
  }

class GoalNoTespassing extends Goal{
    constructor (x, y, z, boundingBoxes) {
        super()
        this.x = Math.floor(x)
        this.y = Math.floor(y)
        this.z = Math.floor(z)
        this.bboxes = boundingBoxes
      }
    
      heuristic (node) {
        const dx = this.x - node.x
        const dy = this.y - node.y
        const dz = this.z - node.z
        let heuristic = distanceXZ(dx, dz) + Math.abs(dy < 0 ? dy + 1 : dy)
    
        for(var neighbourHouse of this.bboxes){
            if (neighbourHouse.inBBox(new Vec3(node.x,node.y,node.z))){
                heuristic += 9999
            }
        }
    
        return heuristic
      }
    
      isEnd (node) {
        const dx = node.x - this.x
        const dy = node.y - this.y
        const dz = node.z - this.z
        return Math.abs(dx) + Math.abs(dy < 0 ? dy + 1 : dy) + Math.abs(dz) === 1
      }
}

module.exports = {GoalNoTespassing}
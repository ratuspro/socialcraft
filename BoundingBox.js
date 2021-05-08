class BoundingBox{
    constructor(p1, p2){
        this.xMin = this.maxMinAxis("min", "x", p1, p2)
        this.xMax = this.maxMinAxis("max", "x", p1, p2)
        this.yMin = this.maxMinAxis("min", "y", p1, p2)
        this.yMax = this.maxMinAxis("max", "y", p1, p2)
        this.zMin = this.maxMinAxis("min", "z", p1, p2)
        this.zMax = this.maxMinAxis("max", "z", p1, p2)
    }

    maxMinAxis(maxOrMin, axis, vec1, vec2){
        if(maxOrMin == "max"){
            if(axis == "x"){
                return (vec1.x > vec2.x ? vec1.x : vec2.x)
            }
            if(axis == "y"){
                return (vec1.y > vec2.y ? vec1.y : vec2.y)
            }
            if(axis == "z"){
                return (vec1.z > vec2.z ? vec1.z : vec2.z)
            }
        }
        else if(maxOrMin == "min"){
            if(axis == "x"){
                return (vec1.x < vec2.x ? vec1.x : vec2.x)
            }
            if(axis == "y"){
                return (vec1.y < vec2.y ? vec1.y : vec2.y)
            }
            if(axis == "z"){
                return (vec1.z < vec2.z ? vec1.z : vec2.z)
            }
        }
    }

    inBBox(point){
        if(point.x >= this.xMin && point.x <= this.xMax){
            if(point.y >= this.yMin && point.y <= this.yMax){
                if(point.z >= this.zMin && point.z <= this.zMax){
                    return true
                }
            }
        }
        return false
    }
}

module.exports = BoundingBox
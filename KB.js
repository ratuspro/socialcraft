class KB{
    constructor(data){
        this.knowledge_base = data
    }

    get get_kb(){
        return this.knowledge_base
    }

    set_kb(prop, value){
        this.knowledge_base[prop] = value
    }

    inKB(varName){
        if(varName in this.knowledge_base){
            return true
        }
        else{
            return false
        }
    }
    getValue(varName){
        if(varName in this.knowledge_base) return this.knowledge_base[varName]
        else return null
    }
    wasPerceived(){
        return 1
    }
}

module.exports = KB
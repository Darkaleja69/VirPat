package furhatos.app.prueba

import furhatos.app.prueba.flow.Init
import furhatos.flow.kotlin.Flow
import furhatos.skills.Skill

class PruebaSkill : Skill() {
    override fun start() {
        Flow().run(Init)
    }
}

fun main(args: Array<String>) {
    Skill.main(args)
}

package furhatos.app.prueba.flow.main

import furhatos.app.prueba.flow.Parent
import furhatos.flow.kotlin.State
import furhatos.flow.kotlin.furhat
import furhatos.flow.kotlin.onResponse
import furhatos.flow.kotlin.state
import furhatos.app.prueba.flow.getDialogCompletion
import furhatos.gestures.Gestures
import furhatos.nlu.EnumEntity
import furhatos.nlu.Intent
import furhatos.nlu.common.Goodbye
import furhatos.nlu.common.No
import furhatos.nlu.common.Yes
import furhatos.util.Language
import furhatos.nlu.common.Number
import furhatos.util.Gender
import org.json.JSONObject
import java.io.File
import furhatos.app.prueba.flow.data

val Greeting: State = state(Parent) {
    val historial: String = data["historial"] as? String ?: ""
    onEntry {
        furhat.ask("Buenos días, doctor")
    }

    onResponse<Goodbye> {
        furhat.say("Adiós")
        goto(Idle)
    }

    onResponse{
        furhat.say(async = true) {
            +Gestures.GazeAway
        }
        val robotResponse = call {
            getDialogCompletion(historial)
        } as String?
        furhat.ask(robotResponse?:"¿Puedes repetirlo?")
    }

}





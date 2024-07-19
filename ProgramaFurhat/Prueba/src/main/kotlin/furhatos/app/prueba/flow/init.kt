package furhatos.app.prueba.flow

import furhatos.app.prueba.PruebaSkill
import furhatos.app.prueba.flow.main.Idle
import furhatos.app.prueba.flow.main.Greeting
import furhatos.app.prueba.setting.DISTANCE_TO_ENGAGE
import furhatos.app.prueba.setting.MAX_NUMBER_OF_USERS
import furhatos.flow.kotlin.State
import furhatos.flow.kotlin.furhat
import furhatos.flow.kotlin.state
import furhatos.flow.kotlin.users
import furhatos.util.Gender
import furhatos.util.Language
import org.json.JSONObject
import java.io.File
import java.io.InputStream

val numero = mutableMapOf<String, Int>()
val Init: State = state {
    init {
        furhat.param.endSilTimeout = 1000
        furhat.param.noSpeechTimeout = 60000
        furhat.param.maxSpeechTimeout = 30000
        /** Set our default interaction parameters */
        users.setSimpleEngagementPolicy(DISTANCE_TO_ENGAGE, MAX_NUMBER_OF_USERS)
        furhat.setVoice(Language.SPANISH_ES, Gender.MALE, false)
        furhat.setInputLanguage(Language.SPANISH_ES)
        loadNumeroHistoriales()
        goto(Context)
    }
    onEntry {
        /** start interaction */
             // Convenient to bypass the need for user when running Virtual Furhat

    }

}
fun loadNumeroHistoriales(){
    val resourcePath = "/Historiales médicos test.json"
    val inputStream: InputStream? = Init::class.java.getResourceAsStream(resourcePath)
    var jsonString=""
    if (inputStream != null) {
        // Read the contents of the file
         jsonString = inputStream.bufferedReader().use { it.readText() }
    } else {
        println("File does not exist at the specified resource path.")
    }

    val jsonObject = JSONObject(jsonString)
    // Access the "lista" array
    val nullableInt:Int? = if(jsonObject.has("num")) jsonObject.getInt("num") else null
    // Get the information associated with a specific number key (e.g., key "0")
    numero["num"]=nullableInt ?:0
}
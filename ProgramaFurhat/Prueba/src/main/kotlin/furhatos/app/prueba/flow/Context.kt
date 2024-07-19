package furhatos.app.prueba.flow
import com.sun.org.apache.xalan.internal.xsltc.compiler.util.Type.Int
import furhatos.flow.kotlin.State
import furhatos.flow.kotlin.furhat
import furhatos.flow.kotlin.onResponse
import furhatos.flow.kotlin.state
import furhatos.app.prueba.flow.main.Greeting
import org.json.JSONObject
import java.io.File
import furhatos.nlu.EnumEntity
import furhatos.nlu.Intent
import furhatos.util.Gender
import furhatos.util.Language
import furhatos.app.prueba.flow.numero
import java.io.InputStream

val data = mutableMapOf<String, Any>()
val Context : State=state {
    var historial:String=""
    var num:String=""
    onEntry{
        furhat.ask("Por favor, di el número de entrevista que deseas probar, ten en cuenta que hay "+numero["num"]+ ". Para una mejor experiencia haz las preguntas en segunda persona.")

    }

    onResponse <Numero>{
        val interviewNumber=it.text.toString()
        data["historial"]= loadMedicalHistoryString(interviewNumber)
        goto(Greeting)
    }
}

fun loadMedicalHistoryString(interviewNumber: String): String {
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
    val listaArray = jsonObject.getJSONArray("lista")
    // Get the information associated with a specific number key (e.g., key "0")
    val information = listaArray.getJSONObject(interviewNumber.toInt())
    val contexto=information.getString(interviewNumber)
    println(contexto)

    return contexto
}

class Numero : EnumEntity() {
    override fun getEnum(lang: Language): List<String> {
        val numConver:Int=(numero["num"] ?: 0)-1

        return (0..numConver).map{it.toString()}
    }
}
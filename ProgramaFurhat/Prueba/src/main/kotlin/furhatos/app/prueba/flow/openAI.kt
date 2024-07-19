package furhatos.app.prueba.flow

import java.io.File

import okhttp3.OkHttpClient
import okhttp3.Request
import com.google.gson.Gson
import furhatos.flow.kotlin.DialogHistory
import furhatos.flow.kotlin.Furhat
import org.json.JSONObject
import furhatos.flow.kotlin.furhat
import furhatos.flow.kotlin.onResponse
import furhatos.flow.kotlin.state
import furhatos.app.prueba.flow.main.Greeting
import java.io.InputStream


fun getDialogCompletion(historial:String): String? {
    val resourcePath = "/apiKey.txt"
    val inputStream: InputStream? = Greeting::class.java.getResourceAsStream(resourcePath)
    var apiKey=""
    if (inputStream != null) {
        // Read the contents of the file
        apiKey = inputStream.bufferedReader().use { it.readText().trim() }
    } else {
        println("File does not exist at the specified resource path.")
    }
    val promptDisegn= loadPrompt()
    val agentName = "Robot"
    val description = promptDisegn+ "\n"+historial
    val contextWindowSize = 10
    val history = mutableListOf<String>()
    Furhat.dialogHistory.all.takeLast(contextWindowSize).forEach {
        when (it) {
            is DialogHistory.ResponseItem -> {
                history.add("Human: ${it.response.text}")
            }
            is DialogHistory.UtteranceItem -> {
                history.add("$agentName: ${it.toText()}")
            }

        }

    }

    val prompt = "$description\n\n${history.joinToString(separator = "\n")}\n$agentName:"
    val requestBody = mapOf(
        "model" to "gpt-3.5-turbo",
        "messages" to listOf(mapOf("role" to "system", "content" to prompt)),
        "temperature" to 0,
        "stop" to listOf("$agentName:", "Human:")
    )

    val response = khttp.post(
        url = "https://api.openai.com/v1/chat/completions",
        headers = mapOf(
            "Content-Type" to "application/json",
            "Authorization" to "Bearer $apiKey" // Fix API key concatenation
        ),
        json = requestBody
    )

    // Handle errors
    if (response.statusCode != 200) {
        println("Error: ${response.jsonObject}")
        return null
    }

    // Extract completion from response
    val choices = response.jsonObject.optJSONArray("choices")
    if (choices == null || choices.length() == 0) {
        println("Error: No choices found in response")
        return null
    }

    val completion = response.jsonObject.getJSONArray("choices").getJSONObject(0).getJSONObject("message").getString("content")
    return completion.trim()
}

fun loadPrompt(): String?{
    val resourcePath = "/prompt.json"
    val inputStream: InputStream? = Init::class.java.getResourceAsStream(resourcePath)
    var jsonString=""
    if (inputStream != null) {
        // Read the contents of the file
         jsonString = inputStream.bufferedReader().use { it.readText() }
    } else {
        println("File does not exist at the specified resource path.")
    }
    val jsonObject = JSONObject(jsonString)
    val prompt=jsonObject.getString("1")
    return prompt
}

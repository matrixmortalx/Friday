package com.friday

import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.ScrollView
import android.widget.TextView
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.cancel
import kotlinx.coroutines.launch
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject
import java.util.concurrent.TimeUnit

class MainActivity : AppCompatActivity() {
    private lateinit var inputText: EditText
    private lateinit var sendButton: Button
    private lateinit var imageButton: Button
    private lateinit var settingsButton: Button
    private lateinit var outputText: TextView
    private lateinit var scrollView: ScrollView

    private val client = OkHttpClient.Builder()
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(120, TimeUnit.SECONDS)
        .writeTimeout(30, TimeUnit.SECONDS)
        .build()

    private val scope = CoroutineScope(Dispatchers.IO)
    private var backendUrl = "http://10.0.2.2:8000"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        inputText = findViewById(R.id.inputText)
        sendButton = findViewById(R.id.sendButton)
        imageButton = findViewById(R.id.imageButton)
        settingsButton = findViewById(R.id.settingsButton)
        outputText = findViewById(R.id.outputText)
        scrollView = findViewById(R.id.scrollView)

        outputText.text = "Merhaba! Ben Friday.\n\nBackend hazır olmalı.\nAyarlar menüsünden sunucu URL'sini güncelleyebilirsin."

        sendButton.setOnClickListener { sendPrompt() }
        imageButton.setOnClickListener { generateImage() }
        settingsButton.setOnClickListener { showSettings() }
    }

    private fun sendPrompt() {
        val text = inputText.text.toString().trim()
        if (text.isEmpty()) return

        inputText.setText("")
        appendText("Sen: $text\n")

        scope.launch {
            try {
                val body = JSONObject().apply {
                    put("message", text)
                }

                val request = Request.Builder()
                    .url("$backendUrl/api/chat")
                    .post(body.toString().toRequestBody("application/json".toMediaType()))
                    .build()

                val response = client.newCall(request).execute()
                val responseBody = response.body?.string() ?: "{}"
                val json = JSONObject(responseBody)
                val reply = json.optString("reply", "Cevap alınamadı.")

                runOnUiThread {
                    appendText("Friday: $reply\n")
                }
            } catch (e: Exception) {
                runOnUiThread {
                    appendText("Hata: ${e.message}\n")
                }
            }
        }
    }

    private fun generateImage() {
        val text = inputText.text.toString().trim()
        if (text.isEmpty()) return

        inputText.setText("")
        appendText("İstek: $text\n")

        scope.launch {
            try {
                val body = JSONObject().apply {
                    put("message", text)
                }

                val request = Request.Builder()
                    .url("$backendUrl/api/image")
                    .post(body.toString().toRequestBody("application/json".toMediaType()))
                    .build()

                val response = client.newCall(request).execute()
                val responseBody = response.body?.string() ?: "{}"
                val json = JSONObject(responseBody)
                val imageUrl = json.optString("image_url", "")

                runOnUiThread {
                    if (imageUrl.isNotEmpty()) {
                        appendText("Görsel: $imageUrl\n")
                    } else {
                        appendText("Görsel URL dönmedi.\n")
                    }
                }
            } catch (e: Exception) {
                runOnUiThread {
                    appendText("Görsel hatası: ${e.message}\n")
                }
            }
        }
    }

    private fun showSettings() {
        val current = backendUrl
        val edit = EditText(this).apply {
            setText(current)
        }

        AlertDialog.Builder(this)
            .setTitle("Backend URL")
            .setView(edit)
            .setPositiveButton("Kaydet") { _, _ ->
                val value = edit.text.toString().trim()
                if (value.isNotEmpty()) {
                    backendUrl = value
                }
            }
            .setNegativeButton("İptal", null)
            .show()
    }

    private fun appendText(value: String) {
        runOnUiThread {
            outputText.append(value)
            scrollView.post { scrollView.fullScroll(ScrollView.FOCUS_DOWN) }
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        scope.cancel()
    }
}

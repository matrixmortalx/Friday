package com.friday

import android.os.Bundle
import android.widget.ArrayAdapter
import android.widget.Button
import android.widget.EditText
import android.widget.ScrollView
import android.widget.Spinner
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
    private lateinit var modelSpinner: Spinner
    private lateinit var providerSpinner: Spinner

    private val client = OkHttpClient.Builder()
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(120, TimeUnit.SECONDS)
        .writeTimeout(30, TimeUnit.SECONDS)
        .build()

    private val scope = CoroutineScope(Dispatchers.IO)
    private var backendUrl = "http://10.0.2.2:8000"
    private var selectedProvider = "anthropic"
    private var selectedModel = "claude-3-5-sonnet-20241022"

    private val modelMap = mapOf(
        "anthropic" to listOf(
            "claude-3-5-sonnet-20241022",
            "claude-3-5-opus-20241022"
        ),
        "google" to listOf(
            "gemini-2.5-flash",
            "gemini-2.5-pro",
            "gemini-1.5-pro",
            "gemini-1.5-flash"
        )
    )

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        inputText = findViewById(R.id.inputText)
        sendButton = findViewById(R.id.sendButton)
        imageButton = findViewById(R.id.imageButton)
        settingsButton = findViewById(R.id.settingsButton)
        outputText = findViewById(R.id.outputText)
        scrollView = findViewById(R.id.scrollView)
        modelSpinner = findViewById(R.id.modelSpinner)
        providerSpinner = findViewById(R.id.providerSpinner)

        outputText.text = "Merhaba! Ben Friday.\n\nProvider ve model seçebilirsiniz.\nBackend hazır olmalı."

        setupSpinners()

        sendButton.setOnClickListener { sendPrompt() }
        imageButton.setOnClickListener { generateImage() }
        settingsButton.setOnClickListener { showSettings() }
    }

    private fun setupSpinners() {
        val providers = listOf("anthropic", "google")
        val providerAdapter = ArrayAdapter(this, android.R.layout.simple_spinner_item, providers)
        providerAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        providerSpinner.adapter = providerAdapter

        providerSpinner.setSelection(0)
        providerSpinner.onItemSelectedListener = object : android.widget.AdapterView.OnItemSelectedListener {
            override fun onItemSelected(parent: android.widget.AdapterView<*>, view: android.view.View?, pos: Int, id: Long) {
                selectedProvider = providers[pos]
                updateModelSpinner()
            }
            override fun onNothingSelected(parent: android.widget.AdapterView<*>) {}
        }

        updateModelSpinner()
    }

    private fun updateModelSpinner() {
        val models = modelMap[selectedProvider] ?: modelMap["anthropic"]!!
        val modelAdapter = ArrayAdapter(this, android.R.layout.simple_spinner_item, models)
        modelAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        modelSpinner.adapter = modelAdapter

        val defaultIndex = models.indexOf(selectedModel).takeIf { it >= 0 } ?: 0
        modelSpinner.setSelection(defaultIndex)
        selectedModel = models[defaultIndex]

        modelSpinner.onItemSelectedListener = object : android.widget.AdapterView.OnItemSelectedListener {
            override fun onItemSelected(parent: android.widget.AdapterView<*>, view: android.view.View?, pos: Int, id: Long) {
                selectedModel = models[pos]
            }
            override fun onNothingSelected(parent: android.widget.AdapterView<*>) {}
        }
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
                    put("model", selectedModel)
                    put("provider", selectedProvider)
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
                    put("model", selectedModel)
                    put("provider", selectedProvider)
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

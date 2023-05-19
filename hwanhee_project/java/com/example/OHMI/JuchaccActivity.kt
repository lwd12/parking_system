package com.example.OHMI

import android.annotation.SuppressLint
import android.content.Intent
import android.os.Bundle
import android.webkit.WebView
import android.widget.ImageButton
import androidx.appcompat.app.AppCompatActivity




class JuchaccActivity : AppCompatActivity() {

    private lateinit var webView: WebView

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_juchacc)

        // 홈 버튼 클릭 이벤트 처리
        val homeBtn3 = findViewById<ImageButton>(R.id.homeBT3)
        homeBtn3.setOnClickListener {
            val intent = Intent(this, MainActivity::class.java)
            startActivity(intent)
        }

        webView = findViewById(R.id.CCTVView)
        webView.settings.javaScriptEnabled = true

        // WebView에 URL 띄우기
        val cctvUrl = "http://192.168.0.220:5000/"
        webView.loadUrl(cctvUrl)
    }
}

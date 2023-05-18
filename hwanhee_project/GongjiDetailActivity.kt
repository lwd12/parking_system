package com.example.OHMI

import android.os.Bundle
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

class GongjiDetailActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_gongji2)

        val titleTextView = findViewById<TextView>(R.id.GongJiTv1)
        val contentTextView = findViewById<TextView>(R.id.GongJiTv2)

        val title = intent.getStringExtra("title")
        val content = intent.getStringExtra("content")

        titleTextView.text = title
        contentTextView.text = content
    }
}

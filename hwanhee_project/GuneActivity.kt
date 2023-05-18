package com.example.OHMI

import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.widget.EditText
import android.widget.ImageButton
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import okhttp3.MediaType
import okhttp3.RequestBody
import okhttp3.ResponseBody
import org.json.JSONObject
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory




class GuneActivity : AppCompatActivity() {
    private lateinit var editText: EditText

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_gune)

        editText = findViewById(R.id.GunET1)
        val 건의보내기 = findViewById<ImageButton>(R.id.GunEgo)
        val 건의목록보기 = findViewById<ImageButton>(R.id.GunEAng)

        건의보내기.setOnClickListener {
            val suggestionText = editText.text.toString()
            // 건의사항 전송 처리
            sendDataToServer(suggestionText)
        }

        건의목록보기.setOnClickListener {
            val intent = Intent(this@GuneActivity, GunebogiActivity::class.java)
            startActivity(intent)
        }
    }

    private fun sendDataToServer(suggestion: String) {
        // 건의 사항을 서버로 전송하는 로직 구현
        val requestBody = JSONObject().apply {
            put("content", suggestion)
        }
        val requestBodyTyped = RequestBody.create(MediaType.parse("application/json"), requestBody.toString())

        val retrofit = Retrofit.Builder()
            .baseUrl("http://192.168.0.19:9000/")
            .addConverterFactory(GsonConverterFactory.create())
            .build()

        val apiService = retrofit.create(ApiService::class.java)
        apiService.GunE(requestBodyTyped).enqueue(object : Callback<ResponseBody> {
            override fun onResponse(call: Call<ResponseBody>, response: Response<ResponseBody>) {
                if (response.isSuccessful) {
                    Log.d("GuneActivity", "건의 사항이 전송되었습니다.")
                    Toast.makeText(this@GuneActivity, "건의 사항이 전송되었습니다.", Toast.LENGTH_SHORT).show()
                } else {
                    Log.e("GuneActivity", "건의 사항 전송 실패: ${response.code()}")
                }
            }

            override fun onFailure(call: Call<ResponseBody>, t: Throwable) {
                Log.e("GuneActivity", "건의 사항 전송 실패: ${t.message}")
            }
        })
    }
}


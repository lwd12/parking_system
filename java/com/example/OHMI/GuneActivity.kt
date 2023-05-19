package com.example.OHMI

import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.widget.EditText
import android.widget.ImageButton
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.OHMI.LoginActivity.Companion.Aid1
import com.example.OHMI.LoginActivity.Companion.Aid2
import okhttp3.MediaType
import okhttp3.RequestBody
import okhttp3.ResponseBody
import org.json.JSONObject
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter

class GuneActivity : AppCompatActivity() {
    private lateinit var titleEditText: EditText
    private lateinit var contentEditText: EditText

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_gune)

        titleEditText = findViewById(R.id.GunET1)
        contentEditText = findViewById(R.id.GunET2)

        val 건의보내기 = findViewById<ImageButton>(R.id.GunEgo)
        val 건의목록보기 = findViewById<ImageButton>(R.id.GunEAng)

        건의보내기.setOnClickListener {
            val title = titleEditText.text.toString()
            val content = contentEditText.text.toString()
            val currentTime = getCurrentTime()
            val type = "건의"
            val modify = "None"
            // 건의사항 전송 처리
            sendDataToServer(title, content, currentTime,type,modify)

        }

        건의목록보기.setOnClickListener {
            val intent = Intent(this@GuneActivity, GunebogiActivity::class.java)
            startActivity(intent)
        }
    }

    private fun sendDataToServer(title: String, content: String, currentTime: String, type: String, modify: String) {
        // 건의 사항을 서버로 전송하는 로직 구현
        val requestBody = JSONObject().apply {
            put("subject", title)
            put("content", content)
            put("creator", Aid1 + "동 " + Aid2 + "호" )
            put("modify_datetime", JSONObject.NULL)
            put("create_datetime", currentTime)
            put("etc",type)

        }
        Log.d("text",title)
        Log.d("text",content)
        Log.d("text",currentTime)
        Log.d("text",type)
        Log.d("text",modify )
        Log.d("text",Aid1+"동" + Aid2+"호")

        val requestBodyTyped = RequestBody.create(MediaType.parse("application/json"), requestBody.toString())

        val retrofit = Retrofit.Builder()
            .baseUrl("http://3.34.74.107:8000")
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

    private fun getCurrentTime(): String {
        val currentDateTime = LocalDateTime.now()
        val formatter = DateTimeFormatter.ISO_DATE_TIME
        return currentDateTime.format(formatter)
    }
}


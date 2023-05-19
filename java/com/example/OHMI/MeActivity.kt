package com.example.OHMI

import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.widget.ImageButton
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import okhttp3.MediaType
import okhttp3.RequestBody
import okhttp3.ResponseBody
import org.json.JSONException
import org.json.JSONObject
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory




class   MeActivity : AppCompatActivity() {
    private val apiService = Retrofit.Builder()
        .baseUrl("http://3.34.74.107:8000")
        .addConverterFactory(GsonConverterFactory.create())
        .build()
        .create(ApiService::class.java)

    private lateinit var dongTextView: TextView
    private lateinit var phoneTextView: TextView
    private lateinit var carNumberTextView: TextView
    private lateinit var carTypeTextView: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_me)

        dongTextView = findViewById(R.id.MET1)
        phoneTextView = findViewById(R.id.MET3)
        carNumberTextView = findViewById(R.id.MET4)
        carTypeTextView = findViewById(R.id.MET5)

        val homeBtn5 = findViewById<ImageButton>(R.id.homeBT5)
        homeBtn5.setOnClickListener {
            val intent = Intent(this, MainActivity::class.java)
            startActivity(intent)
        }

        // Aid1, Aid2 값을 서버로 전송
        sendDataToServer()

        // GunE 버튼 클릭 이벤트 리스너 등록
        val guneBtn = findViewById<ImageButton>(R.id.GunE)
        guneBtn.setOnClickListener {
            val intent = Intent(this, GuneActivity::class.java)
            startActivity(intent)
        }
    }

    // 서버로 데이터 전송하는 함수
    private fun sendDataToServer() {
        if (LoginActivity.Aid1 != null && LoginActivity.Aid2 != null) {
            // HTTP 요청을 보냅니다.
            val requestBody = JSONObject().apply {
                put("dong", LoginActivity.Aid1)
                put("ho", LoginActivity.Aid2)

            }
            val requestBodyTyped = RequestBody.create(MediaType.parse("application/json"), requestBody.toString())

            apiService.sendDataToServer(requestBodyTyped).enqueue(object : Callback<ResponseBody> {
                override fun onResponse(call: Call<ResponseBody>, response: Response<ResponseBody>) {
                    if (response.isSuccessful) {
                        try {
                            val jsonObject = JSONObject(response.body()?.string())
                            // 서버에서 받은 데이터 처리
                            val dong = jsonObject.getString("resident_dong_ho")
                            val phone = jsonObject.getString("resident_phone")
                            val carNumber = jsonObject.getString("resident_carnumber")
                            val carType = jsonObject.getString("resident_typeofcar")

                            // 해당 뷰에 출력
                            dongTextView.text = "집 주소: $dong"
                            phoneTextView.text = "전화번호: $phone"
                            carNumberTextView.text = "차번호: $carNumber"
                            carTypeTextView.text = "차타입: $carType"
                        } catch (e: JSONException) {
                            Log.e("MeActivity", "데이터 전송 실패: ${e.message}")
                        }
                    } else {
                        Log.e("MeActivity", "데이터 전송 실패: ${response.code()}")
                    }
                }

                override fun onFailure(call: Call<ResponseBody>, t: Throwable) {
                    Log.e("MeActivity", "데이터 전송 실패: ${t.message}")
                }
            })
        }
    }
}
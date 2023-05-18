package com.example.OHMI

import android.content.Intent
import android.os.Bundle
import android.widget.Button
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
import java.time.LocalDate




class NomeActivity : AppCompatActivity() {

    private val retrofit = Retrofit.Builder()
        .baseUrl("http://192.168.0.19:9000")
        .addConverterFactory(GsonConverterFactory.create())
        .build()

    private val apiService = retrofit.create(ApiService::class.java)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_nome)

        val homeBtn4 = findViewById<ImageButton>(R.id.homeBT4)
        homeBtn4.setOnClickListener {
            val intent = Intent(this, MainActivity::class.java)
            startActivity(intent)
        }

        // 방문자 정보 전송 버튼 클릭 이벤트 처리
        val registerBtn = findViewById<Button>(R.id.register_button)
        registerBtn.setOnClickListener {
            // EditText에서 입력한 차량 번호와 날짜를 가져와 변수에 저장
            val carNumber = findViewById<EditText>(R.id.car_number_input).text.toString()
            val date = findViewById<EditText>(R.id.visit_date_input).text.toString()

            // 서버에 데이터 전송하기
            sendData(carNumber, date)
        }
    }

    private fun sendData(carNumber: String, date: String) {
        val jsonObject = JSONObject()
        val currentDate = LocalDate.now()
        val dateString = currentDate.toString()

        jsonObject.put("visitor_information_carnumber", carNumber)
        jsonObject.put("visitor_information_date", date)
        jsonObject.put("resident_dong", LoginActivity.Aid1)
        jsonObject.put("resident_ho", LoginActivity.Aid2)
        jsonObject.put("residents_number" ,1 )
        jsonObject.put("visitor_information_datetime" ,dateString )

        println(jsonObject.toString())

        val requestBody =
            RequestBody.create(
                MediaType.parse("application/json; charset=utf-8"),
                jsonObject.toString()
            )
        println(requestBody)
        apiService.sendData(requestBody).enqueue(object : Callback<ResponseBody> {
            override fun onResponse(call: Call<ResponseBody>, response: Response<ResponseBody>) {
                println(response)
                if (response.isSuccessful) {
                    // 등록 성공
                    Toast.makeText(this@NomeActivity, "등록이 완료되었습니다.", Toast.LENGTH_SHORT).show()
                } else {
                    // 등록 실패
                    //Toast.makeText(this@NomeActivity, "등록에 실패하였습니다.", Toast.LENGTH_SHORT).show()
                    Toast.makeText(this@NomeActivity, jsonObject.toString(), Toast.LENGTH_SHORT)
                        .show()
                }
            }

            override fun onFailure(call: Call<ResponseBody>, t: Throwable) {
                TODO("Not yet implemented")
                // 서버로 요청을 보내지 못했을 때 수행할 코드
                Toast.makeText(
                    this@NomeActivity,
                    "서버와의 통신에 실패하였습니다. ${t.message}",
                    Toast.LENGTH_SHORT
                ).show()
            }
        })
    }
}
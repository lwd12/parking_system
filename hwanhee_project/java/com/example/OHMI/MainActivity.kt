@file:Suppress("PackageName")
package com.example.OHMI

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.Context
import android.content.Intent
import android.os.*
import androidx.appcompat.app.AppCompatActivity
import android.provider.ContactsContract
import android.util.Log
import android.widget.*
import androidx.core.app.NotificationCompat
import com.google.gson.annotations.SerializedName
import okhttp3.RequestBody
import okhttp3.ResponseBody
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.*


interface ApiService {
    @GET("/visitor_information/")
    fun getData(): Call<ContactsContract.Contacts.Data>

    @POST("/visitor_information/")
    fun sendData(@Body body: RequestBody): Call<ResponseBody>

    @POST("/loginforClient/")
    fun login(@Body body: RequestBody): Call<ResponseBody>

    @GET("/question/")
    fun getQuestionsSortedByNumberDesc(): Call<List<Question>>

    @GET("safetyaccident/")
    fun getSafetyAccidents(): Call<List<SafetyAccident>>

    @POST("ClientData/")
    fun sendDataToServer(@Body body: RequestBody): Call<ResponseBody>

    @GET("insidetheparkinglot/")
    fun getJuCha(): Call<List<ChaCha>>

    @POST("parkinglot/")
    fun POSTParking(@Body requestBody: RequestBody): Call<ResponseBody>

    @POST("/question/")
    fun GunE(@Body requestBody: RequestBody): Call<ResponseBody>
}

//그렇게 안보이겠지만 화재감지 데이터
data class SafetyAccident(
    @SerializedName("safetyaccident_number")
    val safetyAccidentNumber: Int,
    @SerializedName("safetyaccident_datetime")
    val safetyAccidentDatetime: String,
    @SerializedName("safetyaccident_kind")
    val safetyAccidentKind: String
)

//메인(굿 따따봉)
class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        //공지사항
        val btn1 = findViewById<ImageButton>(R.id.btn1)
        //주차장 메인 단면도
        val btn2 = findViewById<ImageButton>(R.id.btn2)
        //주차장 CCTV
        val btn3 = findViewById<ImageButton>(R.id.btn3)
        //방문자
        val btn4 = findViewById<ImageButton>(R.id.btn4)
        //내정보
        val btn5 = findViewById<ImageButton>(R.id.btn5)


        //공지사항
        btn1.setOnClickListener {
            val intent = Intent(this, GongjiActivity::class.java)
            startActivity(intent)
        }

        //주차장 메인 단면도
        btn2.setOnClickListener {
            val intent = Intent(this, JuchaActivity::class.java)
            startActivity(intent)
        }

        //주차장 CCTV
        btn3.setOnClickListener {
            val intent = Intent(this, JuchaccActivity::class.java)
            startActivity(intent)
        }

        //방문자 등록
        btn4.setOnClickListener {
            val intent = Intent(this, NomeActivity::class.java)
            startActivity(intent)
        }

        //내정보 확인
        btn5.setOnClickListener {
            val intent = Intent(this, MeActivity::class.java)
            startActivity(intent)
        }
    }
}
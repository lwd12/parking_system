package com.example.OHMI

import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.ImageButton
import android.widget.ImageView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.google.gson.annotations.SerializedName
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


//그렇게 안보이겠지만 주차장메인 데이터
data class ChaCha(
    @SerializedName("parking_generalseat")
    val parking_generalseat: String,
    @SerializedName("parking_evchargedseattstate")
    val parking_evchargedseattstate: String,
    @SerializedName("parking_seatstate")
    val parking_seatstate: Boolean,
    @SerializedName("parking_seatcarnumber")
    val parking_seatcarnumber: String,
)



class JuchaActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_jucha)


        val retrofit = Retrofit.Builder()
            .baseUrl("http://3.34.74.107:8000")
            .addConverterFactory(GsonConverterFactory.create())
            .build()

        val requestBody = JSONObject().apply {
            put("dong", LoginActivity.Aid1)
            put("ho", LoginActivity.Aid2)
        }
        val requestBodyTyped = RequestBody.create(MediaType.parse("application/json"), requestBody.toString())

        val MECAR1 = findViewById<ImageView>(R.id. MECAR1)
        val MECAR2 = findViewById<ImageView>(R.id. MECAR2)
        val MECAR3 = findViewById<ImageView>(R.id. MECAR3)

        val jari1 = findViewById<ImageButton>(R.id.JARIIT1)
        val jari2 = findViewById<ImageButton>(R.id.JARIIT2)
        val jari3 = findViewById<ImageButton>(R.id.JARIIT3)




        val apiService = retrofit.create(ApiService::class.java)
        apiService.sendDataToServer(requestBodyTyped).enqueue(object : Callback<ResponseBody> {
            override fun onResponse(call: Call<ResponseBody>, response: Response<ResponseBody>) {
                if (response.isSuccessful) {
                    try {
                        val jsonObject = JSONObject(response.body()?.string())
                        // 서버에서 받은 데이터 처리
                        val carNumber1 = jsonObject.getString("resident_carnumber")
                        Log.d("juchaactivity", carNumber1)
                        // 주차 정보 가져오기
                        apiService.getJuCha().enqueue(object : Callback<List<ChaCha>> {
                            override fun onResponse(call: Call<List<ChaCha>>, response: Response<List<ChaCha>>) {
                                val choCho = response.body()?.take(10)
                                if (choCho != null) {
                                    for (item in choCho) {
                                        //if (item.parking_seatcarnumber == null)
                                        if (item.parking_seatcarnumber == carNumber1) {
                                            if (item.parking_generalseat == "A-1")
                                                MECAR1.visibility = View.VISIBLE
                                            else if (item.parking_generalseat == "B-1")
                                                MECAR2.visibility = View.VISIBLE
                                            else if (item.parking_generalseat == "C-1")
                                                MECAR3.visibility = View.VISIBLE
                                            Log.d("juchaactivity", item.toString())
                                            break
                                        } else {
                                            Log.d("juchaactivity",item.parking_generalseat)


                                            if (item.parking_seatstate == false) {
                                                if (item.parking_generalseat == "A-1")
                                                    jari1.visibility = View.VISIBLE
                                                else if (item.parking_generalseat == "B-1")
                                                    jari2.visibility = View.VISIBLE
                                                else if (item.parking_generalseat == "C-1")
                                                    jari3.visibility = View.VISIBLE
                                            }
                                        }
                                    }
                                }
                            }

                            override fun onFailure(call: Call<List<ChaCha>>, t: Throwable) {
                                // 실패
                            }

                        })
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


        val homeBtn2 = findViewById<ImageButton>(R.id.homeBT2)
        homeBtn2.setOnClickListener {
            val intent = Intent(this, MainActivity::class.java)
            startActivity(intent)
        }


        jari1.setOnClickListener {
            val requestBody = JSONObject().apply {
                put("parking_generalseat", "C-1")
                put("resident_dong", LoginActivity.Aid1)
                put("resident_ho", LoginActivity.Aid2)
            }
            val requestBodyTyped = RequestBody.create(MediaType.parse("application/json"), requestBody.toString())

            apiService.POSTParking(requestBodyTyped).enqueue(object : Callback<ResponseBody> {
                override fun onResponse(call: Call<ResponseBody>, response: Response<ResponseBody>) {
                    if (response.isSuccessful) {
                        Log.d("JuchaActivity", "자리 선택이 완료되었습니다.")
                        Toast.makeText(this@JuchaActivity, "자리 선택이 완료되었습니다.", Toast.LENGTH_SHORT).show()
                    } else {
                        Log.e("JuchaActivity", "데이터 전송 실패: ${response.code()}")
                    }
                }

                override fun onFailure(call: Call<ResponseBody>, t: Throwable) {
                    Log.e("JuchaActivity", "데이터 전송 실패: ${t.message}")
                }
            })
        }


        jari2.setOnClickListener {
            val requestBody = JSONObject().apply {
                put("parking_generalseat", "B-1")
                put("resident_dong", LoginActivity.Aid1)
                put("resident_ho", LoginActivity.Aid2)
            }
            val requestBodyTyped = RequestBody.create(MediaType.parse("application/json"), requestBody.toString())

            apiService.POSTParking(requestBodyTyped).enqueue(object : Callback<ResponseBody> {
                override fun onResponse(call: Call<ResponseBody>, response: Response<ResponseBody>) {
                    if (response.isSuccessful) {
                        Log.d("JuchaActivity", "자리 선택이 완료되었습니다.")
                        Toast.makeText(this@JuchaActivity, "자리 선택이 완료되었습니다.", Toast.LENGTH_SHORT).show()
                    } else {
                        Log.e("JuchaActivity", "데이터 전송 실패: ${response.code()}")
                    }
                }

                override fun onFailure(call: Call<ResponseBody>, t: Throwable) {
                    Log.e("JuchaActivity", "데이터 전송 실패: ${t.message}")
                }
            })
        }


        jari3.setOnClickListener {
            val requestBody = JSONObject().apply {
                put("parking_generalseat", "A-1")
                put("resident_dong", LoginActivity.Aid1)
                put("resident_ho", LoginActivity.Aid2)
            }
            val requestBodyTyped = RequestBody.create(MediaType.parse("application/json"), requestBody.toString())

            apiService.POSTParking(requestBodyTyped).enqueue(object : Callback<ResponseBody> {
                override fun onResponse(call: Call<ResponseBody>, response: Response<ResponseBody>) {
                    if (response.isSuccessful) {
                        Log.d("JuchaActivity", "자리 선택이 완료되었습니다.")
                        Toast.makeText(this@JuchaActivity, "자리 선택이 완료되었습니다.", Toast.LENGTH_SHORT).show()
                    } else {
                        Log.e("JuchaActivity", "데이터 전송 실패: ${response.code()}")
                    }
                }

                override fun onFailure(call: Call<ResponseBody>, t: Throwable) {
                    Log.e("JuchaActivity", "데이터 전송 실패: ${t.message}")
                }
            })
        }
    }
}
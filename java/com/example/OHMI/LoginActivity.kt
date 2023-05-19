package com.example.OHMI

import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
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
import retrofit2.http.Body
import retrofit2.http.POST




class LoginActivity : AppCompatActivity() {
    private lateinit var id1EditText: EditText
    private lateinit var id2EditText: EditText
    private lateinit var passwordEditText: EditText

    // 사용자 ID를 저장할 변수
    companion object {
        var Aid1: String? = null
        var Aid2: String? = null
    }


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_login)

        id1EditText = findViewById(R.id.ID1)
        id2EditText = findViewById(R.id.ID2)
        passwordEditText = findViewById(R.id.PS)
        val loginButton = findViewById<Button>(R.id.btn_login)


        // Retrofit 객체 생성
        val retrofit = Retrofit.Builder()
            .baseUrl("http://3.34.74.107:8000")
            .addConverterFactory(GsonConverterFactory.create())
            .build()
        val apiService = retrofit.create(ApiService::class.java)

        loginButton.setOnClickListener {
            try {
                // ID와 비밀번호를 가져옵니다.
                val id1 = id1EditText.text.toString()
                val id2 = id2EditText.text.toString()
                val password = passwordEditText.text.toString()

                // HTTP 요청을 보냅니다.
                val requestBody = JSONObject().apply {
                    put("dong", id1)
                    put("ho", id2)
                    put("PassWd", password)
                }
                val requestBodyTyped =
                    RequestBody.create(MediaType.parse("application/json"), requestBody.toString())

                apiService.login(requestBodyTyped).enqueue(object : Callback<ResponseBody> {
                    override fun onResponse(
                        call: Call<ResponseBody>,
                        response: Response<ResponseBody>
                    ) {
                        if (response.isSuccessful) {
                            try {
                                val jsonObject = JSONObject(response.body()?.string())
                                for (key in jsonObject.keys()) {
                                    // 해당 키에 대한 값 가져오기
                                    val value = jsonObject.get(key)
                                    // 여기에서 해당 값으로 필요한 작업 수행
                                    Log.d("JSON", "Key: $key, Value: $value")
                                }
                                print(jsonObject)
                                val state = jsonObject.getString("state")

                                if (state == "OK") {

                                    // 로그인에 성공하면 사용자 ID를 변수에 저장
                                    Aid1 = id1EditText.text.toString()
                                    Aid2 = id2EditText.text.toString()
                                    Log.d("LoginActivity", "id1: $id1, id2: $id2")

                                    val intent = Intent(this@LoginActivity, MainActivity::class.java)
                                    startActivity(intent)
                                    finish()
                                } else {

                                    Toast.makeText(this@LoginActivity, state, Toast.LENGTH_SHORT).show()
                                }
                            } catch (e: JSONException) {
                                Log.e("LoginActivity", "로그인 실패: ${e.message}")
                                Toast.makeText(this@LoginActivity, "로그인 실패1: ${e.message}", Toast.LENGTH_SHORT).show()
                            }
                        } else {
                            Log.e("LoginActivity", "로그인 실패: ${response.code()}")
                            Toast.makeText(this@LoginActivity, "로그인 실패2: ${response.code()}", Toast.LENGTH_SHORT).show()
                        }
                    }

                    override fun onFailure(call: Call<ResponseBody>, t: Throwable) {
                        Log.e("LoginActivity", "로그인 실패: ${t.message}")
                        Toast.makeText(this@LoginActivity, "로그인에 실패하였습니다.", Toast.LENGTH_SHORT).show()
                    }
                })
            } catch (e: Exception) {
                Log.e("LoginActivity", "로그인 실패: ${e.message}")
                Toast.makeText(this@LoginActivity, "로그인 실패3: ${e.message}", Toast.LENGTH_SHORT).show()
            }
        }
    }
}
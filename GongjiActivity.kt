package com.example.OHMI

import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.widget.ArrayAdapter
import android.widget.ImageButton
import android.widget.ListView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.google.gson.annotations.SerializedName
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

//그렇게 안보이겠지만 공지 데이터
data class Question(
    @SerializedName("subject")
    val subject: String,
    @SerializedName("content")
    val content: String,
    @SerializedName("creator")
    val creator: String,
    @SerializedName("question_number")
    val question_number: Int,
    @SerializedName("etc")
    val etc: String
)



class GongjiActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_gongji)

        val homeBtn1 = findViewById<ImageButton>(R.id.homeBT1)
        homeBtn1.setOnClickListener {
            val intent = Intent(this, MainActivity::class.java)
            startActivity(intent)
        }

        val listView = findViewById<ListView>(R.id.LV1)
        val adapter = ArrayAdapter<String>(this, android.R.layout.simple_list_item_1)
        listView.adapter = adapter

        val retrofit = Retrofit.Builder()
            .baseUrl("http://192.168.0.19:9000")
            .addConverterFactory(GsonConverterFactory.create())
            .build()

        val service = retrofit.create(ApiService::class.java)
        service.getQuestionsSortedByNumberDesc().enqueue(object : Callback<List<Question>> {

        override fun onResponse(call: Call<List<Question>>, response: Response<List<Question>>) {
            val questions = response.body()?.take(10)
            if (questions != null) {
                val filteredQuestions = questions.filter { it.etc == "공지" } // '건의' 값인 항목 필터링
                adapter.addAll(filteredQuestions.sortedByDescending { it.question_number }.map { it.subject })

                listView.setOnItemClickListener { parent, view, position, id ->
                    val intent = Intent(this@GongjiActivity, GongjiDetailActivity::class.java)
                    val selectedQuestion = filteredQuestions[position] // 필터링된 항목에서 선택한 항목 가져오기
                    intent.putExtra("content", selectedQuestion.content)
                    startActivity(intent)
                }
            }
        }

            override fun onFailure(call: Call<List<Question>>, t: Throwable) {
                Log.e("GongjiActivity", "Failed to get questions", t)
                Toast.makeText(this@GongjiActivity, "공지사항을 가져오는데 실패했습니다.", Toast.LENGTH_SHORT).show()
            }
        })
    }
}
import RPi.GPIO as GPIO
import cv2
import time
import pytesseract
import requests
import datetime
import base64
import json
from tkinter import *
from tkinter import messagebox

frame = ""
fail_count = 0
flag = False  # 입차


class Ras:  # 동/호수/비번 UI
    def __init__(self):
        self.show = Tk()
        self.show.title("Dong_Ho_Passward")
        self.show.geometry("640x400")
        self.show.resizable(0, 0)

        self.label = Label(self.show, text="동", width=15, height=2)
        self.label.grid(row=0, column=0)

        self.label1 = Label(self.show, text="호수", width=15, height=2)
        self.label1.grid(row=1, column=0)

        self.label2 = Label(self.show, text="비번", width=15, height=2)
        self.label2.grid(row=2, column=0)

        self.dong_textbox = Entry(self.show, width=15)
        self.dong_textbox.grid(row=0, column=1, padx=30, pady=30)

        self.ho_textbox = Entry(self.show, width=15)
        self.ho_textbox.grid(row=1, column=1, padx=30, pady=30)

        self.pw_textbox = Entry(self.show, width=15)
        self.pw_textbox.grid(row=2, column=1, padx=30, pady=30)

        self.button = Button(
            self.show, text="Send", width=15, height=2, command=self.click
        )
        self.button.grid(row=0, column=2)

        self.dong_value = ""
        self.ho_value = ""
        self.pw_value = ""

        self.is_running = True

    def click(self):
        # self.label.configure(text="전송됨")
        self.dong_value = self.dong_textbox.get()  # 텍스트 값 받기
        self.ho_value = self.ho_textbox.get()
        self.pw_value = self.pw_textbox.get()

        if self.dong_value == "" or self.ho_value == "" or self.pw_value == "":
            messagebox.showinfo("Title", "동, 호수, 비밀번호 중 입력하지 않은 것이 있습니다.")
        else:
            self.dong_result = int(self.dong_value)
            self.ho_result = int(self.ho_value)
            self.pw_result = int(self.pw_value)
            self.show.destroy()
            self.is_running = False


class jsonurl:
    def __init__(self):
        self.residents_endpoint = "http://192.168.0.19:9000/residents_information/"
        self.visitors_endpoint = "http://192.168.0.19:9000/visitor_information/"
        self.parking_endpoint = "http://192.168.0.19:9000/entrancetotheparkinglot/"


headers = {
    # "Authorization": "ToKen 750b311fec4b7c0a2a023bd557a149fb1f3a5085",  # 토큰값
    "Content-Type": "application/json",
    "charset": "UTF-8",
    "Accept": "*/*",
}


def encoding_image(final_result, iso):
    ras = Ras()
    ras.dong_value = ""  # 텍스트 받는 값 null로 초기화
    ras.ho_value = ""
    ras.pw_value = ""
    global flag
    while ras.is_running:
        ras.show.mainloop()  # 창 실행

    url = "http://192.168.0.19:9000/unauthorized_parking/"  # 비인가 차량 url

    with open("./cap01.jpg", "rb") as f:
        img_data = f.read()
    encoded_data = base64.b64encode(img_data).decode("utf-8")  # 이미지 디코딩(이미지 받아오기)
    print(encoded_data)

    body = {
        # "parking_log_number": 1,
        "unauthorized_carnumber": encoded_data,
        "unauthorized_carnumbers": final_result[0],
        "resident_dong": ras.dong_result,  # ras.dong_result
        "resident_ho": ras.dong_result,  # ras.dong_result
        "residents_doorpasswd": ras.pw_result,  # ras.pw_result
        # "residest_number": ras.answer,
    }
    if flag == True:
        data = {
            "typeofentrysandexit": "출차",
            "exitdatetime": iso,
        }
    else:
        data = {
            "typeofentrysandexit": "입차",
            "entrydatetime": iso,
        }
    body.update(data)  # 딕셔너리 붙이기
    flag = False
    response = requests.post(
        url,
        headers=headers,
        data=json.dumps(body, ensure_ascii=False).encode("utf8"),
    )  # json 형식으로 post(생성)
    # ras.response_image(response)
    print("response status %r" % response.status_code)
    print("response text %r" % response.text)
    dic = eval(response.text)
    if dic["state"] == "ok":
        servo_setting()


def comingcar_dect():
    # camera = cv2.VideoCapture(0)
    # camera.set(3, 320)
    # camera.set(4, 240)

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    TRIG_CARIN = 23
    ECHO_CARIN = 24

    TRIG_CAROUT = 21
    ECHO_CAROUT = 20
    print("Distance measurement in progress")

    GPIO.setup(TRIG_CARIN, GPIO.OUT)
    GPIO.setup(ECHO_CARIN, GPIO.IN)
    GPIO.setup(TRIG_CAROUT, GPIO.OUT)
    GPIO.setup(ECHO_CAROUT, GPIO.IN)

    button_pin = 15
    GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    print("Waiting for sensor to settle")
    GPIO.setup(TRIG_CARIN, False)
    GPIO.setup(TRIG_CAROUT, False)
    time.sleep(2)

    try:
        while True:
            distance_in = measure(TRIG_CARIN, ECHO_CARIN)  # 입차 초음파
            distance_out = measure(TRIG_CAROUT, ECHO_CAROUT)  # 출차 초음파

            print("Car IN Distance : %d cm" % distance_in)
            time.sleep(0.4)
            print("Car OUT Distance : %d cm" % distance_out)
            time.sleep(0.4)
            try:
                if (
                    distance_in < 30 or distance_out < 30
                ):  # distance_in < 30 or distance_out < 30
                    camera = cv2.VideoCapture(0)
                    camera.set(3, 640)
                    camera.set(4, 480)
                    global frame
                    global flag
                    _, frame = camera.read()

                    cv2.imshow("Frame", frame)
                    cv2.waitKey(30)

                    # if GPIO.input(button_pin) == GPIO.HIGH:  # 버튼이 눌리면 실행
                    print("Button pushed!")
                    cv2.imwrite("./cap01.jpg", frame)  # 이미지 저장
                    color_img = cv2.imread("./cap01.jpg", cv2.IMREAD_COLOR)
                    if distance_out < 30:
                        flag = True
                    framesetting(color_img)  # 차 인식
                    camera.release()
                    cv2.destroyAllWindows()
                else:
                    cv2.destroyAllWindows()
            except:
                print("출입차량 중 한대만 와주세요.")
            # test(distance,button_pin,camera)
    except KeyboardInterrupt:
        print("measurement stopped by User")
        GPIO.cleanup()


def measure(TRIG, ECHO):
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        start = time.time()
    while GPIO.input(ECHO) == 1:
        stop = time.time()
    check_time = stop - start
    distance = check_time * 34300 / 2
    return distance  # 측정된 거리 반환


def servo_setting():
    servo_pin = 12
    GPIO.setup(servo_pin, GPIO.OUT)
    p = GPIO.PWM(servo_pin, 50)
    p.start(0)

    p.ChangeDutyCycle(5.6)
    time.sleep(4)
    p.ChangeDutyCycle(1.8)
    time.sleep(0.1)


def framesetting(img):
    global fail_count
    global flag
    fail_count += 1
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print(fail_count)
    blur = cv2.GaussianBlur(img_gray, (3, 3), 0)
    for i in range(30, 180, 1):  # 150, 240
        ret, img_binary = cv2.threshold(blur, i, 255, cv2.THRESH_BINARY)
        img_binary = ~img_binary

        text = pytesseract.image_to_string(img_binary, lang="kor+eng")
        text1 = []

        if text != "":
            print(text)
            for i in range(0, len(text)):
                if (text[i] >= "가" and text[i] <= "힣") or (
                    text[i] >= "0" and text[i] <= "9"
                ):
                    text1.append(text[i])

        text2 = "".join(text1)
        now = datetime.datetime.now()
        iso = now.isoformat()
        if len(text2) >= 7 and fail_count == 2:
            final_result1 = frame_dect(text2)
            encoding_image(final_result1, iso)
            fail_count = 0
            break

        final_result = frame_dect(text2)

        try:  # 입주자/방문자 조회 후 출입기록 url로 post
            ur = jsonurl()

            if flag == True:
                body = {
                    "carnumber": final_result[0],
                    "typeofentrysandexit": "출차",
                    "exitdatetime": iso,
                }
                response = requests.post(
                    ur.parking_endpoint,
                    headers=headers,
                    data=json.dumps(body, ensure_ascii=False).encode("utf8"),
                )
            else:
                body = {
                    "carnumber": final_result[0],
                    "typeofentrysandexit": "입차",
                    "entrydatetime": iso,
                }
                response = requests.post(
                    ur.parking_endpoint,
                    headers=headers,
                    data=json.dumps(body, ensure_ascii=False).encode("utf8"),
                )

            print("response status %r" % response.status_code)
            print("response text %r" % response.text)

            if response.status_code == 201:
                servo_setting()
                fail_count = 0
                print("성공")
                break
        except:
            pass

        cv2.imshow("image", img_binary)
        cv2.waitKey(1)


def frame_dect(text):  # 글자 형식 맞추는 함수
    carnum_list = []
    str_count = 0

    for i in range(0, len(text)):
        if text[i] >= "가" and text[i] <= "힣":
            carnum_list.append(text[i])
            carnum_list.append(" ")
            str_count = 0
        else:
            str_count += 1
            if str_count == 5:
                carnum_list.append(",")
                str_count = 0
            carnum_list.append(text[i])

    carnum_result = "".join(carnum_list)
    final_result = carnum_result.split(",")

    print(final_result)
    return final_result


if __name__ == "__main__":
    comingcar_dect()

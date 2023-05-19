"""5/19 : 주차 상태에 따라 서버로 보내는 값 수정"""

# 필요 라이브러리
# 라즈베리파이 포트 및 LED
import RPi.GPIO as GPIO  # OLED
import os
import time
from waveshare_OLED import OLED_0in96
from PIL import Image, ImageDraw, ImageFont
import threading  # Thread
import json
import requests
from flask import Flask, render_template, request, Response, jsonify
from Cam_tess import *
import cv2

url_host = "http://192.168.0.19:9000"
locate = "/insidetheparkinglot/"
app = Flask(__name__)


# 기초 세팅 및 전역변수 설정
def base_set():
    global Parking_lot_Data  # 주차장 데이터
    global Emergency  # 화재 감지 등 비상상황
    global user_select
    global fsenser_pin
    global Select_Point
    global CarNum
    global parktrue
    global refer_distance

    Parking_lot_Data = {
        "linenum": 1,
        "fsens": 12,
        "pitem": {
            "A-1": {"rl": 17, "gl": 27, "trig": 22, "echo": 18, "lednum": 1},
            "B-1": {"rl": 10, "gl": 9, "trig": 23, "echo": 24, "lednum": 3},
            "C-1": {"rl": 25, "gl": 8, "trig": 16, "echo": 20, "lednum": 5},
            "D-1": {"rl": 25, "gl": 8, "trig": 16, "echo": 20, "lednum": 5},
        },
        "litem": {"l1": 5, "l2": 6, "l3": 13, "l4": 19, "l5": 26},
        "seatnumber": {"A-1": 1, "B-1": 2, "C-1": 3, "D-1": 4},
    }
    Emergency = False
    user_select = False
    Select_Point = ""
    CarNum = ""
    parktrue = {}
    # 초음파 기준 거리
    refer_distance = 7

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # 화재감지센서 세팅
    fsenser_pin = Parking_lot_Data.get("fsens")
    GPIO.setup(fsenser_pin, GPIO.IN)

    time.sleep(2)


# thread function or class
# 각 자리 초음파 체크 및 RGB LED로 상태 체크 모듈
class parking_module(threading.Thread):
    def __init__(self, point, Parking_lot_Data, distance):
        super().__init__()
        self.state_set(point, Parking_lot_Data)
        parktrue.update({point: False})
        self.bef_state = False
        self.state_change = False
        self.point = point
        self.body = {}
        self.body["parking_generalseat"] = point
        self.body["parking_seatstate"] = False
        self.distance = distance

        temp = Parking_lot_Data.get("seatnumber")
        self.seatnumber = temp.get(point)
        time.sleep(0.5)

    def run(self):
        global user_select
        global Select_Point
        onoff = False

        while True:
            # print(self.body)
            if user_select == False:
                self.dis_check()
                if self.car:
                    GPIO.output(self.rl, True)
                    GPIO.output(self.gl, False)
                    parktrue[self.point] = True
                    if self.bef_state == True:
                        self.state_change = True
                        self.bef_state = False
                        self.body["parking_seatstate"] = True
                    # print(self.bef_state)
                else:
                    GPIO.output(self.rl, False)
                    GPIO.output(self.gl, True)
                    parktrue[self.point] = False
                    if self.bef_state == False:
                        self.state_change = True
                        self.bef_state = True
                        self.body["parking_seatstate"] = False
                    # print(self.bef_state)
                time.sleep(1)
            elif user_select and Select_Point == self.point:
                self.dis_check()
                if self.car:
                    user_select = False
                    if self.bef_state == True:
                        self.state_change = True
                        self.bef_state = False
                        self.body["parking_seatstate"] = True
                else:
                    onoff = not onoff
                    GPIO.output(self.rl, onoff)
                    GPIO.output(self.gl, onoff)
                    if self.bef_state == False:
                        self.state_change = True
                        self.bef_state = True
                        self.body["parking_seatstate"] = False
                time.sleep(1)

    def state_set(self, point, data):
        pitem = data.get("pitem")
        spot = pitem.get(point)
        self.rl = spot.get("rl")
        self.gl = spot.get("gl")
        self.trig = spot.get("trig")
        self.echo = spot.get("echo")

        GPIO.setup(self.rl, GPIO.OUT)
        GPIO.setup(self.gl, GPIO.OUT)
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)

        time.sleep(2)

    def dis_check(self):
        dis = self.uss_distance()
        if dis > self.distance:
            self.car = False
        else:
            self.car = True

    def uss_distance(self):
        start = 0
        stop = 0
        GPIO.output(self.trig, True)
        time.sleep(0.00001)
        GPIO.output(self.trig, False)

        while GPIO.input(self.echo) == 0:
            start = time.time()
        while GPIO.input(self.echo) == 1:
            stop = time.time()
        check = stop - start
        # print(self.point + " : " + str(check * 34300 / 2))
        return check * 34300 / 2


# 화재 감지 모듈
def flame_check():
    global emergency
    while True:
        if GPIO.input(fsenser_pin) == 0:
            emergency = True
            break
        time.sleep(0.5)


# oled 및 차량 유도
class parking_guidance(threading.Thread):
    def __init__(self, parking_lot_data):
        super().__init__()
        self.parking_set()
        self.parking_lot = parking_lot_data
        self.display = OLED_0in96.OLED_0in96()
        self.background_img = Image.new(
            "1", (self.display.width, self.display.height), 255
        )
        self.draw = ImageDraw.Draw(self.background_img)
        self.reset()

    def run(self):
        global user_select
        global Select_Point
        while True:
            self.view_oled()
            if user_select:
                self.view_usersel()
                self.light_on(Select_Point)
            time.sleep(1)
            self.reset()

    def parking_set(self):
        kor_font = "/home/pi/webapps/OLED_Module_Code/RaspberryPi/python/pic"
        self.Font_size = 20
        self.basic_font = ImageFont.truetype(
            os.path.join(kor_font, "Font.ttc"), self.Font_size
        )

        led_list = Parking_lot_Data.get("litem")
        for item in led_list:
            GPIO.setup(led_list.get(item), GPIO.OUT)
            GPIO.output(led_list.get(item), False)
        time.sleep(2)

    def reset(self):
        self.background_img = Image.new(
            "1", (self.display.width, self.display.height), 255
        )
        self.draw = ImageDraw.Draw(self.background_img)

    def view_oled(self):
        num = 0
        for val in parktrue.values():
            if val == False:
                num += 1
        txt = "남은 자리 : " + str(num)
        px = (32 - self.Font_size) / 2
        self.draw.text((3, px), txt, fill=0, font=self.basic_font)
        self.display.ShowImage(self.display.getbuffer(self.background_img))

    def view_usersel(self):
        global CarNum
        px = (32 - self.Font_size) / 2
        self.draw.text((3, 32 + px), "← " + CarNum, fill=0, font=self.basic_font)
        self.display.ShowImage(self.display.getbuffer(self.background_img))

    def light_on(self, Sel_Point):
        pitem = self.parking_lot.get("pitem")
        sel_parking = pitem.get(Sel_Point)
        led_set = list(self.parking_lot.get("litem").values())
        print(sel_parking.get("lednum"))
        while user_select:
            for num in range(0, int(sel_parking.get("lednum"))):
                GPIO.output(led_set[num], True)
                time.sleep(0.1)
            for num in range(0, int(sel_parking.get("lednum"))):
                GPIO.output(led_set[num], False)
                time.sleep(0.1)
        for num in range(0, int(sel_parking.get("lednum"))):
            GPIO.output(led_set[num], False)
            time.sleep(0.1)


# API Data 받아오기
def send_api(API_HOST, path, method, body):
    url = API_HOST + path
    # print(url)
    # print(body)
    headers = {
        # "Authorization": "ToKen 750b311fec4b7c0a2a023bd557a149fb1f3a5085",  # 토큰값
        "Content-Type": "application/json",
        "charset": "UTF-8",
        "Accept": "*/*",
    }

    try:
        if method == "GET":
            response = requests.get(url, headers=headers)

        elif method == "PUT":
            response = requests.put(
                url,
                headers=headers,
                data=json.dumps(body, ensure_ascii=False).encode("utf8"),
            )
        elif method == "POST":
            response = requests.post(
                url,
                headers=headers,
                data=json.dumps(body, ensure_ascii=False).encode("utf8"),
            )
        else:
            print("CMD error")
        print("response status %r" % response.status_code)
        # print("response text %r" % response.text)
    except Exception as ex:
        # print(ex)
        print("Error")


# API로 주차 위치 받기
@app.route("/parking")
def user_parking():
    global Select_Point
    global user_select
    select = request.args.get("locate", "error")
    pitem = Parking_lot_Data.get("pitem")
    print(select)
    for item in pitem:
        if select == item:
            Select_Point = select
            try:
                if parktrue[Select_Point] == True:
                    print("Already Parking")
                    return "Already Parking"
                else:
                    user_select = True
                    return "Parking to " + Select_Point
            except:
                return "It is a place that does not exist."


# 주차장 내 CCTV
def video_stream():
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 500)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 500)
    try:
        while True:
            success, frame = camera.read()
            if not success:
                print("breaking")
                time.sleep(0.1)
                continue
            else:
                ret, buffer = cv2.imencode(".jpg", frame)
                cv2.imwrite("./cap02.jpg", frame)
                frame = buffer.tobytes()
                yield (
                    b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
                )
    except:
        print("breakk")


@app.route("/video_feed")
def video_feed():
    return Response(
        video_stream(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


# server 열기
def start_server():
    app.run(host="0.0.0.0", port=7800, threaded=True)


# main 함수
if __name__ == "__main__":
    global user_select
    global Select_Point
    global CarNum

    base_set()

    # parking thread 작성
    A1 = parking_module("A-1", Parking_lot_Data, refer_distance)
    B1 = parking_module("B-1", Parking_lot_Data, refer_distance)
    C1 = parking_module("C-1", Parking_lot_Data, refer_distance)
    flame = threading.Thread(target=flame_check)
    Guidance = parking_guidance(Parking_lot_Data)
    server = threading.Thread(target=start_server)
    cam = threading.Thread(target=comingcar_dect)

    A1.daemon = True
    B1.daemon = True
    C1.daemon = True
    flame.daemon = True
    Guidance.daemon = True
    server.daemon = True
    cam.daemon = True

    A1.start()
    B1.start()
    C1.start()
    flame.start()
    Guidance.start()
    server.start()
    cam.start()

    time.sleep(10)

    A1.state_change = False
    B1.state_change = False
    C1.state_change = False

    while True:
        if Emergency:
            print(
                "Emergency"
                + time.strftime("%Y-%m-%d %p %I:%M:%S", time.localtime(time.time()))
            )
            emergency_url = "http://192.168.0.19:9000/safetyaccident/"
            emergency_body = {
                "safetyaccident_datetime": time.strftime(
                    "%Y-%m-%dT%H:%M:%S+09:00", time.localtime(time.time())
                ),
                "safetyaccident_kind": "화재 감지",
            }
            send_api(url_host, "/safetyaccident/", "POST", emergency_body)
            break

        if A1.state_change:
            print("A1 state change")
            # 각 자리 차량의 유무에 따라 차 번호 시트 값이 변화
            if A1.car:
                color_img = cv2.imread("./cap02.jpg", cv2.IMREAD_COLOR)
                numdata = carnum_output(color_img)
                A1.body["parking_seatcarnumber"] = numdata.get("A-1")
            else:
                A1.body["pakring_seatcarnumber"] = "None"
            # print(A1.body)

            send_api(url_host, locate + str(A1.seatnumber), "PUT", A1.body)
            A1.state_change = False
        if B1.state_change:
            print("B1 state change")
            if B1.car:
                color_img = cv2.imread("./cap02.jpg", cv2.IMREAD_COLOR)
                numdata = carnum_output(color_img)
                B1.body["parking_seatcarnumber"] = numdata.get("B-1")
            else:
                B1.body["pakring_seatcarnumber"] = "None"

            # print(B1.body)

            send_api(url_host, locate + str(B1.seatnumber), "PUT", B1.body)
            B1.state_change = False
        if C1.state_change:
            print("C1 state change")
            if C1.car:
                color_img = cv2.imread("./cap02.jpg", cv2.IMREAD_COLOR)
                numdata = carnum_output(color_img)
                C1.body["parking_seatcarnumber"] = numdata.get("C-1")
            else:
                C1.body["pakring_seatcarnumber"] = "None"

            send_api(url_host, locate + str(C1.seatnumber), "PUT", C1.body)
            C1.state_change = False

        time.sleep(1)

import cv2
import numpy as np
import RPi.GPIO as GPIO
import pytesseract
import requests
import json

WIDTH = 640
HEIGHT = 480

headers = {
    # "Authorization": "ToKen 750b311fec4b7c0a2a023bd557a149fb1f3a5085",  # 토큰값
    "Content-Type": "application/json",
    "charset": "UTF-8",
    "Accept": "*/*",
}


def rect_line(img):
    cv2.rectangle(img, (0, 0), (213 - 1, 480 - 1), (0, 0, 255), 2)
    cv2.rectangle(img, (213, 0), (426 - 1, 480 - 1), (0, 255, 0), 2)
    cv2.rectangle(img, (426, 0), (640 - 1, 480 - 1), (255, 0, 0), 2)


data = {"A-1": "", "B-1": "", "C-1": ""}
flag1 = False
flag2 = False
flag3 = False
fail_count = 0
count = 0


def carnum_print(text):
    text1 = []
    if text != "":
        print(text)
        for i in range(0, len(text)):
            if (text[i] >= "가" and text[i] <= "힣") or (
                text[i] >= "0" and text[i] <= "9"
            ):
                text1.append(text[i])
    text_answer = "".join(text1)
    return text_answer


def carnum_output(color_img):
    car_area = ["A-1", "B-1"]  # 가정: 초음파에서 측정된  주차 구역
    print(car_area)
    parking_endpoint = "http://192.168.0.19:9000/insidetheparkinglot/"
    global data
    global flag1
    global flag2
    global flag3
    global fail_count
    global count

    height, width, _ = color_img.shape

    # 가로 방향 분할
    part_width = width // 3
    part1 = color_img[:, :part_width]
    part2 = color_img[:, part_width : part_width * 2]
    part3 = color_img[:, part_width * 2 :]

    img_gray1 = cv2.cvtColor(part1, cv2.COLOR_BGR2GRAY)
    img_gray2 = cv2.cvtColor(part2, cv2.COLOR_BGR2GRAY)
    img_gray3 = cv2.cvtColor(part3, cv2.COLOR_BGR2GRAY)

    flag_fail = False
    count = 0
    fail_count += 1
    for i in range(15, 120, 2):  # 150, 240
        ret, img_binary1 = cv2.threshold(img_gray1, i, 255, cv2.THRESH_BINARY)
        ret, img_binary2 = cv2.threshold(img_gray2, i, 255, cv2.THRESH_BINARY)
        ret, img_binary3 = cv2.threshold(img_gray3, i, 255, cv2.THRESH_BINARY)
        # img_binary = ~img_binary

        text_1 = pytesseract.image_to_string(img_binary1, lang="kor+eng")
        text_2 = pytesseract.image_to_string(img_binary2, lang="kor+eng")
        text_3 = pytesseract.image_to_string(img_binary3, lang="kor+eng")

        text_answer1 = carnum_print(text_1)
        text_answer2 = carnum_print(text_2)
        text_answer3 = carnum_print(text_3)

        final_result1 = frame_dect(text_answer1)  # 인식된 차 번호
        final_result2 = frame_dect(text_answer2)
        final_result3 = frame_dect(text_answer3)

        if len(car_area) == count:
            break

        print(fail_count)
        print(count)

        try:
            if fail_count == 2:
                if len(text_answer1) >= 7 and data["A-1"] == "":
                    data["A-1"] = final_result1[0]
                    fail_count = 0
                    flag_fail = False
                    flag1 = False
                    flag2 = False
                    flag3 = False
                    break
                if len(text_answer2) >= 7 and data["B-1"] == "":
                    data["B-1"] = final_result2[0]
                    fail_count = 0
                    flag_fail = False
                    flag1 = False
                    flag2 = False
                    flag3 = False
                    break
                if len(text_answer3) >= 7 and data["C-1"] == "":
                    data["C-1"] = final_result3[0]
                    fail_count = 0
                    flag_fail = False
                    flag1 = False
                    flag2 = False
                    flag3 = False
                    break
        except:
            pass

        if flag1 == False:
            area = "A-1"
            flag1 = response_post(final_result1[0], parking_endpoint, area, flag1)

        if flag2 == False:
            area = "B-1"
            flag2 = response_post(final_result2[0], parking_endpoint, area, flag2)

        if flag3 == False:
            area = "C-1"
            flag3 = response_post(final_result3[0], parking_endpoint, area, flag3)

        if fail_count == 1 and flag_fail == False:
            data = {"A-1": "", "B-1": "", "C-1": ""}
            flag_fail = True

        cv2.imshow("image1", img_binary1)
        cv2.imshow("image2", img_binary2)
        cv2.imshow("image3", img_binary3)
        cv2.waitKey(1)

    cv2.destroyAllWindows()
    print(data)


def response_post(final_result, parking_endpoint, area, flag):
    global count
    body = {"parking_seatnumber": final_result}
    response = requests.post(
        parking_endpoint,
        headers=headers,
        data=json.dumps(body, ensure_ascii=False).encode("utf8"),
    )
    print("response text %r" % response.text)
    dic = eval(response.text)
    if dic["state"] == "입" or dic["state"] == "방":
        if flag == False:
            data[area] = final_result
            print(data[area])
            count += 1
            flag = True
    return flag


def comingcar_dect():
    camera = cv2.VideoCapture(0)
    global WIDTH
    global HEIGHT
    print(WIDTH)
    camera.set(3, WIDTH)
    camera.set(4, HEIGHT)

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # 초음파로 바꿔줘
    button_pin = 15
    GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(button_pin, GPIO.RISING, bouncetime=300)

    while True:
        _, frame = camera.read()
        rect_line(frame)  # 영상에 사각형 구분 라인
        cv2.imshow("Frame", frame)
        cv2.waitKey(100)
        if GPIO.input(button_pin) == GPIO.HIGH:  # 초음파로 바꿔줘
            print("Button pushed!")
            cv2.imwrite("./cap02.jpg", frame)
            # cv2.imwrite("./cap03.jpg", frame)
            color_img = cv2.imread("./cap02.jpg", cv2.IMREAD_COLOR)
            carnum_output(color_img)
            cv2.destroyAllWindows()


def frame_dect(text):  # 영상에서 인식된 차번호 검출
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

    print(carnum_list)
    carnum_result = "".join(carnum_list)
    print(carnum_result)
    final_result = carnum_result.split(",")

    print(final_result)
    return final_result


if __name__ == "__main__":
    comingcar_dect()

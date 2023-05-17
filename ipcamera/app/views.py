from django.shortcuts import render
import cv2
import threading
from django.views.decorators import gzip
from django.http import StreamingHttpResponse

# from models import CameraImage


# Create your views here.
def home(request):
    return render(request, "home.html")


class VideoCamera_CarIO(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        self.is_running = True
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.is_running = False
        self.video.release()

    def get_frame(self):
        image = self.frame
        ret, jpeg = cv2.imencode(".jpg", image)
        return jpeg.tobytes()

    def update(self):
        while self.is_running:
            (self.grabbed, self.frame) = self.video.read()


def gen(camera):
    try:
        while True:
            frame = camera.get_frame()
            yield (
                b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n"
            )
    except:
        camera.is_running = False


@gzip.gzip_page
def cam_stream_IO(request):
    cam = VideoCamera_CarIO()
    try:
        return StreamingHttpResponse(
            gen(cam), content_type="multipart/x-mixed-replace; boundary=frame"
        )
    except:
        pass


# def test(request):
#     if request.method == "POST":
#         image = request.FILES.get("camera-image")
#         CameraImage.objects.create(image=image)
#     images = CameraImage.objects.all()
#     context = {"images": images}
#     return render(request, "camera_view.html", context)


# @gzip.gzip_page
# def detectme(request):
#     try:
#         # cam = VideoCamera()  # 웹캠 호출
#         # frame단위로 이미지를 계속 송출한다
#         return StreamingHttpResponse(
#             gen(cam), content_type="multipart/x-mixed-replace;boundary=frame"
#         )
#     except cv2.error as e:
#         print(e)
#         for k in dir(e):
#             if k[0:2] != "__":
#                 print("e.%s = %s" % (k, getattr(e, k)))

#         # handle error: empty frame
#         if e.err == "!_src.empty()":
#             pass

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers
from . import models
import hashlib
import requests
from django.db import connection
from django.db.models import Max, F
from django.db import IntegrityError


class residents_informationViewSet(viewsets.ModelViewSet):
    queryset = models.residents_information.objects.all()
    serializer_class = serializers.residents_informationSerializer


class insidetheparkinglotViewSet(viewsets.ModelViewSet):
    queryset = models.insidetheparkinglot.objects.all()
    serializer_class = serializers.insidetheparkinglotSerializer


# class parkinglotViewSet(viewsets.ModelViewSet):
#     queryset = models.parkinglot.objects.all()
#     serializer_class = serializers.parkinglotSerializer


class entrancetotheparkinglotViewSet(viewsets.ModelViewSet):
    queryset = models.entrancetotheparkinglot.objects.all()
    serializer_class = serializers.entrancetotheparkinglotSerializer


class unauthorized_parkinglotViewSet(viewsets.ModelViewSet):
    queryset = models.unauthorized_parking.objects.all()
    serializer_class = serializers.unauthorized_parkingSerializer


class visitor_informationViewSet(viewsets.ModelViewSet):
    queryset = models.visitor_information.objects.all()
    serializer_class = serializers.visitor_informationSerializer


class safetyaccidentViewSet(viewsets.ModelViewSet):
    queryset = models.safetyaccident.objects.all()
    serializer_class = serializers.safetyaccidentSerializer


class loginforAdministratorViewSet(viewsets.ModelViewSet):
    queryset = models.loginforAdministrator.objects.all()
    serializer_class = serializers.loginforAdministratorSerializer


# class loginforClientViewSet(viewsets.ModelViewSet):
#     queryset = models.loginforClient.objects.all()
#     serializer_class = serializers.loginforClientSerializer


class questionViewSet(viewsets.ModelViewSet):
    queryset = models.question.objects.all()
    serializer_class = serializers.questionSerializer


class answerViewSet(viewsets.ModelViewSet):
    queryset = models.answer.objects.all()
    serializer_class = serializers.answerSerializer


class residents_informationAPIView(APIView):
    def get(self, request):
        # permission_classes = (IsAuthenticated,)
        queryset = models.residents_information.objects.all()
        serializer_class = serializers.residents_informationSerializer(queryset, many=True)
        return Response(serializer_class.data)

    def post(self, request):  #순번 에러 뜰때초기화
        try:
            user = models.residents_information.objects.get(resident_phone=request.data.get('resident_phone'))
            users = models.residents_information.objects.get(resident_carnumber=request.data.get('resident_carnumber'))
            return Response(user)
        except models.residents_information.DoesNotExist:
            serializer_class = serializers.residents_informationSerializer(data=request.data)
            if serializer_class.is_valid():
                serializer_class.save()
                return Response(serializer_class.data, status=status.HTTP_201_CREATED)
            return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

class residents_informationdetailAPIView(APIView):

    def get(self, request, residents_number):
        # permission_classes = (IsAuthenticated,)
        queryset = models.residents_information.objects.get(residents_number=residents_number)
        serializer_class = serializers.residents_informationSerializer(queryset)
        return Response(serializer_class.data)

    def put(self, request, residents_number):
        # permission_classes = (IsAuthenticated,)
        queryset = models.residents_information.objects.get(residents_number=residents_number)
        serializer_class = serializers.residents_informationSerializer(queryset, data=request.data)

        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, residents_number):
        queryset = models.residents_information.objects.get(residents_number=residents_number)
        queryset.delete()

        # 마지막 데이터를 삭제한 경우에만 초기화
        last_data = models.residents_information.objects.last()
        if last_data is None:
            cursor = connection.cursor()
            cursor.execute("ALTER TABLE residents_information AUTO_INCREMENT=1;")

        models.residents_information.objects.filter(residents_number__gt=residents_number).update(
            residents_number=F('residents_number') - 1)

        # 가장 큰 residents_number 가져오기
        max_residents_number = \
            models.residents_information.objects.aggregate(max_residents_number=Max('residents_number'))[
                'max_residents_number']
        if max_residents_number is not None:
            cursor = connection.cursor()
            cursor.execute(f"ALTER TABLE residents_information AUTO_INCREMENT={max_residents_number + 1};")

        return Response(status=status.HTTP_204_NO_CONTENT)


class insidetheparkinglotAPIView(APIView):
    def get(self, request):
        # permission_classes = (IsAuthenticated,)
        queryset = models.insidetheparkinglot.objects.all()
        serializer_class = serializers.insidetheparkinglotSerializer(queryset, many=True)
        return Response(serializer_class.data)

    def post(self, request):
        parking_seatcarnumber = request.data.get('parking_seatnumber')
        print(request.data)
        data = {}
        if not parking_seatcarnumber:
            data = {
                'state': 'nodata'
            }
            return Response(data)

        ExceptionType1 = models.residents_information.DoesNotExist
        ExceptionType2 = models.visitor_information.DoesNotExist
        try:
            user = models.residents_information.objects.get(resident_carnumber=parking_seatcarnumber)
            data = {'state': '입'}
            return Response(data)
        except ExceptionType1:
            try:
                users = models.visitor_information.objects.get(visitor_information_carnumber=parking_seatcarnumber)
                data = {'state': '방'}
                return Response(data)
            except ExceptionType2:
                data = {
                    'state': '비인가'
                }
                return Response(data)


class insidetheparkinglotdetailAPIView(APIView):

    def get(self, request, parking_seatnumber):
        # permission_classes = (IsAuthenticated,)
        queryset = models.insidetheparkinglot.objects.get(parking_seatnumber=parking_seatnumber)
        serializer_class = serializers.insidetheparkinglotSerializer(queryset)
        return Response(serializer_class.data)

    def put(self, request, parking_seatnumber):
        # permission_classes = (IsAuthenticated,)
        queryset = models.insidetheparkinglot.objects.get(parking_seatnumber=parking_seatnumber)
        serializer_class = serializers.insidetheparkinglotSerializer(queryset, data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, parking_seatnumber):
        queryset = models.insidetheparkinglot.objects.get(parking_seatnumber=parking_seatnumber)
        queryset.delete()

        # 마지막 데이터를 삭제한 경우에만 초기화
        last_data = models.insidetheparkinglot.objects.last()
        if last_data is None:
            cursor = connection.cursor()
            cursor.execute("ALTER TABLE insidetheparkinglot AUTO_INCREMENT=1;")

        models.insidetheparkinglot.objects.filter(parking_seatnumber__gt=parking_seatnumber).update(
            parking_seatnumber=F('parking_seatnumber') - 1)

        max_parking_seatnumber = \
            models.insidetheparkinglot.objects.aggregate(max_parking_seatnumber=Max('parking_seatnumber'))[
                'max_parking_seatnumber']
        if max_parking_seatnumber is not None:
            cursor = connection.cursor()
            cursor.execute(f"ALTER TABLE insidetheparkinglot AUTO_INCREMENT={max_parking_seatnumber + 1};")

        return Response(status=status.HTTP_204_NO_CONTENT)


class parkinglotAPIView(APIView):  #환희 한솔 데이터 주고 받는 코드

    def post(self, request):
        resident_dong = request.data.get('resident_dong')
        resident_ho = request.data.get('resident_ho')
        parking_generalseat = request.data.get('parking_generalseat')
        print(request.data)
        try:
            parking_lot = models.insidetheparkinglot.objects.get(parking_generalseat=parking_generalseat)
            if parking_lot.parking_seatstate:
                return Response(dict(state='no'))
            else:
                try:
                    user = models.residents_information.objects.get(resident_dong=resident_dong,
                                                                    resident_ho=resident_ho)

                except models.residents_information.DoesNotExist:
                    return Response(dict(error="no"))

                url = f'http://192.168.0.220:7800/parking?locate={parking_generalseat}'
                response = requests.get(url)
                if response.status_code == 200:
                    url = f'http://192.168.0.175:5000/parking_lot'
                    responses = requests.get(url)

                else:
                    print(f"Error: {response.status_code} - {response.reason}")
                return Response(dict(state='ok'))
        except models.insidetheparkinglot.DoesNotExist:
            return Response(dict(state='fuck'))



class entrancetotheparkinglotAPIView(APIView):
    def get(self, request):
        # permission_classes = (IsAuthenticated,)
        queryset = models.entrancetotheparkinglot.objects.all()
        serializer_class = serializers.entrancetotheparkinglotSerializer(queryset, many=True)
        return Response(serializer_class.data)

    def post(self, request):
        # permission_classes = (IsAuthenticated,)
        carnumber = request.data.get('carnumber', "")
        typeofentrysandexit = request.data.get('typeofentrysandexit')
        entrydatetime = request.data.get('entrydatetime')
        exitdatetime = request.data.get('exitdatetime')

        data = {}
        if not carnumber:
            data = {
                'state': 'nodata'
            }
            return Response(data)

        ExceptionType1 = models.residents_information.DoesNotExist
        ExceptionType2 = models.visitor_information.DoesNotExist
        try:
            user = models.residents_information.objects.get(resident_carnumber=carnumber)
            person_check = '입주자'
            users = None
        except ExceptionType1:
            try:
                user = None
                users = models.visitor_information.objects.get(visitor_information_carnumber=carnumber)
                person_check = '방문자'
            except ExceptionType2:
                data = {
                    'state': 'no'
                }
                return Response(data)
            else:
                pass

        if user:
            resident_dong = user.resident_dong
            resident_ho = user.resident_ho
            data = {
                'carnumber': user.resident_carnumber,
                'typeofentrysandexit': typeofentrysandexit,
                'entrydatetime': entrydatetime,
                'exitdatetime': exitdatetime,
                'resident_dong': resident_dong,
                'resident_ho': resident_ho,
                'person_check ': person_check

            }
        elif users:
            resident_dong = users.resident_dong
            resident_ho = users.resident_ho

            data = {
                'carnumber': users.visitor_information_carnumber,
                'typeofentrysandexit': typeofentrysandexit,
                'entrydatetime': entrydatetime,
                'exitdatetime': exitdatetime,
                'resident_dong': resident_dong,
                'resident_ho': resident_ho,
                'person_check': person_check,
            }
        serializer_class = serializers.entrancetotheparkinglotSerializer(data=data)
        if serializer_class.is_valid():
            serializer_class.save()
            data = {
                'state': 'ok'
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status.HTTP_400_BAD_REQUEST)


class entrancetotheparkinglotdetailAPIView(APIView):

    def get(self, request, parking_log_number):
        # permission_classes = (IsAuthenticated,)
        queryset = models.entrancetotheparkinglot.objects.get(parking_log_number=parking_log_number)
        serializer_class = serializers.entrancetotheparkinglotSerializer(queryset)
        return Response(serializer_class.data)

    def put(self, request, parking_log_number):
        # permission_classes = (IsAuthenticated,)
        queryset = models.entrancetotheparkinglot.objects.get(parking_log_number=parking_log_number)
        serializer_class = serializers.entrancetotheparkinglotSerializer(queryset, data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, parking_log_number):
        queryset = models.entrancetotheparkinglot.objects.get(parking_log_number=parking_log_number)
        queryset.delete()
        last_data = models.entrancetotheparkinglot.objects.last()
        if last_data is None:
            cursor = connection.cursor()
            cursor.execute("ALTER TABLE entrancetotheparkinglot AUTO_INCREMENT=1;")

        models.entrancetotheparkinglot.objects.filter(parking_log_number__gt=parking_log_number).update(
            parking_log_number=F('parking_log_number') - 1)

        max_parking_log_number = \
            models.entrancetotheparkinglot.objects.aggregate(max_parking_log_number=Max('parking_log_number'))[
                'max_parking_log_number']
        if max_parking_log_number is not None:
            cursor = connection.cursor()
            cursor.execute(f"ALTER TABLE entrancetotheparkinglot AUTO_INCREMENT={max_parking_log_number + 1};")

        return Response(status=status.HTTP_204_NO_CONTENT)


class unauthorized_parkingAPIView(APIView):
    def get(self, request):
        # permission_classes = (IsAuthenticated,)
        queryset = models.unauthorized_parking.objects.all()
        serializer_class = serializers.unauthorized_parkingSerializer(queryset, many=True)
        return Response(serializer_class.data)

    def post(self, request):
        # permission_classes = (IsAuthenticated,)a
        unauthorized_carnumber = request.data.get('unauthorized_carnumber')
        unauthorized_carnumbers = request.data.get('unauthorized_carnumbers')
        typeofentrysandexit = request.data.get('typeofentrysandexit')
        entrydatetime = request.data.get('entrydatetime')
        exitdatetime = request.data.get('exitdatetime')
        resident_dong = request.data.get('resident_dong')
        resident_ho = request.data.get('resident_ho')
        residents_doorpasswd = request.data.get('residents_doorpasswd')
        try:
            user = models.residents_information.objects.get(resident_dong=resident_dong, resident_ho=resident_ho,
                                                            residents_doorpasswd=residents_doorpasswd)
        except models.residents_information.DoesNotExist:
            return Response(dict(state='no'))

        data = {
            'unauthorized_carnumber': unauthorized_carnumber,
            'unauthorized_carnumbers': unauthorized_carnumbers,
            'typeofentrysandexit': typeofentrysandexit,
            'resident_dong': resident_dong,
            'resident_ho': resident_ho,
            'residents_doorpasswd': residents_doorpasswd,
            'entrydatetime': entrydatetime,
            'exitdatetime': exitdatetime,
        }

        serializer_class = serializers.unauthorized_parkingSerializer(data=data)
        if serializer_class.is_valid():
            serializer_class.save()
            data = {
                'state': 'ok'
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status.HTTP_400_BAD_REQUEST)


class unauthorized_parkingdetailAPIView(APIView):
    def get(self, request, parking_log_number):
        # permission_classes = (IsAuthenticated,)
        queryset = models.unauthorized_parking.objects.get(parking_log_number=parking_log_number)
        serializer_class = serializers.unauthorized_parkingSerializer(queryset)
        return Response(serializer_class.data)

    def put(self, request, parking_log_number):
        # permission_classes = (IsAuthenticated,)
        queryset = models.unauthorized_parking.objects.get(parking_log_number=parking_log_number)
        serializer_class = serializers.unauthorized_parkingSerializer(queryset, data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, parking_log_number):
        queryset = models.unauthorized_parking.objects.get(parking_log_number=parking_log_number)
        queryset.delete()
        last_data = models.unauthorized_parking.objects.last()
        if last_data is None:
            cursor = connection.cursor()
            cursor.execute("ALTER TABLE unauthorized_parking AUTO_INCREMENT=1;")

        models.unauthorized_parking.objects.filter(parking_log_number__gt=parking_log_number).update(
            parking_log_number=F('parking_log_number') - 1)

        max_parking_log_number = \
            models.unauthorized_parking.objects.aggregate(max_parking_log_number=Max('parking_log_number'))[
                'max_parking_log_number']
        if max_parking_log_number is not None:
            cursor = connection.cursor()
            cursor.execute(f"ALTER TABLE unauthorized_parking AUTO_INCREMENT={max_parking_log_number + 1};")

        return Response(status=status.HTTP_204_NO_CONTENT)


class visitor_informationAPIView(APIView):
    def get(self, request):
        # permission_classes = (IsAuthenticated,)
        queryset = models.visitor_information.objects.all()
        serializer_class = serializers.visitor_informationSerializer(queryset, many=True)
        return Response(serializer_class.data)

    def post(self, request):
        # permission_classes = (IsAuthenticated,)

        serializer_class = serializers.visitor_informationSerializer(data=request.data)

        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status.HTTP_400_BAD_REQUEST)


class visitor_informationdetailAPIView(APIView):
    def get(self, request, visitor_information_number):
        # permission_classes = (IsAuthenticated,)
        queryset = models.visitor_information.objects.get(visitor_information_number=visitor_information_number)
        serializer_class = serializers.visitor_informationSerializer(queryset)
        return Response(serializer_class.data)

    def put(self, request, visitor_information_number):
        # permission_classes = (IsAuthenticated,)
        queryset = models.visitor_information.objects.get(visitor_information_number=visitor_information_number)
        serializer_class = serializers.visitor_informationSerializer(queryset, data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, visitor_information_number):
        queryset = models.visitor_information.objects.get(visitor_information_number=visitor_information_number)
        queryset.delete()
        last_data = models.visitor_information.objects.last()
        if last_data is None:
            cursor = connection.cursor()
            cursor.execute("ALTER TABLE visitor_information AUTO_INCREMENT=1;")

        models.visitor_information.objects.filter(visitor_information_number__gt=visitor_information_number).update(
            visitor_information_number=F(' visitor_information_number') - 1)

        max_visitor_information_number = \
            models.visitor_information.objects.aggregate(
                max_visitor_information_number=Max('visitor_information_number'))[
                'max_visitor_information_number']
        if max_visitor_information_number is not None:
            cursor = connection.cursor()
            cursor.execute(f"ALTER TABLE visitor_information AUTO_INCREMENT={max_visitor_information_number + 1};")

        return Response(status=status.HTTP_204_NO_CONTENT)


class safetyaccidentAPIView(APIView):
    def get(self, request):
        # permission_classes = (IsAuthenticated,)
        queryset = models.safetyaccident.objects.all()
        serializer_class = serializers.safetyaccidentSerializer(queryset, many=True)
        return Response(serializer_class.data)

    def post(self, request):
        # permission_classes = (IsAuthenticated,)
        serializer_class = serializers.safetyaccidentSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        # permission_classes = (IsAuthenticated,)
        serializer_class = serializers.safetyaccidentSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()

            # Check if the safety accident was caused by the sensor
            if "열감지" in request.data.get("safetyaccident_kind", ""):
                # Send email to admin
                send_mail(
                    'Alert: Safety accident detected',
                    'A safety accident was detected by the temperature sensor. Please check the situation immediately.',
                    'noreply@example.com',
                    ['admin@example.com'],
                    fail_silently=False,
                )

                # 사용자에게 푸시 알림 보내기
                # 푸시 알림 서비스를 구현하고 푸시 알림을 보내려면 사용자의 장치 토큰을 얻어야 합니다
                # 다음은 FCM(Firebase Cloud Messaging)을 사용하여 푸시 알림을 보내는 샘플 코드입니다
                # fcm = FCMDevice.objects.filter(user=request.user).first()
                # if fcm:
                #     fcm.send_message(title="Safety Alert", body=""안전 사고가 감지되었습니다. 부디 안전하게 지내세요.")

            return Response(serializer_class.data, status=status.HTTP_201_CREATD)
        return Response(serializer_class.errors, status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer_class = serializers.SafetyAccidentSerializer(data=request.data)
        if serializer_class.is_valid():
            safety_accident_kind = request.data.get('safetyaccident_kind')

            if safety_accident_kind == '화재 감지':
                serializer_class.save()

                # 안전사고 발생 시, 관리자에게 알림을 보내는 코드
                send_mail(
                    '안전사고 발생 알림',
                    '화재가 감지되었습니다.',
                    settings.EMAIL_HOST_USER,
                    [settings.ADMIN_EMAIL],
                    fail_silently=False,
                )
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status.HTTP_400_BAD_REQUEST)


class WeatherWarningChecker:  #공공 api 가져오는거
    def __init__(self, api_key):
        self.api_key = "aF8LxXdiU1NpTwZamiqP7M5c7ivK8Lq0SAY5GeH5u4txEpDAo1SJL+jGB7HvmdszvawMSjPaOkkWED2rMZp9FQ=="
        self.url = "http://apis.data.go.kr/1360000/WthrWrnInfoService/getWthrWrnList"

    def check_weather_warnings(self, warning_type):
        today = datetime.date.today().strftime("%Y%m%d")
        params = {
            "serviceKey": self.api_key,
            "pageNo": "1",
            "numOfRows": "10",
            "dataType": "json",
            "fromTmFc": today,
            "toTmFc": today,
            "areaCode": "L1030200",
            "warningType": warning_type,
            "stnId": "232",
        }

        response = requests.get(self.url, params=params)
        data = response.json()

        warning_types = data["response"]["body"]["items"]["item"]["warningType"]
        if "4" in warning_types or "7" in warning_types or "8" in warning_types:
            if "4" in warning_types:
                send_mail(
                    "폭우 발생 알림",
                    "폭우가 발생했습니다.",
                    settings.EMAIL_HOST_USER,
                    [settings.ADMIN_EMAIL],
                    fail_silently=False,
                )
            if "7" in warning_types:
                send_mail(
                    "태풍 발생 알림",
                    "태풍이 발생했습니다.",
                    settings.EMAIL_HOST_USER,
                    [settings.ADMIN_EMAIL],
                    fail_silently=False,
                )
            if "8" in warning_types:
                send_mail(
                    "대설 발생 알림",
                    "대설이 발생했습니다.",
                    settings.EMAIL_HOST_USER,
                    [settings.ADMIN_EMAIL],
                    fail_silently=False,
                )
        else:
            print("No weather warnings for the given types")


class safetyaccidentdetailAPIView(APIView):
    def get(self, request, safetyaccident_number):
        # permission_classes = (IsAuthenticated,)
        queryset = models.safetyaccident.objects.get(
            safetyaccident_number=safetyaccident_number)
        serializer_class = serializers.safetyaccidentSerializer(queryset)
        return Response(serializer_class.data)

    def put(self, request, safetyaccident_number):
        # permission_classes = (IsAuthenticated,)
        queryset = models.safetyaccident.objects.get(
            safetyaccident_number=safetyaccident_number)
        serializer_class = serializers.safetyaccidentSerializer(queryset, data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, safetyaccident_number):
        queryset = models.safetyaccident.objects.get(safetyaccident_number=safetyaccident_number)
        queryset.delete()

        last_data = models.safetyaccident.objects.last()
        if last_data is None:
            cursor = connection.cursor()
            cursor.execute("ALTER TABLE safetyaccident AUTO_INCREMENT=1;")

        models.safetyaccident.objects.filter(safetyaccident_number__gt=safetyaccident_number).update(
            safetyaccident_number=F('safetyaccident_number') - 1)

        max_safetyaccident_number = \
            models.safetyaccident.objects.aggregate(max_safetyaccident_number=Max('safetyaccident_number'))[
                'max_safetyaccident_number']
        if max_safetyaccident_number is not None:
            cursor = connection.cursor()
            cursor.execute(f"ALTER TABLE safetyaccident AUTO_INCREMENT={max_safetyaccident_number + 1};")

        return Response(status=status.HTTP_204_NO_CONTENT)


class loginforAdministratorAPIView(APIView):

    def get(self, request):
        # permission_classes = (IsAuthenticated,)
        queryset = models.loginforAdministrator.objects.all()
        serializer_class = serializers.loginforAdministratorSerializer(queryset, many=True)
        return Response(serializer_class.data)

    def post(self, request):
        login_ID = request.data.get('login_ID', "")
        login_PassWd = request.data.get('login_PassWd', "")

        # 암호화된 세션값
        try:
            user = models.loginforAdministrator.objects.get(login_ID=login_ID)
        except models.loginforAdministrator.DoesNotExist:
            return Response(dict(error="해당 ID의 사용자가 없습니다."))

        if login_PassWd == user.login_PassWd:
            hashed = hashlib.sha256()
            hashed.update(login_ID.encode('utf-8'))
            user.session = hashed.hexdigest()
            user.save()
            data = {
                'error': "로그인 성공",
                'session': user.session
            }
            return Response(data)
        else:
            return Response(dict(error="로그인 실패. 패스워드 불일치"))


class loginAPIView(APIView):  # 로그인

    def get(self, request):
        # permission_classes = (IsAuthenticated,)
        queryset = models.loginforAdministrator.objects.all()
        serializer_class = serializers.loginforAdministratorSerializer(queryset, many=True)
        return Response(serializer_class.data)

    def post(self, request):
        # permission_classes = (IsAuthenticated,)
        session = request.data.get('session', "")  # 요청한걸
        user = models.loginforAdministrator.objects.filter(session=session).first()
        if user:
            return Response(dict(username=user.login_ID))
        else:
            return Response(dict(username="정보가 없습니다."))


class RegistUser(APIView):  # 회원가입
    def get(self, request):
        queryset = models.loginforAdministrator.objects.all()
        serializer_class = serializers.loginforAdministratorSerializer(queryset, many=True)
        return Response(serializer_class.data)

    def post(self, request):
        login_ID = request.data.get('login_ID', "")
        login_PassWd = request.data.get('login_PassWd', "")
        email = request.data.get('email', "")

        if models.loginforAdministrator.objects.filter(login_ID=login_ID).exists():
            data = {
                'error': "이미 존재하는 아이디입니다.",
            }
            return Response(data)
        else:
            hashed = hashlib.sha256()
            hashed.update(login_ID.encode('utf-8'))

            models.loginforAdministrator.objects.create(login_ID=login_ID, login_PassWd=login_PassWd, email=email,
                                                        session=hashed.hexdigest())
            data = {
                'error': None,
                'login_ID': login_ID,
                'session': hashed.hexdigest(),
            }
            return Response(data=data)


class Clientlogin(APIView):  # 환희 로그인
    def post(self, request):
        dong = request.data.get('dong', "")
        ho = request.data.get('ho', "")
        PassWd = request.data.get('PassWd', "")
        user = models.residents_information.objects.filter(resident_dong=dong, resident_ho=ho).first()
        if user is None:
            data = {
                'state': 'ID1'
            }
            return Response(data)
        else:
            if PassWd == user.login_PassWd:
                data = {
                    'state': 'OK',
                }
                return Response(data)
            else:
                data = {
                    'state': 'PASSWD'
                }
                return Response(data)


class ClientData(APIView):  # 환희 정보 가져가기
    def post(self, request):
        dong = request.data.get('dong', "")
        ho = request.data.get('ho', "")

        user = models.residents_information.objects.filter(resident_dong=dong, resident_ho=ho).first()
        if user is None:

            data = {
                'state': 'ID1'
            }
            return Response(data)
        else:

            data = {
                'state': 'OK',
                'resident_name': user.resident_name,
                'resident_dong_ho': f"{user.resident_dong}동{user.resident_ho}호",
                'resident_carnumber': user.resident_carnumber,
                'resident_typeofcar': user.resident_typeofcar,
                'resident_phone': user.resident_phone,
            }
            return Response(data)


class loginforAdministratordetailAPIView(APIView):
    def get(self, request, loginforAdministrator_number):
        # permission_classes = (IsAuthenticated,)
        queryset = models.loginforAdministrator.objects.get(
            loginforAdministrator_number=loginforAdministrator_number)
        serializer_class = serializers.loginforAdministratorSerializer(queryset)
        return Response(serializer_class.data)

    def put(self, request, loginforAdministrator_number):
        # permission_classes = (IsAuthenticated,)
        queryset = models.loginforAdministrator.objects.get(
            loginforAdministrator_number=loginforAdministrator_number)
        serializer_class = serializers.loginforAdministratorSerializer(queryset, data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, loginforAdministrator_number):
        queryset = models.loginforAdministrator.objects.get(loginforAdministrator_number=loginforAdministrator_number)
        queryset.delete()

        last_data = models.loginforAdministrator.objects.last()
        if last_data is None:
            cursor = connection.cursor()
            cursor.execute("ALTER TABLE loginforAdministrator AUTO_INCREMENT=1;")

        models.loginforAdministrator.objects.filter(
            loginforAdministrator_number__gt=loginforAdministrator_number).update(
            loginforAdministrator_number=F('loginforAdministrator_number') - 1)

        max_loginforAdministrator_number = \
            models.loginforAdministrator.objects.aggregate(
                max_loginforAdministrator_number=Max('loginforAdministrator_number'))[
                'max_loginforAdministrator_number']
        if max_loginforAdministrator_number is not None:
            cursor = connection.cursor()
            cursor.execute(f"ALTER TABLE loginforAdministrator AUTO_INCREMENT={max_loginforAdministrator_number + 1};")

        return Response(status=status.HTTP_204_NO_CONTENT)


class loginforClientAPIView(APIView):
    def get(self, request):
        # permission_classes = (IsAuthenticated,)
        queryset = models.loginforClient.objects.all()
        serializer_class = serializers.loginforClientSerializer(queryset, many=True)
        return Response(serializer_class.data)

    def post(self, request):
        # permission_classes = (IsAuthenticated,)
        login_ID = request.data.get('login_ID', "")
        login_PassWd = request.data.get('login_PassWd', "")
        user = models.loginforClient.objects.filter(login_ID=login_ID).first()
        if user is None:
            data = {
                'state': 'ID'
            }
            return Response(data)
        if login_PassWd == user.login_PassWd:
            data = {
                'state': 'OK'
            }
            return Response(data)
        else:
            data = {
                'state': 'PASSWD'
            }
            return Response(data)


class Clientregistration(APIView):  # 회원가입
    def get(self, request):
        queryset = models.loginforClient.objects.all()
        serializer_class = serializers.loginforClientSerializer(queryset, many=True)
        return Response(serializer_class.data)

    def post(self, request):
        login_ID = request.data.get('login_ID', "")
        login_PassWd = request.data.get('login_PassWd', "")
        # email = request.data.get('email', "")  #이부분 resident_information
        print(login_ID)
        if models.loginforClient.objects.filter(login_ID=login_ID).exists():
            data = {
                'error': "이미 존재하는 아이디입니다.",
            }
            return Response(data)
        else:
            models.loginforClient.objects.create(login_ID=login_ID, login_PassWd=login_PassWd)
            data = {
                'error': None,
                'login_ID': login_ID,
            }
            return Response(data=data)


class loginforClientdetailAPIView(APIView):
    def get(self, request, loginforClient_number):
        # permission_classes = (IsAuthenticated,)
        queryset = models.loginforClient.objects.get(
            loginforClient_number=loginforClient_number)
        serializer_class = serializers.loginforClientSerializer(queryset)
        return Response(serializer_class.data)

    def put(self, request, loginforClient_number):
        # permission_classes = (IsAuthenticated,)
        queryset = models.loginforClient.objects.get(
            loginforClient_number=loginforClient_number)
        serializer_class = serializers.loginforClientSerializer(queryset, data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, loginforClient_number):
        queryset = models.loginforClient.objects.get(loginforClient_number=loginforClient_number)
        queryset.delete()

        last_data = models.loginforClient.objects.last()
        if last_data is None:
            cursor = connection.cursor()
            cursor.execute("ALTER TABLE loginforClient AUTO_INCREMENT=1;")
        models.loginforClient.objects.filter(loginforClient_number__gt=loginforClient_number).update(
            loginforClient_number=F('loginforClient_number') - 1)

        max_loginforClient_number = \
            models.loginforClient.objects.aggregate(
                max_loginforClient_number=Max('loginforClient_number'))[
                'max_loginforClient_number']
        if max_loginforClient_number is not None:
            cursor = connection.cursor()
            cursor.execute(f"ALTER TABLE loginforClient AUTO_INCREMENT={max_loginforClient_number + 1};")

        return Response(status=status.HTTP_204_NO_CONTENT)


class questionAPIView(APIView):
    def get(self, request):
        # permission_classes = (IsAuthenticated,)
        queryset = models.question.objects.all()
        serializer_class = serializers.questionSerializer(queryset, many=True)
        return Response(serializer_class.data)

    def post(self, request):
        # permission_classes = (IsAuthenticated,)
        serializer_class = serializers.questionSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status.HTTP_400_BAD_REQUEST)


class questiondetailAPIView(APIView):
    def get(self, request, question_number):
        # permission_classes = (IsAuthenticated,)
        queryset = models.question.objects.get(question_number=question_number)
        serializer_class = serializers.questionSerializer(queryset)
        return Response(serializer_class.data)

    def put(self, request, question_number):
        # permission_classes = (IsAuthenticated,)
        queryset = models.question.objects.get(
            question_number=question_number)
        serializer_class = serializers.questionSerializer(queryset, data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, question_number):
        queryset = models.question.objects.get(question_number=question_number)
        queryset.delete()
        models.question.objects.filter(question_number__gt=question_number).update(
            question_number=F('question_number') - 1)
        models.question.objects.aggregate(max_question_number=Max('question_number'))
        return Response(status=status.HTTP_204_NO_CONTENT)


class answerAPIView(APIView):
    def get(self, request):
        # permission_classes = (IsAuthenticated,)
        queryset = models.answer.objects.all()
        # values('Answer_number', 'content','Question_number')  공부해야할거
        serializer_class = serializers.answerSerializer(queryset, many=True)
        return Response(serializer_class.data)

    def post(self, request):
        # permission_classes = (IsAuthenticated,)
        serializer_class = serializers.answerSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status.HTTP_400_BAD_REQUEST)


class answerdetailAPIView(APIView):
    def get(self, request, answer_number):
        # permission_classes = (IsAuthenticated,)
        queryset = models.answer.objects.get(
            answer_number=answer_number)
        serializer_class = serializers.answerSerializer(queryset)
        return Response(serializer_class.data)

    def put(self, request, answer_number):
        # permission_classes = (IsAuthenticated,)
        queryset = models.answer.objects.get(
            answer_number=answer_number)
        serializer_class = serializers.answerSerializer(queryset, data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, answer_number):
        queryset = models.answer.objects.get(answer_number=answer_number)
        queryset.delete()
        models.answer.objects.filter(answer_number__gt=answer_number).update(
            answer_number=F('answer_number') - 1)
        models.answer.objects.aggregate(answer_number_number=Max('answer_number'))
        return Response(status=status.HTTP_204_NO_CONTENT)

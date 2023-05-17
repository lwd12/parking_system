from datetime import date
from django.db import  models
from django.utils import timezone
initial = True
from datetime import datetime


class residents_information(models.Model):  # 입주자정보
    TYPEOFCAR_CHOICES = [
        ('휘발유', '휘발유'),
        ('경유', '경유'),
        ('전기', '전기'),
    ]
    residents_number = models.BigAutoField(primary_key=True, serialize=False, verbose_name='resident_number')
    resident_name = models.CharField(max_length=10, verbose_name='입주자이름')
    resident_dong = models.IntegerField(verbose_name='입주자사는동')
    resident_ho = models.IntegerField(verbose_name='입주자사는호수')
    residents_doorpasswd = models.IntegerField(verbose_name='입주자현관문비밀번호')
    resident_homephonenumber = models.CharField(max_length=20, blank=True, null=True, verbose_name='집전화번호')
    resident_phone = models.CharField(max_length=20, unique=True,verbose_name='개인휴대전화번호')
    resident_carnumber = models.CharField(max_length=10, blank=True, null=True, verbose_name='차동자번호', unique=True)
    resident_typeofcar = models.CharField(max_length=5, choices= TYPEOFCAR_CHOICES, verbose_name='자동차의타입')
    resident_residency = models.BooleanField(default=True, verbose_name='거주여부')
    resident_movedate = models.DateField(max_length=100, blank=True, null=True, verbose_name='이사날짜')
    login_PassWd = models.CharField(max_length=20, verbose_name='PASSWD', null=True, blank=True)
    objects = models.Manager()

    class Meta:
        db_table = 'residents_information'
        ordering = ['residents_number']  #내림차순

    def save(self, *args, **kwargs):    #False 이사 날짜 추가 하는코드
        if not self.resident_residency and not self.resident_movedate:
            self.resident_movedate = date.today()
        else:
            self.resident_movedate = None
        super().save(*args, **kwargs)

    def delete_old_residents_information(self):
        six_months_ago = timezone.now() - timezone.timedelta(days=180)
        deleted_count = residents_information.objects.filter(residents_information_datetime__lt=six_months_ago,).delete()[0]
        residents_information.objects.filter(residents_number__gt=deleted_count).update(residents_number=models.F('residents_number') - deleted_count)
        return deleted_count

class insidetheparkinglot(models.Model):  # 주차장내부 한솔 원종
    GENERAL_SEAT_CHOICES = [
        ('A-1', 'A-1'),
        ('B-1', 'B-1'),
        ('C-1', 'C-1'),
    ]
    parking_seatnumber = models.BigAutoField(primary_key=True, serialize=False,
                                             verbose_name='parking_seatnumber')
    parking_generalseat = models.CharField(max_length=6, choices=GENERAL_SEAT_CHOICES, verbose_name='일반주차자리',
                                           unique=True, primary_key=False)
    parking_evchargedseattstate = models.BooleanField(verbose_name='전기충전자리상태')
    parking_seatstate = models.BooleanField(verbose_name='주차자리상태')
    parking_seatcarnumber = models.CharField(max_length=11, blank=True, null=True, verbose_name='주차된차량번호')
    objects = models.Manager()

    class Meta:
        db_table = 'insidetheparkinglot'
        ordering = ['parking_seatnumber']  # 내림차순

    def save(self, *args, **kwargs):
        if self.parking_generalseat == 'A-1':
            self.parking_evchargedseattstate = True
        super().save(*args, **kwargs)


# class parkinglot(models.Model):  # 주차장상태APP-클라이언트연동 환희 한솔
#     GENERAL_SEAT_CHOICES = [
#         ('A-1', 'A-1'),
#         ('B-1', 'B-1'),
#         ('C-1', 'C-1'),
#     ]
#     residents_choice_seatnumber = models.BigAutoField( primary_key=True, serialize=False,
#                                                       verbose_name=' residents_choice_seatnumber')
#     resident_dong = models.IntegerField(verbose_name='입주자사는동')
#     resident_ho = models.IntegerField(verbose_name='입주자사는호수')
#     parking_generalseat = models.CharField(max_length=6, choices=GENERAL_SEAT_CHOICES, verbose_name='일반주차자리')
#
#     objects = models.Manager()
#
#     class Meta:
#         db_table = 'parkinglot'
#         ordering = ['residents_choice_seatnumber']  # 내림차순
#
#     def save(self, *args, **kwargs):
#         if self.parking_generalseat == 'A-1':
#             self.parking_evchargedseattstate = True
#         super().save(*args, **kwargs)

class entrancetotheparkinglot(models.Model):  # 방문자입주자주차장입구 동선
    GENERAL_SEAT_CHOICES = [
        ('입차', '입차'),
        ('출차', '출차'),
    ]

    parking_log_number = models.BigAutoField(primary_key=True, serialize=False,verbose_name='parking_innumber')
    carnumber = models.CharField(max_length=11, verbose_name='차량번호')
    typeofentrysandexit = models.CharField(max_length=3, choices=GENERAL_SEAT_CHOICES, verbose_name='입출차여부')
    resident_dong = models.IntegerField(verbose_name='입주자사는동')
    resident_ho = models.IntegerField(verbose_name='입주자사는호수')
    entrydatetime = models.DateTimeField(verbose_name='입차날짜시간', unique=True, primary_key=False, null=True)
    exitdatetime = models.DateTimeField(verbose_name='출차날짜시간', unique=True, primary_key=False, null=True)
    person_check = models.CharField(max_length=30,verbose_name='차주상태')
    objects = models.Manager()
    class Meta:
        db_table = 'entrancetotheparkinglot'
        ordering = ['parking_log_number']  # 내림차순




class unauthorized_parking(models.Model):  # 비인가입차동선
    GENERAL_SEAT_CHOICES = [
        ('입차', '입차'),
        ('출차', '출차'),
    ]
    parking_log_number = models.BigAutoField(primary_key=True, serialize=False,verbose_name='parking_innumber')
    unauthorized_carnumber = models.TextField(verbose_name='차량번호 사진')
    unauthorized_carnumbers = models.TextField(verbose_name='비인가차량텍스트')
    typeofentrysandexit = models.CharField(max_length=3, choices=GENERAL_SEAT_CHOICES, verbose_name='입출차여부')
    resident_dong = models.IntegerField(verbose_name='입주자사는동')
    resident_ho = models.IntegerField(verbose_name='입주자사는호수')
    residents_doorpasswd = models.IntegerField(verbose_name='입주자현관문비밀번호')
    entrydatetime = models.DateTimeField(verbose_name='입차날짜시간', null=True, unique=True, primary_key=False)
    exitdatetime = models.DateTimeField(verbose_name='출차날짜시간', null=True, unique=True, primary_key=False)
    objects = models.Manager()

    class Meta:
        db_table = 'unauthorized_parking'
        ordering = ['parking_log_number']  # 내림차순


class visitor_information(models.Model):  # 방문자정보 환희
    visitor_information_number = models.BigAutoField(primary_key=True, serialize=False,
                                                     verbose_name='visitor_information_number ')
    resident_dong = models.IntegerField(verbose_name='신청인 동')
    resident_ho = models.IntegerField(verbose_name='신청인 호수')
    visitor_information_datetime = models.DateField(max_length=30, verbose_name='방문자신청일')
    visitor_information_date = models.DateField(max_length=30, verbose_name='방문자방문일')
    visitor_information_carnumber = models.CharField(max_length=11, verbose_name='방문자차량번호')
    objects = models.Manager()

    class Meta:
        db_table = 'visitor_information'
        ordering = ['visitor_information_number']  # 내림차순


    def save(self, *args, **kwargs): #방문일 신청하면 신청일 자동으로 그날짜 입력됨
        if self.visitor_information_date and not self.visitor_information_datetime:
            self.visitor_information_datetime = datetime.now().date()
        super().save(*args, **kwargs)


    def handle(self, *args, **options):  #datetime기준 2일 삭제되는코드
         two_days_ago = timezone.now() - timezone.timedelta(days=2)
         deleted_count, _ = visitor_information.objects.filter(visitor_information_datetime__lt=two_days_ago,).delete()
         visitor_information.objects.filter(visitor_information_number__gt=deleted_count).update(visitor_information_number=models.F('visitor_information_number') - deleted_count)



class safetyaccident(models.Model):  # 안전사고 환희 한솔
    safetyaccident_number = models.BigAutoField(primary_key=True, serialize=False,
                                                verbose_name='safetyaccident_number')
    safetyaccident_datetime = models.DateTimeField(verbose_name='안전사고발생날짜', default=timezone.now())
    safetyaccident_kind = models.CharField(max_length=100, verbose_name='안전사고종류및기타내용')
    objects = models.Manager()
    class Meta:
        db_table = 'safetyaccident'
        ordering = ['safetyaccident_number']  # 내림차순




class loginforAdministrator(models.Model):  # 로그인기록 원종
    loginforAdministrator_number = models.BigAutoField(primary_key=True, serialize=False,
                                                       verbose_name='loginforAdministrator_number')
    login_ID = models.CharField(max_length=20, verbose_name='ID')
    login_PassWd = models.CharField(max_length=255, verbose_name='PASSWD')
    email = models.CharField(max_length=100, verbose_name='E-mail')
    session = models.CharField(max_length=255, verbose_name='session', null=True, blank=True)
    objects = models.Manager()

    class Meta:
        db_table = 'loginforAdministrator'
        ordering = ['loginforAdministrator_number']  # 내림차순





class question(models.Model):
    question_number = models.BigAutoField(primary_key=True, verbose_name='Question_number')
    subject = models.CharField(max_length=200, verbose_name='제목', unique=True)

    content = models.CharField(max_length=1000, verbose_name='내용')
    create_datetime = models.DateTimeField(max_length=100, verbose_name='작성한일시간')
    modify_datetime = models.DateTimeField(max_length=100, null=True, blank=True, verbose_name='수정일시간')
    creator = models.CharField(max_length=200, verbose_name='작성자')
    etc = models.CharField(max_length=200, verbose_name='기타')
    objects = models.Manager()

    class Meta:
        db_table = 'question'
        ordering = ['question_number']  # 내림차순


class answer(models.Model):
    answer_number = models.BigAutoField(auto_created=True, primary_key=True, serialize=False,
                                        verbose_name='answer_number')
    content = models.CharField(max_length=1000, verbose_name='내용')
    create_date = models.DateTimeField(verbose_name='작성일')
    modify_date = models.DateTimeField(null=True, blank=True, verbose_name='작성한시간')
    creator = models.CharField(max_length=200, verbose_name='작성자')
    question_number = models.ForeignKey("question", on_delete=models.CASCADE, db_column=" question_number",
                                        verbose_name='질문번호')
    objects = models.Manager()
    class Meta:
        db_table = 'answer'
        ordering = ['answer_number']  # 내림차순




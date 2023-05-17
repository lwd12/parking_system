from rest_framework import serializers
from . import models



class residents_informationSerializer(serializers.ModelSerializer):

    resident_name = serializers.CharField(required=False, label="입주자이름")
    resident_dong = serializers.IntegerField(required=False,label='입주자거주동')
    resident_ho = serializers.IntegerField(required=False, label='입주자거주호수')
    residents_doorpasswd = serializers.IntegerField(required=False,label='현관문비밀번호')
    resident_homephonenumber = serializers.CharField(required=False, label='집전화번호')
    resident_phone = serializers.CharField(required=False, label='휴대전화번호')
    resident_carnumber = serializers.CharField(required=False, label='차량번호')
    resident_typeofcar = serializers.CharField(required=False,label='차량종류')
    resident_residency = serializers.BooleanField(required=False,label='거주여부')
    #resident_movedate = serializers.DateField(required=False)
    login_PassWd = serializers.CharField(required=False,label='앱비밀번호')
    print(models.residents_information.residents_number)


    class Meta:
        model = models.residents_information
        fields = "__all__"


class insidetheparkinglotSerializer(serializers.ModelSerializer):


    parking_generalseat = serializers.CharField(required=False, label='일반주차자리')
    parking_evchargedseattstate = serializers.BooleanField(required=False, label='전기충전자리상태')
    parking_seatstate = serializers.BooleanField(required=False, label='주차자리상태')
    parking_seatcarnumber = serializers.CharField(required=False, label='주차된차량번호')


    class Meta:
        model = models.insidetheparkinglot
        fields = "__all__"



class entrancetotheparkinglotSerializer(serializers.ModelSerializer):

    carnumber = serializers.CharField(required=False, label='차량번호')
    typeofentrysandexit = serializers.CharField(required=False, label='입출차여부')
    #resident_dong = serializers.IntegerField(verbose_name='입주자사는동')
    #resident_ho = serializers.IntegerField(verbose_name='입주자사는호수')
    #entrydatetime = serializers.DateTimeField(required=False)
    #exitdatetime = serializers.DateTimeField(required=False)
    person_check = serializers.CharField(required=False, label='차주상태')


    class Meta:
        model = models.entrancetotheparkinglot
        fields = "__all__"


class unauthorized_parkingSerializer(serializers.ModelSerializer):

    #unauthorized_carnumber = serializers.CharField(required=False)
    #unauthorized_carnumbers = serializers.CharField(required=False)
    typeofentrysandexit = serializers.CharField(required=False, label='입출차여부')
    resident_dong = serializers.IntegerField(required=False, label='입주자거주동')
    resident_ho = serializers.IntegerField(required=False, label='입주자거주호수')
    residents_doorpasswd = serializers.IntegerField(required=False, label='입주자현관문비밀번호')
    # entrydatetime = serializers.DateTimeField(required=False)
    # exitdatetime = serializers.DateTimeField(required=False)

    class Meta:
        model = models.unauthorized_parking
        fields = "__all__"


class visitor_informationSerializer(serializers.ModelSerializer):

    resident_dong = serializers.IntegerField(required=False, label='입주자거주동')
    resident_ho = serializers.IntegerField(required=False, label='입주자거주호수')
    # visitor_information_datetime = serializers.DateTimeField(required=False)
    visitor_information_carnumber = serializers.CharField(required=False, label='방문자차번호')


    class Meta:
        model = models.visitor_information
        fields = ("__all__")



class safetyaccidentSerializer(serializers.ModelSerializer):
    # safetyaccident_date = serializers.DateField(required=False)
    # safetyaccident_time = serializers.TimeField(required=False)
    # safetyaccident_kind = serializers.CharField(required=False)

    class Meta:
        model = models.safetyaccident
        fields = "__all__"


class loginforAdministratorSerializer(serializers.ModelSerializer):
    login_ID = serializers.CharField(required=False, label='관리자ID')
    login_PassWd = serializers.CharField(required=False, label='관리자PASSWD')
    email = serializers.CharField(required=False, label='E-mail')
    session = serializers.CharField(required=False, label='session')

    class Meta:
        model = models.loginforAdministrator
        fields = "__all__"



class questionSerializer(serializers.ModelSerializer):
    # resident_dong = serializers.IntegerField(required=False)
    # resident_ho = serializers.IntegerField(required=False)
    subject = serializers.CharField(required=False, label='제목')
    content = serializers.CharField(required=False, label='내용')
    #create_datetime = serializers.DateTimeField(required=False)
    #modify_datetime = serializers.DateTimeField(required=False)
    creator = serializers.CharField(required=False, label='작성자')
    etc = serializers.CharField(required=False, label='기타')

    # loginforAdministrator_number = serializers.PrimaryKeyRelatedField(required=False,queryset=models.loginforAdministrator.objects.all())
    class Meta:
        model = models.question
        fields = "__all__"
        # fields = ('Question_number', 'subject', 'content', 'create_date', 'modify_date', 'top_fixed')


class answerSerializer(serializers.ModelSerializer):
    # question = serializers.CharField(source='Question_number.question_text')  #
    content = serializers.CharField(required=False, label='내용')
    create_date = serializers.DateTimeField(required=False)
    modify_date = serializers.DateTimeField(required=False)
    creator = serializers.CharField(required=False, label='작성자')
    question_number = serializers.PrimaryKeyRelatedField(
        required=False, queryset=models.question.objects.all(), label='질문번호'
    )

    class Meta:
        model = models.answer
        fields = "__all__"
        # fields = ('Answer_number', 'content', 'create_date', 'modify_date','question')
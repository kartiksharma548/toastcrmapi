from dataclasses import field
from collections import OrderedDict
from datetime import datetime

from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from base.models import AllowedStatus, Lead, Note, Schedule, Status, Sub_Status, User
from sorl.thumbnail import ImageField, get_thumbnail
from PIL import Image
from django_resized import ResizedImageField

class UserSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField()
    id = serializers.ReadOnlyField()
    picture = ResizedImageField()

    class Meta:
        model = User
        fields = ('id',   'email', 'first_name', 'last_name', 'picture')
        optional_fields = ['picture', ]


    def create(self, validated_Data):
        user = User.objects.create_user(
            username=validated_Data['username'], email=validated_Data['email'], password=validated_Data['password'])
        user.first_name = validated_Data['first_name']
        user.last_name = validated_Data['last_name']
        user.save()
        return user

    def update(self, instance, validated_data):

        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)
        instance.picture = validated_data.get('picture', instance.picture)

        instance.save()

        
        return instance


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        user = User.objects.get(id=self.user.id)
        serializer = UserSerializer(user)
        print(serializer.data)

        data['user'] = serializer.data

        return data


class StatusSerializer(serializers.ModelSerializer):

    status_id = serializers.IntegerField(read_only=False)

    class Meta:
        model = Status
        fields = '__all__'


class SubStatusSerializer(serializers.ModelSerializer):

    sub_status_id = serializers.IntegerField(read_only=False)
    status = StatusSerializer()

    class Meta:
        model = Sub_Status
        fields = '__all__'


class AllowedStatusesSerializer(serializers.ModelSerializer):

    #sub_status_id = serializers.IntegerField(read_only=False)
    allowed_statuses = SubStatusSerializer(many=True)

    class Meta:
        model = AllowedStatus
        fields = ['allowed_statuses']


class LeadChartSerializer(serializers.ModelSerializer):
    value = serializers.IntegerField()
    text = serializers.CharField()
    color = serializers.CharField()

    class Meta:
        model = Lead
        fields = ('text', 'value', 'color')


class LeadClientConversionSerializer(serializers.ModelSerializer):

    Count = serializers.IntegerField()
    Month = serializers.CharField()

    class Meta:
        model = Lead
        fields = ('Count', 'Month')


class LeadSerializer(serializers.ModelSerializer):

    substatus = SubStatusSerializer()
    dob = serializers.DateField(format="%Y-%m-%d")
    full_name = serializers.CharField()
    new_status_id = serializers.CharField(
        write_only=True, required=False, allow_null=True)

    class Meta:
        model = Lead
        fields = '__all__'

    def validate(self, attrs):

        return super().validate(attrs)

    def update(self, instance, validated_data):

        #status = dict(OrderedDict(validated_data.pop('status')))

        if (validated_data.get('new_status_id') is not None):
            substatusObj = Sub_Status.objects.get(
                sub_status_id=validated_data.get('new_status_id'))

        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)
        instance.city = validated_data.get('city', instance.city)
        instance.state = validated_data.get('state', instance.state)
        instance.zip = validated_data.get('zip', instance.zip)
        instance.phone_number = validated_data.get(
            'phone_number', instance.phone_number)
        instance.address1 = validated_data.get('address1', instance.address1)
        instance.address2 = validated_data.get('address2', instance.address2)
        instance.dob = validated_data.get('dob', instance.dob)

        print(instance.substatus.sub_status_id)
        print(validated_data.get("new_status_id"))

        if (validated_data.get('new_status_id') is not None):
            if (instance.substatus.sub_status_id != validated_data.get('new_status_id')):
                instance.status_changedOn = datetime.now()
            instance.substatus = substatusObj

        instance.save()

        return instance

        # print(status)
        # print(newLeadData)


class NoteSerializer(serializers.ModelSerializer):
    lead = LeadSerializer(read_only=True)
    lead_id = serializers.IntegerField()

    #dateTime=serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = Note
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
        note = Note()
        note.note = validated_data.get('note')
        note.subject = validated_data.get('subject')

        lead = Lead.objects.get(lead_id=validated_data.get('lead_id'))
        note.lead = lead
        print(note)
        note.save()
        return note

    def update(self, instance, validated_data):
        instance.subject = validated_data.get('subject')
        instance.note = validated_data.get('note')

        instance.save()
        return instance

    def validate(self, attrs):
        print(attrs)
        return super().validate(attrs)


class ScheduleSerializer(serializers.ModelSerializer):
    schedule_dateTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    lead = LeadSerializer(read_only=True)
    lead_id = serializers.IntegerField()

    #dateTime=serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = Schedule
        fields = '__all__'

    def create(self, validated_data):

        sch = Schedule()
        sch.message = validated_data.get('message')
        sch.subject = validated_data.get('subject')
        sch.location = validated_data.get('location')
        sch.durationHr = validated_data.get('durationHr')
        sch.durationMin = validated_data.get('durationMin')
        sch.alarm = validated_data.get('alarm')
        sch.isCompleted = validated_data.get('isCompleted')
        sch.isCancelled = validated_data.get('isCancelled')
        sch.schedule_dateTime = validated_data.get('schedule_dateTime')

        lead = Lead.objects.get(lead_id=validated_data.get('lead_id'))
        sch.lead = lead

        sch.save()
        return sch

    def update(self, instance, validated_data):
        instance.message = validated_data.get('message')
        instance.subject = validated_data.get('subject')
        instance.location = validated_data.get('location')
        instance.durationHr = validated_data.get('durationHr')
        instance.durationMin = validated_data.get('durationMin')
        instance.alarm = validated_data.get('alarm')
        instance.isCompleted = validated_data.get('isCompleted')
        instance.isCancelled = validated_data.get('isCancelled')
        instance.schedule_dateTime = validated_data.get('schedule_dateTime')
        lead = Lead.objects.get(lead_id=validated_data.get('lead_id'))
        print(lead.substatus.sub_status_id)
        instance.schedule_updatedateTime = datetime.now()

        instance.save()
        return instance

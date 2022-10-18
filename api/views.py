from ast import And
from functools import partial
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import ListCreateAPIView
from base.models import AllowedStatus, Lead, Note, Schedule, Status, Sub_Status, User
from base.serializers import AllowedStatusesSerializer, LeadChartSerializer, LeadClientConversionSerializer, LeadSerializer, MyTokenObtainPairSerializer, NoteSerializer, ScheduleSerializer, StatusSerializer, SubStatusSerializer, UserSerializer
from django.db.models import Q, Count, F
from django.db import connection
from rest_framework.views import APIView
from rest_framework import serializers


@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

    return Response("Successful")


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def getLead(request, userid):

    status = request.data['status']
    lead_id = str(request.data['lead_id'])
    userid = str(userid)
    query = request.data['query']
    query = "%"+query+"%"

    cursor = connection.cursor()

    # cursor.execute()
    # row = cursor.fetchall()
    # print("SELECT * FROM base_lead where user_id=4 and ('"+status+"'='' or status_id='" +
    #       status+"' ) and ('"+query+"'='' or first_name like %s)", [query])
    leads = Lead.objects.raw("SELECT * FROM base_lead LE JOIN base_sub_status SS on SS.sub_status_id=LE.substatus_id Join base_status S on S.status_id = SS.status_id where user_id='"+userid+"'  and ('" +
                             status+"'='' or S.status_id='"+status+"' ) and ('" +
                             lead_id+"'='' or LE.lead_id='"+lead_id+"' ) and CONCAT(first_name ,' ', last_name) like %s", [query])

    serializer = LeadSerializer(leads, many=True)
    print(serializer.data)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def getStatuses(request):

    statuses = Status.objects.all()

    serializer = StatusSerializer(statuses, many=True)

    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def getSubStatuses(request, substatus_id):

    if request.data:
        cancellationStatuses = request.data['cancellationStatuses']

    else:
        cancellationStatuses = "0"

    sub_statuses = Sub_Status.objects.raw("SELECT BA_SUB2.* FROM base_allowedstatus_allowed_statuses BA_ALL_STATUS JOIN base_allowedstatus BA_ALL on BA_ALL.id=BA_ALL_STATUS.allowedstatus_id join base_sub_status BA_SUB on BA_ALL.current_status_id=BA_SUB.sub_status_id join base_sub_status BA_SUB2 on BA_ALL_STATUS.sub_status_id=BA_SUB2.sub_status_id where BA_SUB.sub_status_id='"+str(
        substatus_id)+"' and BA_SUB2.statusForCancellation='"+cancellationStatuses+"'")

    # sub_statuses=AllowedStatus.objects.filter(current_status__sub_status_id=substatus_id,allowed_statuses__statusForCancellation=False)
    # newSubStatuses=sub_statuses.filter(current_status__statusForCancellation=False)

    #sub_statuses = Sub_Status.objects.filter(~Q(sub_status_id=substatus_id))
    serializer = SubStatusSerializer(sub_statuses, many=True)

    #serializer = SubStatusSerializer(sub_statuses, many=True)

    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def getCancelledStatuses(request):

    substatuses = Sub_Status.objects.filter(
        status__status_id_name='STATUS_LOST')

    serializer = SubStatusSerializer(substatuses, many=True)

    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def updateLead(request, id):

    leadInstance = Lead.objects.get(lead_id=id)

    serializer = LeadSerializer(instance=leadInstance, data=request.data)

    if (serializer.is_valid()):
        serializer.save()
        return Response(serializer.data)

    return Response({'msg': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# class NoteListCreate(ListCreateAPIView):
#     authentication_classes=[JWTAuthentication]
#     permission_classes=[IsAuthenticated]
#     queryset=Note.objects.all()
#     serializer_class=NoteSerializer

#     def create(self, request, *args, **kwargs):
#         print('Here')
#         response = super().create(request, *args, **kwargs)
#         print(response)
#         note=Note()
#         note.note=response.data.get('note')
#         note.subject=response.data.get('subject')
#         note.lead=response.data.get('lead')

#         note.save()

#         return response


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def postNote(request):

    serializer = NoteSerializer(data=request.data)

    if (serializer.is_valid(raise_exception=True)):
        print('Is Valid')
        serializer.save()

    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def getNotes(request, lead_id):

    notes = Note.objects.filter(lead=lead_id).order_by('-dateTime')
    serializer = NoteSerializer(notes, many=True)

    return Response(serializer.data)


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def deleteNote(request, id):

    note = Note.objects.get(note_id=id)
    note.delete()

    return Response("OK")


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def updateNote(request, id):

    # print(id)
    noteInstance = Note.objects.get(note_id=id)

    serializer = NoteSerializer(instance=noteInstance, data=request.data)

    if (serializer.is_valid(raise_exception=True)):
        print('Is Valid')
        serializer.save()

    return Response(serializer.data)


# class ScheduleViewSet(viewsets.ModelViewSet):
#     authentication_classes = [JWTAuthentication]
#     permission_classes=[IsAuthenticated]
#     queryset=Schedule.objects.all()
#     serializer_class=ScheduleSerializer

#     def create(self, request, *args, **kwargs):
#         serialized = self.serializer_class(data=request.DATA)


#         if serialized.is_valid():
#             serialized.save()
#             return Response(status=status.HTTP_202_ACCEPTED)
#         else:
#             return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class ScheduleAPI(APIView):
    def get(self, request, id=None, format=None):

        if id is not None:
            sch = Schedule.objects.filter(
                lead=id).order_by('-schedule_dateTime')
            serializer = ScheduleSerializer(sch, many=True)
            return Response(serializer.data)

        sch = Schedule.objects.all()
        serializer = ScheduleSerializer(sch, many=True)
        return Response(serializer.data)

    def put(self, request, id):

        schObj = Schedule.objects.get(schedule_id=id)
        serializer = ScheduleSerializer(instance=schObj, data=request.data)
        if (serializer.is_valid()):
            serializer.save()
            return Response({'msg': 'Data Updated'}, status=status.HTTP_201_CREATED)

        return Response({'msg': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):

        serializer = ScheduleSerializer(data=request.data)
        if (serializer.is_valid()):
            serializer.save()
            return Response({'msg': 'Data Created'}, status=status.HTTP_201_CREATED)

        return Response({'msg': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):

        sch = Schedule.objects.get(schedule_id=id)
        sch.delete()

        return Response("OK")


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def changeStatus(request):

    leadid = request.data['lead_id']
    leadInstance = Lead.objects.get(lead_id=leadid)

    serializer = LeadSerializer(
        instance=leadInstance, data=request.data, partial=True)

    if (serializer.is_valid()):
        serializer.save()
        return Response(serializer.data)
    return Response({'msg': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def getLeadChartData(request, userid):

    leads = (Lead.objects.filter(user_id=userid).values('substatus__sub_status_name').annotate(value=Count(
        'substatus'), text=F('substatus__sub_status_name'), color=F('substatus__status__status_backcolor')))

    serializer = LeadChartSerializer(leads, many=True)

    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def getClientConversionData(request, userid):

    clientConversion = Lead.objects.raw(
        "SELECT lead_id,Count(*) as Count,Month(cast(status_changedOn as Date)) as Month FROM base_lead BE JOIN base_sub_status BS on Be.substatus_id=Bs.sub_status_id  where BS.sub_status_name='Client' and BE.user_id='"+str(userid)+"' group by Month order by Month")
    print(clientConversion)
    serializer = LeadClientConversionSerializer(clientConversion, many=True)

    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def updateUserProfile(request, userid):

    print(request.data)
    user = User.objects.get(id=userid)
    serializer = UserSerializer(user, data=request.data)

    if (serializer.is_valid()):
        serializer.save()
        return Response(serializer.data)
    return Response({'msg': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

   


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

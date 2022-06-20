from datetime import datetime
import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
import graphql_jwt
from .mutations import ClockInMutation, ClockOutMutation, UserMutation,UserType,ClockType,ClockedHoursType
from .models import ClockItem, ClockedHours
from graphql_jwt.decorators import login_required
import arrow

class Query(graphene.ObjectType):
    me = graphene.Field(UserType, token=graphene.String(required=True))
    current_clock=graphene.Field(ClockType,token=graphene.String(required=True))
    clocked_hours=graphene.Field(ClockedHoursType,token=graphene.String(required=True))
    
    @login_required
    def resolve_me(self, info, **kwargs):
        return info.context.user

    @login_required
    def resolve_current_clock(self, info, **kwargs):
        user=info.context.user
        user=User.objects.get(username=user)
        clocks=ClockItem.objects.filter(user=user,clockOut=None)
        for clock in clocks:
            if clock.clockOut==None:
                return clock

    @login_required
    def resolve_clocked_hours(self, info, **kwargs):
        start_of_month=(arrow.utcnow().span('month')[0])
        start_of_week=(arrow.utcnow().span('week')[0])
        start_of_day=(arrow.utcnow().span('day')[0])

        clocks = ClockItem.objects.filter(clockIn__gte=str(start_of_day),clockIn__lte=str(datetime.now()))
        total_hours_worked_in_a_day=0
        for clock in clocks:
            hours_worked_in_shift=((clock.clockOut-clock.clockIn).total_seconds())/3600
            total_hours_worked_in_a_day=total_hours_worked_in_a_day+hours_worked_in_shift

        clocks = ClockItem.objects.filter(clockIn__gte=str(start_of_week),clockIn__lte=str(datetime.now()))
        total_hours_worked_in_a_week=0
        for clock in clocks:
            hours_worked_in_shift=((clock.clockOut-clock.clockIn).total_seconds())/3600
            total_hours_worked_in_a_week=total_hours_worked_in_a_week+hours_worked_in_shift

        clocks = ClockItem.objects.filter(clockIn__gte=str(start_of_month),clockIn__lte=str(datetime.now()))
        total_hours_worked_in_a_month=0
        for clock in clocks:
            hours_worked_in_shift=((clock.clockOut-clock.clockIn).total_seconds())/3600
            total_hours_worked_in_a_month=total_hours_worked_in_a_month+hours_worked_in_shift
        return ClockedHours(today=total_hours_worked_in_a_day,currentWeek=total_hours_worked_in_a_week,currentMonth=total_hours_worked_in_a_month)

class Mutation(graphene.ObjectType):
    add_user = UserMutation.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    clock_in = ClockInMutation.Field()
    clock_out = ClockOutMutation.Field()

schema = graphene.Schema(query=Query,mutation=Mutation)
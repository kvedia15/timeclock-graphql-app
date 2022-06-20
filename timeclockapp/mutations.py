from datetime import datetime
import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from .models import ClockItem, ClockedHours
from graphql_jwt.decorators import login_required



class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "email", "username")

class ClockType(DjangoObjectType):
    class Meta:
        model = ClockItem
        fields = ("user", "clockIn", "clockOut")
    
class ClockedHoursType(DjangoObjectType):
    class Meta:
        model=ClockedHours
        fields = ("today","currentWeek","currentMonth")


class UserMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        email = graphene.String(required=True)
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    # The class attributes define the response of the mutation
    user = graphene.Field(UserType)
    @classmethod
    def mutate(cls, root, info, email,username,password):
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return UserMutation(user=user)
 
class ClockInMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        token=graphene.String(required=True)
    clock_item = graphene.Field(ClockType)
    
    
    @classmethod
    @login_required
    def mutate(cls, root, info, token):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("Authentication credentials were not provided")
        else:
            user=User.objects.get(username=user)
            clocks=ClockItem.objects.filter(user=user)

            if len(clocks)==0 :
                new_clock=ClockItem()
                new_clock.user=User.objects.get(username=user)
                new_clock.clockIn=datetime.now()
                new_clock.save()
                return ClockInMutation(clock_item=new_clock)
            else:
                for clock in clocks:
                    not_clocked_out_yet=True if clock.clockOut == None else False
                if not_clocked_out_yet:
                    raise Exception("You have already clocked in, please clock out to clock in again.")
                else:
                    new_clock=ClockItem()
                    new_clock.user=User.objects.get(username=user)
                    new_clock.clockIn=datetime.now()
                    new_clock.save()
                    return ClockInMutation(clock_item=new_clock)
         
class ClockOutMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        token=graphene.String(required=True)
    clock_item = graphene.Field(ClockType)
    
    
    @classmethod
    @login_required
    def mutate(cls, root, info, token):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("Authentication credentials were not provided")
        else:
            user=User.objects.get(username=user)
            clocks=ClockItem.objects.filter(user=user,clockOut=None)

            if len(clocks)==0 :
                raise Exception("You have not clocked in yet. Please clock in first!")
                
            else:
                for clock in clocks:
                    not_clocked_out_yet=True if clock.clockOut == None else False
                    if not_clocked_out_yet:
                        clock.clockOut=datetime.now()
                        clock.save()
                        return ClockOutMutation(clock_item=clock)
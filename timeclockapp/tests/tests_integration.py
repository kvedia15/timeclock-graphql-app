from datetime import datetime, timedelta
import json
import time

import pandas as pd
from sympy import sec
import graphene
from graphene_django.utils.testing import GraphQLTestCase
from ..models import ClockItem
from ..schema import Mutation, Query
from django.contrib.auth import get_user_model
from graphql_jwt.testcases import JSONWebTokenTestCase



class ClockTests(JSONWebTokenTestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(username="test")
        self.client.authenticate(self.user)
        

    def test_clock_in_and_clock_out_mutation(self):
        query ='''
                mutation {
                clockIn(token:"test-token"){
                    clockItem{
                    user{
                        username
                    }
                    clockIn
                    clockOut
                    }
                }
                }
            '''
        response=self.client.execute(query)
        print(dict(response.data))
        time.sleep(1)
        query ='''
                mutation {
                clockOut(token:"test-token"){
                    clockItem{
                    user{
                        email
                        username
                    }
                    clockIn
                    clockOut
                    }
                }
                }
            '''
        response=self.client.execute(query)
        response_dict=(dict(response.data))
        clock_in_time=pd.to_datetime(response_dict["clockOut"]["clockItem"]["clockIn"][0:10]+" "+response_dict["clockOut"]["clockItem"]["clockIn"][11:19])
        clock_out_time=pd.to_datetime(response_dict["clockOut"]["clockItem"]["clockOut"][0:10]+" "+response_dict["clockOut"]["clockItem"]["clockOut"][11:19])
        secs_worked=int((clock_out_time-clock_in_time).total_seconds())
        assert secs_worked == 1


class CurrentClockTests(JSONWebTokenTestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(username="test")
        self.client.authenticate(self.user)
        

    def test_clock_in_and_clock_out_mutation(self):
        query ='''
                mutation {
                clockIn(token:"test-token"){
                    clockItem{
                    user{
                        username
                    }
                    clockIn
                    clockOut
                    }
                }
                }
            '''
        response=self.client.execute(query)
        query ='''
            query  {
            currentClock(token:"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Imtpc2hhbiIsImV4cCI6MTY1NTY1MTc0MSwib3JpZ0lhdCI6MTY1NTY1MTQ0MX0.UWsk2W2b3WLUfNk-nslK_QD5YnzvCrK8RdTaRg3JwT0") {
                user{
                    username
                }
                clockOut
            }
}
            '''
        response=self.client.execute(query)
        response_dict=(dict(response.data))
        username=response_dict["currentClock"]["user"]["username"]
        clock_out=response_dict["currentClock"]["clockOut"]
        assert username == 'test'
        assert clock_out == None
        

class ClockedHoursTests(JSONWebTokenTestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username="test")
        self.client.authenticate(self.user)
        new_clock=ClockItem()
        new_clock.user=self.user
        new_clock.clockIn=datetime.now()-timedelta(hours=2)
        new_clock.clockOut=datetime.now()-timedelta(hours=1)
        new_clock.save()
        new_clock=ClockItem()
        new_clock.user=self.user
        new_clock.clockIn=datetime.now()-timedelta(hours=1)
        new_clock.clockOut=datetime.now()-timedelta(minutes=10)
        new_clock.save()

    def test_hour_aggregation_query(self):
        query ='''
                query  {
                clockedHours(token:"test-token") {
                    today
                    currentWeek
                    currentMonth
                }
                }
            '''
        response=self.client.execute(query)
        response_dict=(dict(response.data))
        today_worked_hrs=(response_dict["clockedHours"]["today"])
        assert today_worked_hrs == 1
    
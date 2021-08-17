from django.db import models
from AI.models import AI

class User_data(models.Model):
    auto_increment_id = models.AutoField(primary_key = True)
    password=models.CharField(max_length=25)


class User(models.Model):
    username=models.CharField(max_length=25,primary_key=True)
    user_data=models.ForeignKey(User_data,on_delete=models.CASCADE, null= True)
    color1=models.CharField(max_length=25)
    color2=models.CharField(max_length=25)
    nb_games = models.IntegerField()
    nb_games_wins = models.IntegerField()
    ai_id = models.ForeignKey(AI,on_delete=models.CASCADE,blank=True,null=True)

    manager = models.Manager()
    



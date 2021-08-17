from django.db import models
from connection.models import User
from AI.models import State


# Create your models here.
class Game_State(models.Model):
    auto_increment_id=models.AutoField(primary_key=True)
    current_player=models.IntegerField()
    board=models.CharField(max_length=146)
    manager = models.Manager()

class Game_Player(models.Model):
    auto_increment_id=models.AutoField(primary_key=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    game_state=models.ForeignKey(Game_State,on_delete=models.CASCADE)
    pos=models.CharField(max_length=5)
    color = models.CharField(max_length=146)
    previous_state_ai=models.ForeignKey(State,on_delete=models.CASCADE,blank=True,null=True)
    num_player = models.IntegerField()
    old_direction = models.IntegerField(null=True)
    manager = models.Manager()
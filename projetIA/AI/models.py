from django.db import models

# Create your models here.
class AI(models.Model):
    id = models.AutoField(primary_key = True)
    epsilon = models.FloatField()
    speed_learning = models.IntegerField()
    learning_rate = models.FloatField()
    manager = models.Manager()
    nb_games_training = models.IntegerField()
    nb_games_training_wins = models.IntegerField()


class State(models.Model):
    id = models.AutoField(primary_key = True)
    board=models.CharField(max_length=146, db_index=True)
    position = models.CharField(max_length=2, db_index=True)
    position2 = models.CharField(max_length=2, db_index=True)
    q_table = models.CharField(max_length=100)
    ai_id=models.ForeignKey(AI,on_delete=models.CASCADE, db_index=True)
    manager = models.Manager()



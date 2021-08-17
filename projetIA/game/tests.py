from django.test import TestCase
from game.business import *
from game.models import Game_Player

# Create your tests here.

class IsCoordValideTest(TestCase):
    def test_is_coord_valide_true(self):
        for i in range(8):
            for j in range(8):
                self.assertTrue(is_coord_valide([i,j]))

    
    def test_is_coord_valide_false(self):
        self.assertFalse(is_coord_valide([9,5]))
        self.assertFalse(is_coord_valide([-1,5]))
        self.assertFalse(is_coord_valide([5,9]))
        self.assertFalse(is_coord_valide([5,-1]))
        self.assertFalse(is_coord_valide([9,9]))
        self.assertFalse(is_coord_valide([-1,-1]))

        
class ChangePlayerTest(TestCase):
    p1 = Game_Player(auto_increment_id=1)
    p2 = Game_Player(auto_increment_id=2)
    p3 = Game_Player(auto_increment_id=3)

    players = [p1,p2]
    players_v2 = [p1,p2,p3]
    
    def test_change_player_1_to_2(self):
        self.assertEqual(change_player(self.players, 0),2)
    
    def test_change_player_2_to_1(self):
        self.assertEqual(change_player(self.players, 1),1)

    def test_change_player_2_to_3(self):
        self.assertEqual(change_player(self.players_v2, 1),3)
    
    def test_change_player_3_to_1(self):
        self.assertEqual(change_player(self.players_v2, 2),1)

class EndOfGameTest(TestCase):

    def test_end_of_game_true(self):
        b = [[1,2,1,2,1],[2,2,2,1]]
        self.assertTrue(end_of_game(b))

    def test_end_of_game_false(self):
        b = [[1,2,1,2,1],[2,0,2,1]]
        self.assertFalse(end_of_game(b))

class DefineWinnerTest(TestCase): #Verifie aussi Count_elements -> Pas vraiment unitaire

    def test_define_winner_1(self):
        b=[[1,1,1,1],[1,1,2,2]]
        self.assertEqual(define_winner(b)[0], 1)

    def test_define_winner_2(self):
        b=[[1,1,2,2],[2,2,2,2]]
        self.assertEqual(define_winner(b)[0], 2)

    def test_define_winner_tie(self):
        b=[[1,1,1,1],[2,2,2,2]]
        self.assertEqual(define_winner(b)[2], True)

        
        

        
        
        

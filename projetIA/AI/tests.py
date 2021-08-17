from django.test import TestCase
from AI.views import *

# Create your tests here.
class countBoxesTest(TestCase):
    def testBoardCorrect1(self):
        board = [[1,1,1,1,0,0],[1,0,1,0]]
        self.assertEquals(count_boxes(board,1),6)
    
    def testBoardIf0(self):
        board = [[0,0,0,0],[2,0,4,0]]
        self.assertEquals(count_boxes(board,1),0)

    def testBoardCorrect2(self):
        board = [[2,2,0,0],[2,2,2,0]]
        self.assertEquals(count_boxes(board,2),5)

class qtableCountValueTest(TestCase):
    def testCount5(self):
        q_table = [0,1,2,2]
        self.assertEquals(qtable_count_value(q_table),5)
    def testCount0(self):
        q_table = [0,0,0,0]
        self.assertEquals(qtable_count_value(q_table),0)



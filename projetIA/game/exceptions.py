class OufOfBoardError(Exception):
    def __init__( self, expression, message):
        self.expression = expression
        self.message = message
        
class NotEmptyCellError(Exception):
    def __init__( self, expression, message):
        self.expression = expression
        self.message = message
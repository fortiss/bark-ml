class BaseQuantizedLabelFunction():
    def __init__(self, robustness: float = float('-inf')):
        self.robustness = robustness    

    def GetCurrentRobustness(self):
        return self.robustness
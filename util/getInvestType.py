class InvestSurvey():
    def __init__(self):
        super(InvestSurvey, self).__init__()
        self.type = ['Cautious', 'steady', 'active', 'aggressive']


    def getType(self,answers):

        score = answers[0] * 2 + answers[1]
        if score == 0:
            return self.type[0]
        if score == 1 or score == 2:
            return self.type[1]
        if score < 5:
            return self.type[2]
        return self.type[3]

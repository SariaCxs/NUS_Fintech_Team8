class InvestSurvey():
    def __init__(self):
        super(InvestSurvey, self).__init__()
        self.type = ['Cautious', 'steady', 'active', 'aggressive']


    def getType(self,answers):

        score = answers[0] * 2 + answers[1]
        type_ind = 0
        if score == 0:
            type_ind = 0
        elif score == 1 or score == 2:
            type_ind = 1
        elif score < 5:
            type_ind = 2
        else:
            type_ind = 3

        score = type_ind * 3 + answers[2]

        return self.type[type_ind],score

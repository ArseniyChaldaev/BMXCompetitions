from GlobalVars import SCORE
from models import Event


class Race:
    def __init__(self, competition_id, gender=None, category_id=None):
        self.competition_id = competition_id
        self.startList = None
        self.initStartList()

        self.gender = gender
        self.category_id = category_id
        self.currentData = None
        self.results = None

    def initStartList(self):
        self.startList = Event.getStartList(self.competition_id)
        if not self.startList:
            self.startList = Event.createStartList(self.competition_id)

    def setGenderAndCategory(self, gender, category_id):
        self.gender = gender
        self.category_id = category_id
        if (self.gender, self.category_id) in self.startList:
            self.currentData = self.startList[(self.gender, self.category_id)]
            self.results = Event.getResults(self.competition_id, self.gender, self.category_id)
        else:
            self.currentData = None
            self.results = None

    def save(self, positions):
        Event.updateStartList(positions)

    def generateRaces(self, last_race_type):
        if last_race_type == 3:
            self.generateAfterMotos()
        else:
            self.generateSomeFinal(last_race_type)

    def generateAfterMotos(self):
        race_count = len(self.currentData[3].keys())
        if race_count == 1:
            self.generateResults()
            return

        res = self.getMotosResults(race_count)
        self.generateNextRound(res)

    def getMotosResults(self, race_count):
        res = [dict() for _ in range(race_count)]
        for i in range(1, 4):
            for j in range(race_count):
                for item in self.currentData[i][j + 1]:
                    sportsman_id, position = item[0], item[3]
                    res[j][sportsman_id] = res[j].get(sportsman_id, 0) + int(position)
        self.sortResults(res)
        return res

    def generateSomeFinal(self, race_type):
        if race_type == 6:
            self.generateResults()
            return
        res = self.getSomeFinalResults(race_type)
        self.generateNextRound(res)

    def getSomeFinalResults(self, race_type):
        if race_type == 4:
            race_count = 4
        elif race_type == 5:
            race_count = 2
        else:
            race_count = 1
        res = [{item[0]: item[3] for item in self.currentData[race_type][i + 1]} for i in range(race_count)]
        self.sortResults(res)
        return res

    def generateNextRound(self, res):
        race_count = len(res) // 2
        next_race_number = 7 - race_count
        next_start_list = []  # gender, category_id, race_type, race_number, sportsman_id, start_position
        place = 1
        for i in range(4):
            for j in range(len(res)):
                next_start_list.append((self.competition_id, self.gender, self.category_id, next_race_number,
                                        (i + j) % race_count + 1, res[j][i][0], place))
                if race_count == 1 or j % race_count == 1:
                    place += 1

        self.startList = Event.createNextRoundStartList(self.competition_id, next_start_list)

    def generateResults(self):
        race_type = 6  # final
        result_list = []  # competition_id, gender, category_id, sportsman_id, position, score
        if race_type not in self.currentData.keys():
            res = self.getMotosResults(1)
            for i in range(len(res)):
                result_list.append((self.competition_id, self.gender, self.category_id,
                                    res[0][i][0], i + 1, SCORE[i + 1]))
            Event.saveResult(result_list)
            return

        res = self.getSomeFinalResults(6)
        for i in range(len(res[0])):
            result_list.append((self.competition_id, self.gender, self.category_id,
                                res[0][i][0], i + 1, SCORE[i]))
        place = 9
        if 5 in self.currentData.keys():
            res = self.getSomeFinalResults(5)
            for i in range(4, 8):
                for j in range(len(res)):
                    result_list.append((self.competition_id, self.gender, self.category_id,
                                        res[j][i][0], place, SCORE[place - 1]))
                    place += 1

        if 4 in self.currentData.keys():
            res = self.getSomeFinalResults(4)
            for i in range(4, 8):
                for j in range(len(res)):
                    result_list.append((self.competition_id, self.gender, self.category_id,
                                        res[j][i][0], place, SCORE[place - 1]))
                    place += 1
        race_count = len(self.currentData[3].keys())
        res = self.getMotosResults(race_count)
        for i in range(4, 8):
            for j in range(len(res)):
                if i < len(res[j]):
                    result_list.append((self.competition_id, self.gender, self.category_id,
                                        res[j][i][0], place, SCORE[place - 1]))
                    place += 1
        Event.saveResult(result_list)
        self.results = Event.getResults(self.competition_id, self.gender, self.category_id)

    def sortResults(self, res):
        for i in range(len(res)):
            res[i] = sorted(res[i].items(), key=lambda x: x[1])

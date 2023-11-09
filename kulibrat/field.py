from kulibrat.const import ROWS


class field:
    def __init__(self, row, col, point, pathway):
        self.point = point
        self.pathway = pathway
        self.row = row
        self.col = col
        self.score = point

    def getScore(self, pathwayPenalty, proximity):
        return self.score - pathwayPenalty - proximity
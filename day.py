'''
Dervaux Florence, N° de matricule : 000396246, groupe 1

Projet d'année: Simulation de la gestion du trafic aérien d’un aéroport
Partie 4

fichier: day.py
'''

class Day:
    def __init__(self, year, month, day):
        self.year = int(year) 
        self.month = int(month)
        self.day = int(day)

    def getDay(self):
        return self.day

    def getMonth(self):
        return self.month

    def getYear(self):
        return self.year

    def increment(self):
        # Information sur le jour 
        bissextile = False
        if self.year % 4 == 0:
            bissextile =  True

        longMonth = False
        february = False
        december = False
        longMonthList = [1, 3, 5, 7, 8, 10]

        if self.month in longMonthList:
            longMonth = True

        if self.month == 2:
            february = True

        if self.month == 12:
            december = True

        #construction de la nouvelle date:
        day = self.day
        month = self.month
        year = self.year

        if longMonth:
            if self.day == 31:
                day = 1
                month = self.month + 1

            else:
                day = self.day + 1

        elif february:
            if bissextile:
                if self.day == 29:
                    day = 1
                    month = self.month + 1
                
                else:
                    day = self.day + 1
            else:
                if self.day == 28:
                    day = 1
                    month = self.month + 1
                else:
                    day = self.day + 1

        elif december:
            if self.day == 31:
                day = 1
                month = 1
                year = self.year + 1
            else:
                day = self.day + 1

        else:
            if self.day == 30:
                day = 1
                month =  self.month + 1
            else:
                day = self.day + 1

        newDate = Day(year, month, day)
        return newDate
    
    def compare(self, anotherDay):
        '''
        Renvoie  1  si day supérieur à anotherDay
                 0  si day égale     à anotherDay
                 -1 si day inférieur à anotherDay
        '''
        yearDay = self.year
        monthDay = self.month
        dayDay = self.day

        yearAnother = anotherDay.getYear()
        monthAnother = anotherDay.getMonth()
        dayAnother = anotherDay.getDay()

        # day égale à anotherDay
        if yearDay == yearAnother and monthDay == monthAnother and dayDay == dayAnother:
            res = 0

        # day inférieur à anotherDay
        elif yearDay < yearAnother:
            res = -1

        elif monthDay < monthAnother and yearDay <= yearAnother:
            res = -1

        elif dayDay < dayAnother and monthDay <= monthAnother and yearDay <= yearAnother:
            res = -1

        # day supérieur à anotherDay
        elif yearDay > yearAnother:
            res = 1

        elif monthDay > monthAnother and yearDay >= yearAnother:
            res = 1

        elif dayDay > dayAnother and monthDay >= monthAnother and yearDay >= yearAnother:
            res = 1

        return res 

    def __str__(self):
        txt = ((str(self.day)).rjust(2, '0') + '/' +
                (str(self.month)).rjust(2, '0') + '/' +
                (str(self.year)))
        return txt

    @staticmethod
    def fromjson(json):
        year = json["year"]
        month = json["month"]
        day = json["day"]

        return Day(year, month, day)

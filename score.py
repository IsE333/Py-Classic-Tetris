import numpy
class Score:
    def __init__(self,level) -> None:
        self.stats = numpy.array([ [255*(a%2),255*(a%2),255*(a%2)] for a in range(14)])
        self.lineC = numpy.array([0,0,0,0])
        self.score = 0
        f = open("topScore.score", "r")
        self.maxScore = int(f.readline())
        f.close()
        self.maxScoreMap = numpy.array([0,0,0,0,0,0])
        self.maxSscoreUpdate()
        self.map = numpy.array([0,0,0,0,0,0])
        self.level = level
        self.startLevel=level
    def lineClear(self,number):
        if number !=0:
            coefficient=0
            if number==1: coefficient=40
            elif number==2: coefficient=100
            elif number==3: coefficient=300
            elif number==4: coefficient=1200
            self.score+= int(coefficient*(self.level+1))
            self.mapUpdate()
    def pressDown(self,frame):
        self.score+=int(frame*12/28)
        self.mapUpdate()
    def mapUpdate(self):
        self.map = numpy.array([self.score%1000000//100000,self.score%100000//10000,self.score%10000//1000,self.score%1000//100,self.score%100//10,self.score%10])
    def maxSscoreUpdate(self):
        self.maxScoreMap = numpy.array([self.maxScore%1000000//100000,self.maxScore%100000//10000,self.maxScore%10000//1000,self.maxScore%1000//100,self.maxScore%100//10,self.maxScore%10])
        f = open("topScore.score", "w")
        f.write(str(self.maxScore))
        f.close()
    def reset(self,level,type):
        if self.maxScore<self.score: 
            self.maxScore=self.score
            self.maxSscoreUpdate()
        if type==0:
            self.score = 0
            self.map = numpy.array([0,0,0,0,0,0])
            self.level = level
    def statUpdate(self,type):
        num=int(self.stats[type*2][0]*100+self.stats[type*2][1]*10+self.stats[type*2][2])
        num+=1
        self.stats[type*2][2] = int(num%10)
        self.stats[type*2][1] = int((num%100)//10)
        self.stats[type*2][0] = int(num//100)
    def lineCountUpdate(self,lineCount): #updates line count and cheks lines for level up
        levelCheck=False
        if lineCount !=0:
            num=self.lineC[0]*1000+self.lineC[1]*100+self.lineC[2]*10+self.lineC[3]#lineCount
            num+=lineCount
            self.lineC[0] = int(num//1000)
            self.lineC[1] = int((num%1000)//100)
            self.lineC[2] = int((num%100)//10)
            self.lineC[3] = int(num%10)
            oldLevel=self.level
            if num>=(self.startLevel * 10 + 10) or num>= max(100,self.startLevel*10-50) :
                self.level = self.startLevel + (num-max(100,self.startLevel*10-50))//10 + 1
                if self.level-oldLevel !=0: levelCheck=True
        return levelCheck,numpy.array([self.level//10,self.level%10])
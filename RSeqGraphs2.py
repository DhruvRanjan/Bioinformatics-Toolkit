from rpy2 import robjects
from rpy2.robjects import Formula, Environment
from rpy2.robjects.vectors import IntVector, FloatVector
from rpy2.robjects.lib import grid
from rpy2.robjects.packages import importr, data
from rpy2.rinterface import RRuntimeError
import warnings
import numpy as np
import pandas as pd
import rpy2.robjects.pandas2ri
import Scripts.MatrixParser as MatrixParser

grdevices = importr('grDevices')

# The R 'print' function
rprint = robjects.globalenv.get("print")
stats = importr('stats')
grdevices = importr('grDevices')
base = importr('base')
datasets = importr('datasets')

grid.activate()
lattice = importr('lattice')
datasets = importr('datasets')
mtcars = data(datasets).fetch('mtcars')['mtcars']
formula = Formula('mpg ~ wt')
formula.getenvironment()['mpg'] = mtcars.rx2('mpg')
formula.getenvironment()['wt'] = mtcars.rx2('wt')

p = lattice.xyplot(formula)

x = np.random.normal(loc=5, scale=2, size=10)
y = x + np.random.normal(loc=0, scale=2, size=10)
z = np.random.normal(loc=0, scale=2, size=10)

print ({'x': x, 'y': y, 'z': z})
testData = pd.DataFrame({'x': x, 'y': y, 'z': z})
# it looks just like a dataframe from R
print testData
robjects.pandas2ri.activate()
testData_R = robjects.conversion.py2ri(testData)

plotFunc = robjects.r("""
    library(ggplot2)

   function(df){
    p <- ggplot(df, aes(df$Position, df$Score)) +
    geom_point( )

   print(p)
    }
   """)


def runFromFileTest():
    rprint(p)
    fileName = "intermediateggplot2.R"
    contents = open(fileName).read()
    output = robjects.r(contents)
    print output
    plotFunc = robjects.r("""
     library(ggplot2)

    function(df){
     p <- ggplot(df, aes(x, y)) +
     geom_point( )

    print(p)
     }
    """)
    plotFunc(testData_R)


def plotSeqScores(score, seq1, seq2, scoreDict, isAffine):

    print isAffine
    if isAffine:
        plotSeqScoresAffine(score,seq1,seq2,scoreDict)
    else:
        print scoreDict
        print seq1
        print seq2
        # generate a list with all iterative alignment scores of seq1, seq2
        totalScore = 0
        scoreList = [totalScore]
        for i in xrange(len(seq1)):
            currentSeq1 = seq1[i]
            currentSeq2 = seq2[i]
            if (currentSeq1 == '-' or currentSeq2 == '-'):
                currentScore = -5
            else:
                currentScore = scoreDict[(currentSeq1, currentSeq2)]
            totalScore += currentScore
            scoreList.append(totalScore)
        indexList = range(0, len(scoreList))
        scoreData = pd.DataFrame({"Position": indexList, "Score": scoreList})
        print scoreData
        fileName = "Scripts/PlotScores.R"
        plotFunction = robjects.r(open(fileName).read())
        plot = plotFunction(scoreData)
        print(plot)

def plotSeqScoresAffine(score, seq1, seq2, scoreDict):

    print scoreDict
    print seq1
    print seq2
    # generate a list with all iterative alignment scores of seq1, seq2
    totalScore = 0
    scoreList = [totalScore]
    gapOpen = False
    for i in xrange(len(seq1)):
        currentSeq1 = seq1[i]
        currentSeq2 = seq2[i]
        if (currentSeq1 == '-' or currentSeq2 == '-'):
            if gapOpen:
                currentScore = -1
            else:
                currentScore = -11
                gapOpen = True
        else:
            currentScore = scoreDict[(currentSeq1, currentSeq2)]
            gapOpen = False
        totalScore += currentScore
        scoreList.append(totalScore)
    indexList = range(0, len(scoreList))
    scoreData = pd.DataFrame({"Position": indexList, "Score": scoreList})
    print scoreData
    fileName = "Scripts/PlotScores.R"
    plotFunction = robjects.r(open(fileName).read())
    plot = plotFunction(scoreData)
    print(plot)


def plotMatrixScores(score, seq1, seq2, isAffine):

    if isAffine:
        plotMatrixScoresAffine(score, seq1, seq2)
    else:
        blosum45 = "matrices/blosum45.txt"
        blosum62 = "matrices/blosum62.txt"
        blosum90 = "matrices/blosum90.txt"
        pam30 = "matrices/pam30.txt"
        pam70 = "matrices/pam70.txt"
        pam250 = "matrices/pam250.txt"
        matrixPathList = [blosum45, blosum62, blosum90, pam30, pam70, pam250]
        matrixNameList = ["blosum45", "blosum62", "blosum90", "pam30", "pam70", "pam250"]
        allIndices = []
        allScores = []
        allMatrices = []
        for j in xrange(len(matrixNameList)):
            scoreDict = makeScoringDict(matrixPathList[j])
            totalScore = 0
            allScores.append(totalScore)
            allMatrices.append(matrixNameList[j])
            for i in xrange(len(seq1)):
                currentSeq1 = seq1[i]
                currentSeq2 = seq2[i]
                if (currentSeq1 == '-' or currentSeq2 == '-'):
                    currentScore = -5
                else:
                    currentScore = scoreDict[(currentSeq1, currentSeq2)]
                totalScore += currentScore
                allScores.append(totalScore)
                allMatrices.append(matrixNameList[j])
            indexList = range(0, len(seq1) + 1)
            allIndices += indexList
        print(len(allIndices))
        print(len(allScores))
        print(len(allMatrices))
        scoreData = pd.DataFrame({"Position": allIndices, "Score": allScores, "Matrix": allMatrices})
        print scoreData
        fileName = "Scripts/PlotMatrixScores.R"
        plotFunction = robjects.r(open(fileName).read())
        plot = plotFunction(scoreData)
        print(plot)

def plotMatrixScoresAffine(score, seq1, seq2):

        blosum45 = "matrices/blosum45.txt"
        blosum62 = "matrices/blosum62.txt"
        blosum90 = "matrices/blosum90.txt"
        pam30 = "matrices/pam30.txt"
        pam70 = "matrices/pam70.txt"
        pam250 = "matrices/pam250.txt"
        matrixPathList = [blosum45, blosum62, blosum90, pam30, pam70, pam250]
        matrixNameList = ["blosum45", "blosum62", "blosum90", "pam30", "pam70", "pam250"]
        allIndices = []
        allScores = []
        allMatrices = []
        for j in xrange(len(matrixNameList)):
            scoreDict = makeScoringDict(matrixPathList[j])
            totalScore = 0
            allScores.append(totalScore)
            allMatrices.append(matrixNameList[j])
            gapOpen = False
            for i in xrange(len(seq1)):
                currentSeq1 = seq1[i]
                currentSeq2 = seq2[i]
                if (currentSeq1 == '-' or currentSeq2 == '-'):
                    if gapOpen:
                        currentScore = -1
                    else:
                        currentScore = -11
                        gapOpen = True
                else:
                    currentScore = scoreDict[(currentSeq1, currentSeq2)]
                    gapOpen = False
                totalScore += currentScore
                allScores.append(totalScore)
                allMatrices.append(matrixNameList[j])
            indexList = range(0, len(seq1) + 1)
            allIndices += indexList
        print(len(allIndices))
        print(len(allScores))
        print(len(allMatrices))
        scoreData = pd.DataFrame({"Position": allIndices, "Score": allScores, "Matrix": allMatrices})
        print scoreData
        fileName = "Scripts/PlotMatrixScores.R"
        plotFunction = robjects.r(open(fileName).read())
        plot = plotFunction(scoreData)
        print(plot)


def makeScoringDict(matrix_input):
    (keys, scoringMatrix) = MatrixParser.importMatrix(matrix_input)
    scoringMatrixDict = {}
    for i in xrange(len(keys)):
        for j in xrange(len(keys)):
            scoringMatrixDict[(keys[i], keys[j])] = scoringMatrix[i][j]
    return scoringMatrixDict

import MatrixParser
import sys


def fittingAlignment(s ,t ,matchScore, mismatchCost, indelCost, scoringMatrix, lookupDict ,best):

    if not(len(s)) > 0:
        return (best, (indelCost * len(t), '-' * len(t), t))
    if not (len(t)) > 0:
        return (best, (0 * len(s), s, '-' * len(s)))
    currentSuffixS = s[1:]
    currentSuffixT = t[1:]
    (solution1, lookupDict) = getSolution4(currentSuffixS, t, matchScore, mismatchCost, indelCost, scoringMatrix, lookupDict, best)
    (solution2, lookupDict) = getSolution4(s, currentSuffixT, matchScore, mismatchCost, indelCost, scoringMatrix, lookupDict, best)
    (solution3, lookupDict) = getSolution4(currentSuffixS, currentSuffixT, matchScore, mismatchCost, indelCost, scoringMatrix,
                                           lookupDict, best)
    a3 = scoringMatrix[s[0], t[0]]
    answers = [(indelCost + solution1[1][0], s[0] + solution1[1][1], '-' + solution1[1][2]),
               (indelCost + solution2[1][0], '-' + solution2[1][1], t[0] + solution2[1][2]),
               (a3 + solution3[1][0], s[0] + solution3[1][1], t[0] + solution3[1][2])]
    bestAlignmentIndex = 0
    currentBest = -sys.maxint - 1
    for i in xrange(len(answers)):
        if answers[i][0] > currentBest:
            currentBest = answers[i][0]
            bestAlignmentIndex = i
    best += [answers[bestAlignmentIndex]]
    return (best, answers[bestAlignmentIndex])


def getSolution4(suffix1, suffix2, matchScore, mismatchCost, indelCost, scoringMatrix, lookupDict, best):
    if (suffix1, suffix2) in lookupDict:
        solution = lookupDict[suffix1, suffix2]
    else:
        solution = fittingAlignment(suffix1, suffix2, matchScore, mismatchCost, indelCost, scoringMatrix, lookupDict, best)
        lookupDict[suffix1, suffix2] = solution
    return (solution, lookupDict)


def fittingAlignmentWrapper(fileName, matrixName):
    matrix_input = "matrices/" + matrixName.lower() + ".txt"
    (keys, scoringMatrix) = MatrixParser.importMatrix(matrix_input)
    contents = open(fileName).readlines()
    s = contents[0].strip()
    t = contents[1].strip()
    indelCost = -5
    matchScore = 1
    mismatchCost = -1
    lookupDict = {}
    scoringMatrixDict = {}
    for i in xrange(len(keys)):
        for j in xrange(len(keys)):
            scoringMatrixDict[(keys[i], keys[j])] = scoringMatrix[i][j]
    best = []
    (best, (score, s1, t1)) = fittingAlignment(s, t, matchScore, mismatchCost, indelCost, scoringMatrixDict, lookupDict, best)
    highestScore = 0
    (bestS, bestT) = ("", "")
    for i in best:
        if i[0] > highestScore and (checkSeq(i[2])) >= len(t):
            highestScore = i[0]
            (bestS, bestT) = (i[1], i[2])
    (cleanedS, cleanedT) = cleanSeqs(bestS, bestT)
    return (highestScore, cleanedS, cleanedT, scoringMatrixDict)

def checkSeq(s):

    eLen = 0
    for i in s:
        if i != '-':
            eLen+=1
    return eLen

def cleanSeqs(s,t):

    cleanedT = t.strip('-')
    sIndex = len(cleanedT)
    cleanedS = s[:sIndex]
    return cleanedS, cleanedT

sys.setrecursionlimit(10000)
import MatrixParser
import sys


def getSolution2(suffix1, suffix2, indelCost, scoringMatrixDict, lookupDict, best):
    if (suffix1, suffix2) in lookupDict:
        solution = lookupDict[suffix1, suffix2]
    else:
        (best, solution) = localAlignment(suffix1, suffix2, indelCost, scoringMatrixDict, lookupDict, best)
        lookupDict[suffix1, suffix2] = solution
    return (solution, lookupDict)


def localAlignment(s, t, indelCost, scoringMatrixDict, lookupDict, best):
    if not (len(s)) > 0:
        lookupDict[s, t] = (0, "", t)
        return (best, (0, "", t))
    if not (len(t)) > 0:
        lookupDict[s, t] = (0, s, "")
        return (best, (0, s, ""))
    currentSuffixS = s[1:]
    currentSuffixT = t[1:]
    (solution1, lookupDict) = getSolution2(currentSuffixS, t, indelCost, scoringMatrixDict, lookupDict, best)
    (solution2, lookupDict) = getSolution2(s, currentSuffixT, indelCost, scoringMatrixDict, lookupDict, best)
    (solution3, lookupDict) = getSolution2(currentSuffixS, currentSuffixT, indelCost, scoringMatrixDict, lookupDict,
                                           best)
    answers = [(indelCost + solution1[0], s[0] + solution1[1], '-' + solution1[2]),
               (indelCost + solution2[0], '-' + solution2[1], t[0] + solution2[2]),
               (scoringMatrixDict[(s[0], t[0])] + solution3[0], s[0] + solution3[1], t[0] + solution3[2]),
               (0, s[0] + "-", t[0] + "-")]
    bestAlignmentIndex = 0
    currentBest = -sys.maxint - 1
    for i in xrange(len(answers)):
        if answers[i][0] > currentBest:
            currentBest = answers[i][0]
            bestAlignmentIndex = i
    if bestAlignmentIndex == 3:
        # lookupDict[currentSuffixS, currentSuffixT] = (0, s[0]+solution3[1], t[0]+solution3[2])
        lookupDict[s, currentSuffixT] = (0, "", "")
        lookupDict[currentSuffixS, t] = (0, "", "")
    best += [answers[bestAlignmentIndex]]
    return (best, answers[bestAlignmentIndex])


# localAlignmentWrapper("texts\hw6\localAlignment.txt")
def localAlignmentWrapper(fileName, matrixName):
    matrix_input = "matrices/" + matrixName.lower() + ".txt"
    (keys, scoringMatrix) = MatrixParser.importMatrix(matrix_input)
    contents = open(fileName).readlines()
    s = contents[0].strip()
    t = contents[1].strip()
    indelCost = -5
    backtrack = []
    lookupDict = {}  # Used for memoization.
    scoringMatrixDict = {}  # dict mapping amino acid pair to blosum62 score.
    # seems easier than using lists
    for i in xrange(len(keys)):
        for j in xrange(len(keys)):
            scoringMatrixDict[(keys[i], keys[j])] = scoringMatrix[i][j]
    best = []
    (best, (score, s1, t1)) = localAlignment(s, t, indelCost, scoringMatrixDict, lookupDict, best)
    highestScore = 0
    (bestS, bestT) = ("", "")
    for i in best:
        if i[0] > highestScore:
            highestScore = i[0]
            (bestS, bestT) = (i[1], i[2])
    return (highestScore, bestS, bestT, scoringMatrixDict)


sys.setrecursionlimit(10000)

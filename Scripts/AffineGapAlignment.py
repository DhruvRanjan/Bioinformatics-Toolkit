import sys
import MatrixParser


def getSolutionL(s, t, scoringMatrixDict, lowerDict, upperDict, middleDict, gapOpen, gapExtend):
    if (s, t) in lowerDict:
        solution = lowerDict[s, t]
    else:
        solution = affineGapAlignment(s, t, scoringMatrixDict, lowerDict, upperDict, middleDict, gapOpen, gapExtend)
        lowerDict[s, t] = solution
    return (solution, lowerDict, upperDict, middleDict)


def getSolutionU(s, t, scoringMatrixDict, lowerDict, upperDict, middleDict, gapOpen, gapExtend):
    if (s, t) in upperDict:
        solution = upperDict[s, t]
    else:
        solution = affineGapAlignment(s, t, scoringMatrixDict, lowerDict, upperDict, middleDict, gapOpen, gapExtend)
        upperDict[s, t] = solution
    return (solution, lowerDict, upperDict, middleDict)


def getSolutionM(s, t, scoringMatrixDict, lowerDict, upperDict, middleDict, gapOpen, gapExtend):
    if (s, t) in middleDict:
        solution = middleDict[s, t]
    else:
        solution = affineGapAlignment(s, t, scoringMatrixDict, lowerDict, upperDict, middleDict, gapOpen, gapExtend)
        middleDict[s, t] = solution
    return (solution, lowerDict, upperDict, middleDict)


# affineGapAlignmentWrapper("texts\hw6\haffineGap.txt")
def affineGapAlignment(s, t, scoringMatrixDict, lowerDict, upperDict, middleDict, gapOpen, gapExtend):
    if not (len(s)) > 0:
        return (gapOpen + gapExtend * len(t), '-' * len(t), t)
    if not (len(t)) > 0:
        return (gapOpen + gapExtend * len(s), s, '-' * len(s))

    currentSuffixS = s[1:]
    currentSuffixT = t[1:]

    (lower1, lowerDict, upperDict, middleDict) = getSolutionL(currentSuffixS, t, scoringMatrixDict, lowerDict,
                                                              upperDict,
                                                              middleDict, gapOpen, gapExtend)
    # print "lower1: " + str(lower1)
    (lower2, lowerDict, upperDict, middleDict) = getSolutionM(currentSuffixS, t, scoringMatrixDict, lowerDict,
                                                              upperDict,
                                                              middleDict, gapOpen, gapExtend)
    # print "lower2: " + str(lower2)
    (upper1, lowerDict, upperDict, middleDict) = getSolutionU(s, currentSuffixT, scoringMatrixDict, lowerDict,
                                                              upperDict,
                                                              middleDict, gapOpen, gapExtend)
    # print "upper1: " + str(upper1)
    (upper2, lowerDict, upperDict, middleDict) = getSolutionM(s, currentSuffixT, scoringMatrixDict, lowerDict,
                                                              upperDict,
                                                              middleDict, gapOpen, gapExtend)
    # print "upper2: " + str(upper2)
    (middle1, lowerDict, upperDict, middleDict) = getSolutionL(currentSuffixS, currentSuffixT, scoringMatrixDict,
                                                               lowerDict,
                                                               upperDict, middleDict, gapOpen, gapExtend)
    # print "middle1: " + str(middle1)
    (middle2, lowerDict, upperDict, middleDict) = getSolutionM(currentSuffixS, currentSuffixT, scoringMatrixDict,
                                                               lowerDict,
                                                               upperDict, middleDict, gapOpen, gapExtend)
    # print "middle2: " + str(middle2)
    (middle3, lowerDict, upperDict, middleDict) = getSolutionU(currentSuffixS, currentSuffixT, scoringMatrixDict,
                                                               lowerDict,
                                                               upperDict, middleDict, gapOpen, gapExtend)
    # print "middle3: " + str(middle3)
    leftAnswer1 = (gapExtend + lower1[0], s[0] + lower1[1], '-' + lower1[2])
    leftAnswer2 = (gapOpen + lower2[0], s[0] + lower2[1], '-' + lower2[2])

    upperAnswer1 = (gapExtend + upper1[0], '-' + upper1[1], t[0] + upper1[2])
    upperAnswer2 = (gapOpen + upper2[0], '-' + upper2[1], t[0] + upper2[2])

    middleAnswer1 = (middle1[0], middle1[1], middle1[2])
    middleAnswer2 = (scoringMatrixDict[(s[0], t[0])] + middle2[0], s[0] + middle2[1], t[0] + middle2[2])
    middleAnswer3 = (middle3[0], middle3[1], middle3[2])

    bestLower = max(leftAnswer1[0], leftAnswer2[0])
    bestUpper = max(upperAnswer1[0], upperAnswer2[0])
    bestMiddle = max(middleAnswer1[0], middleAnswer2[0], middleAnswer3[0])

    if bestLower == leftAnswer1[0]:
        bestLowerAnswer = leftAnswer1
    else:
        bestLowerAnswer = leftAnswer2

    if bestUpper == upperAnswer1[0]:
        bestUpperAnswer = upperAnswer1
    else:
        bestUpperAnswer = upperAnswer2

    if bestMiddle == middleAnswer1[0]:
        bestMiddleAnswer = middleAnswer1
    elif bestMiddle == middleAnswer2[0]:
        bestMiddleAnswer = middleAnswer2
    else:
        bestMiddleAnswer = middleAnswer3

    bestOverallAnswer = max(bestLower, bestUpper, bestMiddle)

    if bestOverallAnswer == bestLower:
        return bestLowerAnswer
    elif bestOverallAnswer == bestUpper:
        return bestUpperAnswer
    else:
        return bestMiddleAnswer


def affineGapAlignmentWrapper(fileName, matrixName):
    matrix_input = "matrices/" + matrixName.lower() + ".txt"
    (keys, scoringMatrix) = MatrixParser.importMatrix(matrix_input)
    contents = open(fileName).readlines()
    s = contents[0].strip()
    t = contents[1].strip()
    gapOpen = -11
    gapExtend = -1
    lowerDict = {}
    upperDict = {}
    middleDict = {}
    scoringMatrixDict = {}  # dict mapping amino acid pair to blosum62 score.
    # seems easier than using lists
    for i in xrange(len(keys)):
        for j in xrange(len(keys)):
            scoringMatrixDict[(keys[i], keys[j])] = scoringMatrix[i][j]
    (score, s1, t1) = affineGapAlignment(s, t, scoringMatrixDict, lowerDict, upperDict, middleDict, gapOpen, gapExtend)
    return (score, s1, t1, scoringMatrixDict)

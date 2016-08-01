# Returns the global alignment and global alignment score of 2 DNA sequences.
# Requires 2 DNA sequences to compare and a txt file containing a scoring matrix (read using MatrixParser.py)

import MatrixParser
import sys

global lookupDict

def globalAlignment(s, t, indelCost, scoringMatrix, lookupDict):
    if not (len(s)) > 0:
        return indelCost * len(t), '-' * len(t), t
    if not (len(t)) > 0:
        return indelCost * len(s), s, '-' * len(s)
    currentSuffixS = s[1:]
    currentSuffixT = t[1:]
    (solution1, lookupDict) = getSolution(currentSuffixS, t, indelCost, scoringMatrix, lookupDict)
    (solution2, lookupDict) = getSolution(s, currentSuffixT, indelCost, scoringMatrix, lookupDict)
    (solution3, lookupDict) = getSolution(currentSuffixS, currentSuffixT, indelCost, scoringMatrix, lookupDict)
    answers = [(indelCost + solution1[0], s[0] + solution1[1], '-' + solution1[2]),
               (indelCost + solution2[0], '-' + solution2[1], t[0] + solution2[2]),
               (scoringMatrix[(s[0], t[0])] + solution3[0], s[0] + solution3[1], t[0] + solution3[2])]
    bestAlignmentIndex = 0
    currentBest = -sys.maxint - 1
    for i in xrange(len(answers)):
        if answers[i][0] > currentBest:
            currentBest = answers[i][0]
            bestAlignmentIndex = i
    return answers[bestAlignmentIndex]


def getSolution(suffix1, suffix2, indelCost, scoringMatrix, lookupDict):
    if (suffix1, suffix2) in lookupDict:
        solution = lookupDict[suffix1, suffix2]
    else:
        solution = globalAlignment(suffix1, suffix2, indelCost, scoringMatrix, lookupDict)
        lookupDict[suffix1, suffix2] = solution
    return (solution, lookupDict)


def globalAlignmentWrapper(fileName, matrixName, gap_cost):
    matrix_input = "matrices/" + matrixName.lower() + ".txt"
    (keys, scoringMatrix) = MatrixParser.importMatrix(matrix_input)
    contents = open(fileName).readlines()
    s = contents[0].strip()
    t = contents[1].strip()
    indelCost = gap_cost
    lookupDict = {}  # Used for memoization.
    scoringMatrixDict = {}  # dict mapping amino acid pair to blosum62 score.
    # seems easier than using lists
    for i in xrange(len(keys)):
        for j in xrange(len(keys)):
            scoringMatrixDict[(keys[i], keys[j])] = scoringMatrix[i][j]
    (score, s1, t1) = globalAlignment(s, t, indelCost, scoringMatrixDict, lookupDict)
    print len(lookupDict)
    return (score, s1, t1, scoringMatrixDict)


sys.setrecursionlimit(10000)

'''def test():
    globalAlignmentWrapper("../Tests/Alignment/globalAlignment.txt", "AH")


test()'''

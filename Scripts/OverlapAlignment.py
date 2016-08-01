import sys


def getSolution5(suffix1, suffix2, matchScore, mismatchCost, indelCost, lookupDict, best):
    if (suffix1, suffix2) in lookupDict:
        solution = lookupDict[suffix1, suffix2]
    else:
        solution = overlapAlignment(suffix1, suffix2, matchScore, mismatchCost, indelCost, lookupDict, best)
        lookupDict[suffix1, suffix2] = solution
    return (solution, lookupDict)


def overlapAlignment(s, t, matchScore, mismatchCost, indelCost, lookupDict, best):
    if not (len(s)) > 0:
        return (best, (0 * len(t), '-' * len(t), t))
    if not (len(t)) > 0:
        return (best, (indelCost * len(s), s, '-' * len(s)))
    currentSuffixS = s[1:]
    currentSuffixT = t[1:]
    (solution1, lookupDict) = getSolution5(currentSuffixS, t, matchScore, mismatchCost, indelCost, lookupDict, best)
    (solution2, lookupDict) = getSolution5(s, currentSuffixT, matchScore, mismatchCost, indelCost, lookupDict, best)
    (solution3, lookupDict) = getSolution5(currentSuffixS, currentSuffixT, matchScore, mismatchCost, indelCost,
                                           lookupDict, best)
    if s[0] == t[0]:
        a3 = matchScore
    else:
        a3 = mismatchCost
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


def overlapAlignmentWrapper(fileName):
    contents = open(fileName).readlines()
    s = contents[0].strip()
    t = contents[1].strip()
    indelCost = -2
    matchScore = 1
    mismatchCost = -2
    lookupDict = {}
    best = []
    (best, (score, s1, t1)) = overlapAlignment(s, t, matchScore, mismatchCost, indelCost, lookupDict, best)
    highestScore = 0
    (bestS, bestT) = ("", "")
    # print best
    for i in best:
        if i[0] > highestScore and (checkSeq(i[2])) >= len(t):
            highestScore = i[0]
            (bestS, bestT) = (i[1], i[2])
    (cleanedS, cleanedT) = cleanSeqs2(bestS, bestT)
    return (highestScore, cleanedS, cleanedT)

def checkSeq(s):
    eLen = 0
    for i in s:
        if i != '-':
            eLen += 1
    return eLen


def cleanSeqs2(s, t):
    cleanedS = s.strip('-')
    tIndex = len(cleanedS)
    cleanedT = t[:tIndex]
    return cleanedS, cleanedT

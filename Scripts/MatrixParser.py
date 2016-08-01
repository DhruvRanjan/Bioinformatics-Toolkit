#Parses scoring matrices (PAM, BLOSUM etc.) into a dictionary mapping AA pairs to scores
#Requires a txt file containing the scoring matrix as an input.

def importMatrix(fileName):

    contents = open(fileName).readlines()
    keys = [str(i) for i in contents[0].strip().split()]
    contents.pop(0)
    for i in xrange(len(contents)):
        line = contents[i][1:]
        line.strip()
        contents[i] = line
    scoring_matrix = [[int(i) for i in line.split()] for line in contents]
    return (keys, scoring_matrix)
import copy

def isSubset(buffer, sequence):
    for i in range(len(buffer) - len(sequence) + 1):
        isFound = True
        for j in range(len(sequence)):
            if buffer[i + j] != sequence[j]:
                isFound = False
                break
        if isFound:
            return True
    return False

def solver(matrixWidth, matrixHeight, bufferSize, sequence, sequenceReward, matrix):
    matrixIndex = [['' for _ in range(matrixWidth)] for _ in range(matrixHeight)]
    for i in range (matrixHeight):
        for j in range (matrixWidth):
            matrixIndex[i][j] = str(i) + str(j)

    isVertical = True
    numberOfBufferNow = 1
    buffer = [[x] for x in matrixIndex[0]]

    while (numberOfBufferNow < bufferSize):
        if (isVertical):
            for i in buffer:
                if (len(i) == numberOfBufferNow):
                    for j in range (matrixHeight):
                        if (matrixIndex[j][int(i[-1][1])] not in i):
                            buffer.append(i + [matrixIndex[j][int(i[-1][1])]])
                else: continue
            isVertical = False
        else:
            for i in buffer:
                if (len(i) == numberOfBufferNow):
                    for j in range (matrixWidth):
                        if (matrixIndex[int(i[-1][0])][j] not in i):
                            buffer.append(i + [matrixIndex[int(i[-1][0])][j]])
                else: continue
            isVertical = True
        numberOfBufferNow += 1

    bufferToken = copy.deepcopy(buffer)

    for i in range(len(bufferToken)):
        for j in range(len(bufferToken[i])):
            bufferToken[i][j] = matrix[int(bufferToken[i][j][0])][int(bufferToken[i][j][1])]

    maxScore = 0
    optimalBuffer = []
    for item in bufferToken:
        score = 0
        for j in sequence:
            if isSubset(item, j):
                score += int(sequenceReward[sequence.index(j)])
        if score > maxScore:
            maxScore = score
            optimalBuffer = item
    path = buffer[bufferToken.index(item)]
    for i in range (len(path)):
        temp1 = path[i][1]
        temp2 = path[i][0]
        path[i] = str(int(temp1)+1) + "," + str(int(temp2)+1)
    if (maxScore == 0):
        optimalBuffer = []
        path = []
    return (optimalBuffer, maxScore, path)
import random
from random import randint
import time
import function as func

# Time
start = time.time()

# KAMUS UMUM
sequence = []
sequenceReward = []

# INPUT
print("Apakah ingin menginput masukan melalui file atau CLI?")
print("(1) File txt")
print("(2) CLI")
choosenInput = int(input())

# Validate read from file or CLI
while choosenInput < 1 or choosenInput > 2:
    print("Input invalid, silakan input ulang!")
    print("Apakah ingin menginput masukan melalui file atau CLI? (ketik angkanya saja)")
    print("1. File txt")
    print("2. CLI")
    choosenInput = int(input())

# Read from file
if (choosenInput == 1):
    while True:
        file_name = input("Silakan masukkan nama file input (disertai dengan .txt): ")
        try:
            with open(file_name, 'r') as inputFile:
                bufferSize = int(inputFile.readline())
                matrixWidth, matrixHeight = map(int, inputFile.readline().split())
                matrix = [inputFile.readline().split() for _ in range(matrixHeight)]
                numberOfSequences = int(inputFile.readline())
                line_number = 0
                sequence = []
                sequenceReward = []
                for line in inputFile:
                    if line_number % 2 == 0:
                        sequence.append(line.split())
                    else:
                        sequenceReward.append(line.strip())
                    line_number += 1
                break  
        except FileNotFoundError:
            print("File tidak ditemukan, silahkan coba lagi.")

# Read from CLI
else:   
    jumlahTokenUnik = int(input("Masukkan jumlah token unik: "))
    while (jumlahTokenUnik < 1):
        jumlahTokenUnik = int(input("Jumlah token unik harus bilangan bulat positif! Masukkan jumlah token unik: "))
    preToken = input("Masukkan token dipisahkan dengan spasi: ")
    while (len(preToken.split()) != jumlahTokenUnik):
        preToken = input("Jumlah token tidak sesuai! Silakan masukkan token lagi: ")
    bufferSize = int(input("Masukkan ukuran buffer: "))
    while (bufferSize < 0):
        bufferSize = int(input("Ukuran buffer harus lebih dari sama dengan nol! Masukkan ukuran buffer: "))
    matrixHeight, matrixWidth = map(int, input("Masukkan ukuran matrix: ").split())
    while (matrixWidth < 1 or matrixHeight < 1):
        matrixHeight, matrixWidth = map(int, input("Ukuran matriks minimal 1x1! Masukkan ukuran matrix: ").split())
    numberOfSequences = int(input("Masukkan jumlah sekuens: "))
    while (numberOfSequences < 1):
        numberOfSequences = int(input("Jumlah sekuens harus lebih dari nol! Masukkan jumlah sekuens: "))
    sequenceMax = int(input("Masukkan ukuran maksimal sekuens: "))
    while (sequenceMax < 1):
        sequenceMax = int(input("Ukuran maksimal sekuens harus lebih dari nol! Masukkan ukuran maksimal sekuens: "))

    # Process token array, random matrix, random sequences, and random sequences reward
    token = preToken.split()
    matrix = [[random.choice(token) for _ in range(matrixWidth)] for _ in range(matrixHeight)]
    sequence = [[random.choice(token) for _ in range(random.randint(2, sequenceMax))] for _ in range(numberOfSequences)]
    sequenceReward = [random.randint(5, 100) for _ in range(numberOfSequences)]

    # Print matrix, sequences, and sequences reward
    print()
    print("Matriks: ")
    for i in matrix:
        for j in i:
            print(j, end=" ")
        print()
    print()
    print("Sekuens: ")
    for i in range (len(sequence)):
        for j in sequence[i]:
            print(j, end=" ")
        print(" reward = ", sequenceReward[i])

# VALIDATE INPUT 
isInputValid = True
if bufferSize < 0 or matrixHeight < 0 or matrixWidth < 0 or numberOfSequences < 0:
    print("Input invalid!")
    exit(1)
for row in matrix:
    for elmt in row:
        if (len(elmt) != 2):
            print("Input invalid!")
            exit(1)
for row in sequence:
    for elmt in row:
        if (len(elmt) != 2):
            print("Input invalid!")
            exit(1)

# Time 
end = time.time()

# PRINT RESULT
result, score, coordinate = func.solver(matrixWidth, matrixHeight, bufferSize, sequence, sequenceReward, matrix)
print()
print("Hasil: ")
print(score)
if (result == []):
    print("Score maksimal ketika buffer kosong!")
else:
    for i in result:
        print(i, end=' ')
    print()
    for i in coordinate:
        print(i)
print()
print((end-start)*1000, "ms")
print()

# SAVE RESULT TO TXT
wantToSave = input("Apakah ingin menyimpan solusi? (y/n) ")
if wantToSave == 'y':
    fileOutput = input("Silakan masukkan nama file output (tanpa .txt): ")
    while True:
        try:
            with open(fileOutput + ".txt", 'r') as outputFile:
                print("File dengan nama tersebut sudah ada, silakan coba lagi!")
                fileOutput = input("Silakan masukkan nama file output (tanpa .txt): ")
        except FileNotFoundError:
            with open(fileOutput + ".txt", 'a') as outputFile:
                outputFile.write(str(score))
                outputFile.write('\n')
                if (result == []):
                    outputFile.write("Score maksimal ketika buffer kosong!")
                else:
                    for i in result:
                        outputFile.write(str(i) + ' ')
                    outputFile.write('\n')
                    for i in coordinate:
                        outputFile.write(str(i))
                        outputFile.write('\n')
                print("Hasil berhasil disimpan dalam file", fileOutput + "." + "txt!")
                break 


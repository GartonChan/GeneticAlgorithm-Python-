import numpy as np

def getMatrixFromCSV(fileName, skiprows, usecols, dtype=float):
    matrix = []
    with open(fileName, 'r', encoding='utf-8') as csv:
        matrix = np.array(np.loadtxt(csv, delimiter=',', dtype=dtype, skiprows=skiprows, usecols=usecols))
    return matrix

def processOfData(matrix):
    # pre-process operations here!
    return matrix

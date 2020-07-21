import sys
import pandas as pd
import numpy as np

def invariantRanking(journalMeta: pd.DataFrame):
  references = journalMeta.drop(journalMeta.columns[[0, 1]], axis=1).to_numpy()
  noOfJournals = journalMeta.shape[0]
  totalNoOfReferences = np.sum(references, axis=1)
  noOfPubs = journalMeta['noOfPubs']

  A = np.zeros((noOfJournals + 1, noOfJournals))
  for i in range(noOfJournals):
    for j in range(noOfJournals):
      A[i, j] =  references[j, i] / totalNoOfReferences[j] * noOfPubs[j] / noOfPubs[i] - (1 if i == j else 0)
    A[noOfJournals, i] = noOfPubs[i]

  b = np.zeros(noOfJournals + 1)
  b[noOfJournals] =  100 * np.mean(noOfPubs)

  score = np.linalg.solve(A.T.dot(A), A.T.dot(b))
  return pd.DataFrame({'journal': journalMeta.iloc[:, 0], 'invariantRank': score}).sort_values(by='invariantRank', ascending=False)

if len(sys.argv) < 2:
  sys.stderr.write('Argument error. Usage: <path to journal references csv> <path to output csv>\n')
  sys.exit(1)

inputFile = sys.argv[1]
outputFile = sys.argv[2]

references = pd.read_csv(inputFile) 
ranking = invariantRanking(references)
ranking.to_csv(outputFile, index=False)

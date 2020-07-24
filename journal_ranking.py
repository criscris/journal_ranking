import sys
import pandas as pd
import numpy as np

def invariantRanking(
  noOfJournals: int,
  references: np.matrix,
  totalNoOfReferences: np.array,
  noOfPubs: np.array,
) -> np.array:
  A = np.zeros((noOfJournals + 1, noOfJournals))
  for i in range(noOfJournals):
    for j in range(noOfJournals):
      A[i, j] =  references[j, i] / totalNoOfReferences[j] * noOfPubs[j] / noOfPubs[i] - (1 if i == j else 0)
    A[noOfJournals, i] = noOfPubs[i]

  b = np.zeros(noOfJournals + 1)
  b[noOfJournals] =  100 * np.mean(noOfPubs)

  return np.linalg.solve(A.T.dot(A), A.T.dot(b))

def hitsRankScore(weight: float, citationPortion: float, noOfPubs_tobeRanked: int, noOfPubs_expert: int):
  return citationPortion * weight * noOfPubs_expert / noOfPubs_tobeRanked

def hitsWeightScore(ranking: float, citationPortion: float,  noOfPubs_tobeRanked: int, noOfPubs_expert: int):
  return citationPortion * ranking * noOfPubs_tobeRanked / noOfPubs_expert

def hitsRanking(
  noOfJournals: int,
  references: np.matrix,
  totalNoOfReferences: np.array,
  noOfPubs: np.array,
  getWeightScore = hitsWeightScore,
  getWeight = lambda sum: sum,
) -> np.array:
  averageNoOfPubsPerJournal = np.mean(noOfPubs)

  weights = np.full((noOfJournals), 100 / noOfJournals)
  scores = np.zeros(noOfJournals)

  prevIteration = {
    'weights': np.zeros(noOfJournals),
    'scores': np.zeros(noOfJournals),
  }

  for iteration in range(10000):
    # compute ranking (row)
    scores = np.zeros(noOfJournals)
    for i in range(noOfJournals):
      for j in range(noOfJournals):
        scores[i] += hitsRankScore(weights[j], references[j, i] / totalNoOfReferences[j], noOfPubs[i], noOfPubs[j])	
    
    # scale rankings 
    scores *= (100 * averageNoOfPubsPerJournal) / np.sum(scores * noOfPubs)

    # compute weights (column)
    weights = np.zeros(noOfJournals)
    for j in range(noOfJournals):
      for i in range(noOfJournals):
        weights[j] += getWeightScore(scores[i], references[j, i] / totalNoOfReferences[j], noOfPubs[i], noOfPubs[j])
      weights[j] = getWeight(weights[j])
    
    # scale weights
    weights *= (100 * averageNoOfPubsPerJournal) / np.sum(weights * noOfPubs)

    if np.allclose(scores, prevIteration['scores']) and np.allclose(weights, prevIteration['weights']):
      print(f'break after {iteration + 1} iterations')
      break
  
    prevIteration = {
      'weights': np.copy(weights),
      'scores': np.copy(scores),
    }
  
  return scores

if len(sys.argv) < 2:
  sys.stderr.write('Argument error. Usage: <path to journal references csv> <path to output csv>\n')
  sys.exit(1)

inputFile = sys.argv[1]
outputFile = sys.argv[2]

journalMeta = pd.read_csv(inputFile)
noOfJournals = journalMeta.shape[0]
references = journalMeta.drop(journalMeta.columns[[0, 1]], axis=1).to_numpy()
totalNoOfReferences = np.sum(references, axis=1)
noOfPubs = journalMeta['noOfPubs'].to_numpy()

invariant = invariantRanking(
  noOfJournals,
  references,
  totalNoOfReferences,
  noOfPubs,
)

hits = hitsRanking(
  noOfJournals,
  references,
  totalNoOfReferences,
  noOfPubs,
)

demange = hitsRanking(
  noOfJournals,
  references,
  totalNoOfReferences,
  noOfPubs,
  lambda ranking, citationPortion, noOfPubs_tobeRanked, noOfPubs_expert:
    citationPortion / (ranking * noOfPubs_tobeRanked) * noOfPubs_expert,
  lambda sum: 1 / sum,
)

result = pd.DataFrame({
  'journal': journalMeta.iloc[:, 0],
  'hits': hits,
  'demange': demange,
  'invariant': invariant,
}).sort_values(by='hits', ascending=False)

result.to_csv(outputFile, index=False)

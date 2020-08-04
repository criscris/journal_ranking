# Journal rankings

We reproduce and compare results of two publications:

Palacios-Huerta, I., and Volij, O. (2004): 
The measurement of intellectual influence.
Econometrica, 72(3), 963–977.

https://onlinelibrary.wiley.com/doi/pdf/10.1111/j.1468-0262.2004.00519.x

Demange, G. (2014): 
A ranking method based on handicaps. 
Theoretical Economics, 9(3), 915–942.

https://onlinelibrary.wiley.com/doi/pdf/10.3982/TE1217


## Installation

Install Docker from https://docs.docker.com/get-docker/

Then, run:

```
docker build --tag=journal_ranking .
```

## Run

```
docker run -it -v $(pwd):/root/journal_ranking journal_ranking
cd journal_ranking
python3 journalRanking.py references_economicJournals.csv ranking.csv
```

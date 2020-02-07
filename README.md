# PDI Project for integrating CD database with semantic duplicates

## Roadmap

v 1.1: NP strings eliminated.\
v 1.2: Scores available with optimum tracks left.\
v 1.3: compared tracks and got new score.\
v 1.4: Brute-force technique tried.\
v 2.0: Worked with complete range of thresholds.\
v 3.0: Errors calculated with respect to reference file.

## Instructions to use
1. Clone directory to your own machine.
2. Go to main directory _location/pdi/pdi_.
3. Use following command to run the program with pre-/defined threshold for sorting.\
`python main.py <threshold>`
Eg. `python main.py 75`

Not defining a threshold will run the program with the threshold of **80%**.

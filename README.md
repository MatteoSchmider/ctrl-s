# CTRL-S

This repository currently contains both python scripts and latex sources for a report on the financial viability of lithium ion based batteries in conjunction with solar power for the BürgerEnergiegenossenschaft Region Karlsruhe Ettlingen eG

All python scripts are intended to be executed from the repository's root directory.
To initialize the raw data:
* run "python ./data/populate-prices.py" to populate the energy prices files in ./data/prices/
* run "python ./data/production/convert_csv.py" to generate the production data from its sources in ./data/production/BEG Buchtzig.csv
Then, to generate the graphs and evaluation results:
* run "python ./scripts/evaluate_prices.py" to get the results in ./results/price-analysis/
* run "python ./scripts/evaluate_buchtzig.py" to get the results of the full simulation

---

## TODO:
* actually latexmk the current report state
* complete the report by filling in all the latex source files
* optimize the online algorithm used in the buchtzig evaluation
* generally try out and compare multiple specific setups in the buchtzig evaluation
* add real-world cost estimates for acquisition, installation and additional costs such as fire safety costs to the report
* write a short presentation in addition to the full report
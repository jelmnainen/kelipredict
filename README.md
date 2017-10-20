# Kelipredict
This is part of University of Helsinki's Introduction to Data Science 2017 miniproject.

The repo contains three python modules:

- scrape.py scrapes keliapu.net/data/ for .csv files and puts them under ./data/
- filter.py filters those files for values near Kumpula and puts all those files under ./processedData/
- compose.py takes values from ./processedData/ and composes them into a single .csv file under ./finalData/

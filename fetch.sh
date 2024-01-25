#!/bin/bash

# Define a fixed date range
yesterday_date=$(date -d "yesterday" +%Y/%m/%d)
today=$(date +%Y/%m/%d)

# Fetch meta-analysis abstracts within the fixed date range
esearch -db pubmed -query "meta-analysis[Publication Type] AND ($yesterday_date[PDAT] : $today[PDAT])" | \
efetch -format abstract > meta_dataset.txt

# Fetch randomized controlled trial abstracts within the fixed date range
esearch -db pubmed -query "\"randomized controlled trial\"[Publication Type] AND ($yesterday_date[PDAT] : $today[PDAT])" | \
efetch -format abstract > rct_dataset.txt

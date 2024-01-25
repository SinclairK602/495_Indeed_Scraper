#!/bin/bash

# Set the timeout duration in seconds
TIMEOUT_DURATION=5  # For example, 5 seconds

# Check if a PMID is provided as an argument
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <pmid>"
    exit 1
fi

# Assign the provided PMID to a variable
PMID=$1

# Use Entrez Direct with a timeout
timeout $TIMEOUT_DURATION esearch -db pubmed -query $PMID | \
efetch -format abstract > request.txt

# Check the exit status of the timeout command
EXIT_STATUS=$?

if [ $EXIT_STATUS -eq 124 ]; then
    echo "Timed out while fetching abstract for PMID $PMID."
    exit 1
elif [ $EXIT_STATUS -eq 0 ]; then
    echo "Abstract for PMID $PMID fetched successfully."
else
    echo "Failed to fetch abstract for PMID $PMID."
    exit 1
fi

#!/bin/bash

# Default values for URLs and destination directory
SPEECHES_CSV="https://dataverse.harvard.edu/api/access/datafile/4745985"
POLITICIANS_TAB="https://dataverse.harvard.edu/api/access/datafile/6544762"
FACTIONS_TAB="https://dataverse.harvard.edu/api/access/datafile/6544758"
DEST_DIR="../data"

# Parse command-line arguments
while getopts "s:p:f:d:" opt; do
  case $opt in
    s) SPEECHES_CSV="$OPTARG"
    ;;
    p) POLITICIANS_TAB="$OPTARG"
    ;;
    f) FACTIONS_TAB="$OPTARG"
    ;;
    d) DEST_DIR="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
        exit 1
    ;;
  esac
done

# Names for the downloaded files
SPEECHES_FILE="speeches.csv"
POLITICIANS_FILE="politicians.tab"
FACTIONS_FILE="factions.tab"

# Check if the destination directory exists, if not, create it
if [ ! -d "$DEST_DIR" ]; then
  mkdir -p "$DEST_DIR"
fi

# Download the SPEECHES_CSV file
wget -O "$SPEECHES_FILE" "$SPEECHES_CSV"
# Check if the download was successful and move the file to /data
if [ $? -eq 0 ]; then
  mv "$SPEECHES_FILE" "$DEST_DIR/$SPEECHES_FILE"
  echo "SPEECHES_CSV file downloaded successfully to $DEST_DIR"
else
  echo "Failed to download SPEECHES_CSV file"
fi

# Download the POLITICIANS_TAB file
wget -O "$POLITICIANS_FILE" "$POLITICIANS_TAB"
# Check if the download was successful and move the file to /data
if [ $? -eq 0 ]; then
  mv "$POLITICIANS_FILE" "$DEST_DIR/$POLITICIANS_FILE"
  echo "POLITICIANS_TAB file downloaded successfully to $DEST_DIR"
else
  echo "Failed to download POLITICIANS_TAB file"
fi

# Download the $FACTIONS_TAB file
wget -O "$FACTIONS_FILE" "$FACTIONS_TAB"
# Check if the download was successful and move the file to /data
if [ $? -eq 0 ]; then
  mv "$FACTIONS_FILE" "$DEST_DIR/$FACTIONS_FILE"
  echo "$FACTIONS_TAB file downloaded successfully to $DEST_DIR"
else
  echo "Failed to download $FACTIONS_TAB file"
fi

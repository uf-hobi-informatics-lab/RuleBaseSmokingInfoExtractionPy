# Quantitative Smoke Status Extraction
This package aims to extract discrete smoking information from clinical narrative text.

## Smoking information type
* pack per day (PPD)
* pack-year (PY)
* smoking year (SY)
* quit year – e.g., quit for 10 years (QY)
* year at quit – e.g., quit at 2008 (YQ)

## Input format
### Individual text files:
A directory containing your individual clinical notes in .txt format. Each file will produce one output file in .ann format.
### CSV file:
A .csv file with no header expected to contain the following information:
* patient ID
* note ID
* note date
* note type
* note text

The output file will be a .csv of the same format, with added fields for each category. If no value for a given category was obtained, the corresponding cell will be left blank.

## Running the package:
Depending on your file input strategy, please run either of the following commands:
#### For individual text files
    python run_engine.py directory/containing/notes/
#### For single .csv file
    python run_engine.py path/to/your/file.csv

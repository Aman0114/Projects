#!/bin/bash

# Create requirements.txt
cat <<EOL > requirements.txt
beautifulsoup4
requests
gspread
pandas
selenium
gspread-dataframe
numpy
EOL

# Install the requirements
pip install -r requirements.txt

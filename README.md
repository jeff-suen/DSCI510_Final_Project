# Financial News Headlines Sentiment Analysis (TSLA)

## Table of Contents

- [Financial News Headlines Sentiment Analysis](#project-name)
  - [Table of Contents](#table-of-contents)
  - [Description](#description)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
  - [Usage](#usage)

## Description

The project is focused on the rapid dissemination of financial news in the modern, internet- driven age, where information spreads within seconds. This immediacy contrasts sharply with the past, where it took days for such news to reach people through radio, newspapers, and word of mouth. The project notes that financial news articles are now often generated automatically from data like figures and earnings call streams.
This project utilizes data science techniques such as Natural Language Process, Data Extraction and Parsing and Data Visualization, to process this abundant information, aiming to generate investing insights. It's particularly relevant for hedge funds and independent traders who leverage such methods for profit. The project involves analyzing news headlines to assess market sentiment and make investment decisions with a comprehensive visualization. 
The project aims to analyze data realted to Tesla Inc.

## Getting Started

Explain how to get your Python project up and running. Include any necessary steps, prerequisites, or Python dependencies.

### Prerequisites

Python 3.11.5 and additional libraries:
```python
requests == 2.31.0
pandas == 2.0.3
bs4 == 0.0.1
numpy == 1.24.3
nltk == 3.8.1
matplotlib == 3.7.2
statsmodels == 0.14.0
seaborn == 0.12.2
```

### Installation

Clone the repository to your local machine.
Install the required Python packages:

```cmd
pip install -r requirements.txt
```
The file "requirements2.txt" contains the result obtained by "pip freeze >> requirements.txt" for the purpose of reference.

## Usage
To start the project, run the scripts in the following order:
```cmd
# Navigate to the code directory
cd src
# getting data
python get_data.py
# cleaning data
python clean_data.py
# running analysis
python run_analysis.py
# visualizing results
python visualize_results.py
```

## Contact
[Shuju Sun] - [shujusun@usc.edu]



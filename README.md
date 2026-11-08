# titanic_analysis

This repository includes the submission of homework 3 for MLDS 400 class. For this homewor, I implemented a logistic regression pipeline to predict passenger survival on the titanic.

## Running the pipeline
Both pipelines are runned by dockerß

To run the full pipelines after cloning the repo, first download the data from https://www.kaggle.com/competitions/titanic/code. There are three csv files to download from this kaggle dataset: `train.csv, test.csv, gender_submission.csv`
All three csvs should be moved under `data/` under the root directory of the repo.


then build the following image in the **root directory of the repo** with

```bash
docker build -t 400hw3-r -f src/rscripts/Dockerfile .   # R image
docker build -t 400hw3 .                                # Python image
```

run the following codes in the same directory to run the project
```bash
docker run --rm 400hw3-r        # R image
docker run --rm 400hw3          # Python image
```


## Structure of the repo

hw3/
├── Dockerfile                  # Dockerfile for python image
├── Homework 3.ipynb            # HW instruction in case of further needs 
├── .dockerignore                
├── .gitignore
├── data/                       # data downloaded from kaggle
    ├── train.csv
    ├── test.csv
    ├── gender_submission.csv
└── src/
    ├── scripts/                # main.py, requirements.txt
        └── main.py             # main pipeline for python logistic regression
        └── requirements.txt    # python package requirement
    └── rscripts/
        ├── Dockerfile          # dockerfile for R image
        └── main.R              # main pipeline for R pipeline
        └── install_packages.R  # Script to install necessary packages to the container

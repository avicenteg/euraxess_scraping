# Euraxess Web Scraper

## Authors
+ Pablo Román-Naranjo Varela
+ Adrián Vicente Gómez

## Background
This project, framed within the subject 'Tipología y ciclo de vida de los datos' of the [Data Science MSc at UOC](https://estudios.uoc.edu/es/masters-universitarios/data-science/presentacion), aims to build a **web scraper with python**. In our case, we decided to build a web scraper to gather information from **[EURAXESS](https://euraxess.ec.europa.eu)**, a website that provides worldwide job opportunities in research.

## Justification and project scope  
It is not always easy to find job opportunities if you are interested in beginning to do research in a certain field. In this sense, having an up-to-date dataset with job offers in your field of interest would simplify this search. This dataset could be generated using web scraping methods.

Although the web scraper we built could be applied to every field, in this project we focused in opportunities related with data science (i.e. data scientist, data analyst, data engineer...) published on [EURAXESS](https://euraxess.ec.europa.eu).

## Main and specific objectives
The main objective of this project is to **generate a dataset of research opportunities** related with **data science** published on [EURAXESS](https://euraxess.ec.europa.eu) **building and applying a web scraper in python**. Besides, we proposed the following specific aims:
+ To perform **Exploratory Data Analyses (EDA)** to investigate generated datasets and summarize key insights.
+ To use **Data visualization** methods to easily interpret the data.

## Dataset description
The dataset generated with this package contains job offers obtained from EURAXESS. Each row of the dataset contains different job offers and its attributes. In the example table showed below, the dataset was obtained using "Data Science" as keyword, but another keywords would result in different datasets. The complete dataset is available on Zenodo (doi:[10.5281/zenodo.5636238](https://zenodo.org/record/5636238#.YYBLe57MJhG)). The columns describing the dataset are:
+ Job Offer Title: Title of the job offer.
+ Researcher Profile: Expected applicant profile/s.
+ Company: Company offering the job.
+ Field: Research field of the job offer.
+ Hours/Week: Weekly working hours.
+ Country: Country where the job is offered.
+ City: City where the job is offered.
+ Where to Apply: Url or email where to apply to the offer.
+ More info: URL where the offer can be located.

| Job Offer Title                           | Researcher Profile                                                                     | Company                                        | Field                                              | Hours/Week | Country     | City     | Where to Apply                                                                                 | More Info                                 |
|-------------------------------------------|----------------------------------------------------------------------------------------|------------------------------------------------|----------------------------------------------------|------------|-------------|----------|------------------------------------------------------------------------------------------------|-------------------------------------------|
| Data Scientist                            | First Stage Researcher (R1) , Recognised Researcher (R2) , Established Researcher (R3) | Centro de Biología Molecular Severo Ochoa      | Biological sciences, Computer science, Programming | 37.5       | Spain       | Madrid   | mailto:m.llorens@csic.es                                                                       | https://euraxess.ec.europa.eu/jobs/692406 |
| Data scientist \| Postdoctoral researcher | Recognised Researcher (R2)                                                             | Radboud University Medical Center (Radboudumc) | Physics                                            | 36.0       | Netherlands | Nijmegen | https://www.academictransfer.com/en/305147/data-scientist-postdoctoral-researcher/apply/#apply | https://euraxess.ec.europa.eu/jobs/695497 |
| Data Scientist                            | First Stage Researcher (R1)                                                            | UNIVERSIDAD DE BURGOS                          | Computer science, Other                            | 37.5       | Spain       | Burgos   |                                                                                                | https://euraxess.ec.europa.eu/jobs/700503 |

## License
This project and all the datasets derived from it are realesed under CC BY-NC-SA 4.0 License. [See more](https://github.com/avicenteg/euraxess_scraping/blob/master/LICENSE.md)

## How to install?
To use this web scraper coded in python, it will be necessary to install the dependencies specified in the [requirements.txt](https://github.com/avicenteg/euraxess_scraping/blob/master/scraping/requirements.txt) file on this repository.

```
pip install -r requirements.txt
```

## How it works

![alt text](https://github.com/avicenteg/euraxess_scraping/blob/master/images/schema.png "Application Schema")

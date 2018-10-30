# Table of Contents
Problem, Approach and Run instructions sections
1. [Problem](README.md#problem)
2. [Approach](README.md#approach)
3. [Instructions](README.md#instructions)
4. [output](README.md#output)


# Problem

In order to support the analysis of data trends on H1B(H-1B, H-1B1, E-3) visa application processing over the past years, This code is designed to calculate two metrics: **Top 10 Occupations** and **Top 10 States** for **certified** visa applications.
The input data is based on statistics available from the US Department of Labor and its [Office of Foreign Labor Certification Performance Data](https://www.foreignlaborcert.doleta.gov/performancedata.cfm#dis). 

# Approach

*  First the input data in input folder will be read into csv.DictReader, and append as dictionary with their counts
*  Then the top 10 data will be generated based on number first and alphabetic second rule
*  The final result with pecentage format will bse saved as txt file to the output folder

# Instructions

Python 3.6 
* Git: git clone hhttps://github.com/Catherinesdataanalytics/h1b_statistics_analysis.git
* Check your input data format (data needs to be in csv format ) and column names( status needs to be "STATUS" or "CASE_STATUS"; state needs to be "LCA_CASE_WORKLOC1_STATE"or "WORKSITE_STATE"; occupation needs to be "LCA_CASE_SOC_NAME" or "SOC_NAME"
* put the data in csv format to the input folder.
* cd to your download local directory and  the run.sh file using . run.sh

# Output 
top_10_states.txt  and top_10_occupations.txt  will be automatically generated into the output folder.


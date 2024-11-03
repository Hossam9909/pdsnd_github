>**Note**: Please **fork** the current Udacity repository so that you will have a **remote** repository in **your** Github account. Clone the remote repository to your local machine. Later, as a part of the project "Post your Work on Github", you will push your proposed changes to the remote repository in your Github account.

# Bikeshare Data Analysis

This project analyzes bikeshare data for three major cities in the United States—Chicago, New York City, and Washington—allowing users to filter the data by city, month, and day, and view various statistics.

### Date created
3 November 2024

### Project Title
Bikeshare Data Analysis

### Description
This Python project enables users to explore bikeshare data for three U.S. cities by filtering data based on city, month, and day. The program calculates key statistics, including:
- The most frequent times of travel.
- The most popular stations and trips.
- Trip duration details (total and average).
- User demographics, including age groups and gender distribution.
- Plots showing distributions of user types, gender, and age groups.

### Features
- **Filtering Options**: Users can filter by city, specific month, and day of the week.
- **Data Visualization**: Displays tables and generates plots, such as user type distribution and age group breakdowns.
- **Error Handling**: Robust handling for missing data or empty datasets.

### Files used
- **`bikeshare.py`**: Main Python script for running the bikeshare data analysis.
- **Data files**: `chicago.csv`, `new_york_city.csv`, `washington.csv` (containing bikeshare trip data for each city).

### Installation
1. Clone this repository and navigate to the project directory:
    ```bash
    git clone https://github.com/hossam9909/bikeshare-data-analysis.git
    cd bikeshare-data-analysis
    ```

2. Install the required dependencies:
    ```bash
    pip install pandas numpy matplotlib tabulate

### How to Run
1. Ensure the required data files are in the same directory as `bikeshare.py`.
2. Run the script:
    ```bash
    python bikeshare.py
    ```

### Usage Examples
- **Example 1**: View data for Chicago in March, on Mondays.
- **Example 2**: Analyze data for New York City for the month of June, without filtering by a specific day.
- **Example 3**: Explore data for Washington across all available data without additional filtering.


### Requirements
- Python 3.6+
- Required packages: `pandas`, `numpy`, `matplotlib`, `tabulate`

### Credits
This project was inspired by Udacity's Data Analyst Nanodegree program.


import time
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt
from tabulate import tabulate  # Importing tabulate

# Global variables to store city, month, and day
city = ''
month = ''
day = ''

# Dictionary mapping city names to their corresponding CSV files
CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def display_raw_data(df):
    """Displays the raw data in the DataFrame in chunks of 5 lines."""
    show = input("Would you like to see the raw data? (yes/no): ").strip().lower()
    if show == "yes":
        start_index = 0
        while True:
            print(df.iloc[start_index:start_index + 5])
            start_index += 5
            if start_index >= len(df):
                print("No more data to display.")
                break
            response = input("Would you like to see the next 5 lines? (yes/no): ").strip().lower()
            if response != "yes":
                break

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    global city, month, day  # Declare global variables
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # Get user input for city
    while city not in CITY_DATA.keys():
        city = input("Please choose a city (chicago, new york city, washington): ").strip().lower()

    # Get user input for month
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while month not in months:
        month = input("Please choose a month ( january, february, march, april, may, june) or all for no filter: ").strip().lower()

    # Get user input for day
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while day not in days:
        day = input("Please choose a day of the week ( monday, tuesday, wednesday, thursday, friday, saturday, sunday) or all for no filter: ").strip().lower()

    print('-' * 40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter

    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        month_index = ['january', 'february', 'march', 'april', 'may', 'june'].index(month) + 1
        df = df[df['month'] == month_index]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print(f'\nCalculating The Most Frequent Times of Travel in {city.title()} for {month.title()} month(s) {day.title()} day(s)...\n')
    start_time = time.time()

    # Check if the DataFrame is empty
    if df.empty:
        print("The DataFrame is empty. No statistics to calculate.")
        return

    # Ensure 'Start Time' is in datetime format
    if 'Start Time' not in df.columns:
        print("Error: 'Start Time' column is missing from the DataFrame.")
        return

    # Convert 'Start Time' to datetime if not already
    df['Start Time'] = pd.to_datetime(df['Start Time'], errors='coerce')

    # Most common month
    if 'month' in df.columns:
        most_frequent_month_num = df['month'].mode()[0] if not df['month'].empty else None
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        most_frequent_month = months[most_frequent_month_num - 1] if most_frequent_month_num is not None else None
    else:
        print("Warning: 'month' column is missing. Cannot calculate most frequent month.")
        most_frequent_month = None

    # Most common day of week
    if 'day_of_week' in df.columns:
        most_frequent_day = df['day_of_week'].mode()[0] if not df['day_of_week'].empty else None
    else:
        print("Warning: 'day_of_week' column is missing. Cannot calculate most frequent day.")
        most_frequent_day = None

    # Most common start hour
    df['hour'] = df['Start Time'].dt.hour  # Extract hour from 'Start Time'
    most_frequent_hour = df['hour'].mode()[0] if not df['hour'].empty else None
    if most_frequent_hour is not None:
        most_frequent_hour = f"{most_frequent_hour % 12 or 12} {'AM' if most_frequent_hour < 12 else 'PM'}"

    # Create a DataFrame with the statistics
    stats_df = pd.DataFrame({
        'Statistic': ['Most Frequent Month', 'Most Frequent Day of Week', 'Most Frequent Start Hour'],
        'Value': [most_frequent_month, most_frequent_day, most_frequent_hour]
    })

    # Print the table using tabulate
    print(tabulate(stats_df, headers='keys', tablefmt='markdown'))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print(f'\nCalculating The Most Popular Stations and Trip in {city.title()} for {month.title()} month(s) {day.title()} day(s)...\n')
    start_time = time.time()

    # Check if the DataFrame is empty
    if df.empty:
        print("The DataFrame is empty. No statistics to calculate.")
        return

    # Check for required columns
    required_columns = ['Start Station', 'End Station']
    for column in required_columns:
        if column not in df.columns:
            print(f"Error: '{column}' column is missing from the DataFrame.")
            return

    # Most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0] if not df['Start Station'].empty else None
    # Most commonly used end station
    most_common_end_station = df['End Station'].mode()[0] if not df['End Station'].empty else None
    # Most frequent combination of start station and end station trip
    df['Start Station & End Station'] = df['Start Station'] + ' - ' + df['End Station']
    most_common_trip = df['Start Station & End Station'].mode()[0] if not df['Start Station & End Station'].empty else None

    # Create a DataFrame with the statistics
    stats_df = pd.DataFrame({
        'Statistic': ['Most Commonly Used Start Station', 'Most Commonly Used End Station', 'Most Frequent Trip'],
        'Value': [most_common_start_station, most_common_end_station, most_common_trip]
    })

    # Print the table using tabulate
    print(tabulate(stats_df, headers='keys', tablefmt='markdown'))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def format_timedelta(td):
    """Formats a timedelta object to hours, minutes, and seconds."""
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours} hour(s), {minutes} minute(s), {seconds} second(s)"

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print(f'\nCalculating Trip Duration in {city.title()} for {month.title()} month(s) {day.title()} day(s)...\n')
    start_time = time.time()

    # Check if the DataFrame is empty
    if df.empty:
        print("The DataFrame is empty. No statistics to calculate.")
        return None, None

    # Check if 'Trip Duration' exists in the DataFrame
    if 'Trip Duration' not in df.columns:
        print("'Trip Duration' column is missing in the DataFrame.")
        return None, None

    # Handle case with one entry (same total and mean)
    if len(df) == 1:
        print("Only one trip available, so total and mean are the same.")
    
    # Total travel time (summing directly as integers, assuming the original data is in seconds)
    total_travel_time_seconds = df['Trip Duration'].sum()

    # Mean travel time (calculated in seconds first)
    mean_travel_time_seconds = df['Trip Duration'].mean()

    # Create a DataFrame with the statistics
    stats_df = pd.DataFrame({
        'Statistic': ['Total Travel Time', 'Mean Travel Time'],
        'Value': [format_timedelta(pd.to_timedelta(total_travel_time_seconds, unit='s')), 
                  format_timedelta(pd.to_timedelta(mean_travel_time_seconds, unit='s'))]
    })
    
    # Print the table using tabulate
    print(tabulate(stats_df, headers='keys', tablefmt='markdown')) 

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def rush_hour_analysis(df):
    print('\nAnalyzing rush hours...\n')
    start_time = time.time()

    df['Hour'] = df['Start Time'].dt.hour
    busy_hours = df['Hour'].value_counts().sort_index()

    print("Number of trips by hour:")
    print(busy_hours)

    plt.figure(figsize=(12, 6))
    busy_hours.plot(kind='bar')
    plt.title('Number of Trips by Hour')
    plt.xlabel('Hour of Day')
    plt.ylabel('Number of Trips')
    plt.savefig('trips_by_hour.png')
    plt.close()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40) 

def plot_gender_distribution(df):
    """
    Plots a pie chart showing the distribution of gender, with handling for missing or incomplete data.
    
    Args:
        df: DataFrame containing the 'Gender' column.
    """
    # Check if the 'Gender' column exists
    if 'Gender' not in df.columns:
        print("'Gender' column is missing in the DataFrame.")
        return
    
    # Count the occurrences of each gender, including NaN values
    gender_counts = df['Gender'].value_counts(dropna=False)
    
    # If the entire column is NaN or empty, handle it
    if gender_counts.empty or gender_counts.isnull().all():
        print("No gender data available to display.")
        return
    
    # Handle cases where there are NaN values but some data
    gender_counts = gender_counts.rename(index={np.nan: 'Unknown'})  # Rename NaN to "Unknown"
    
    # Display counts
    print(f"Gender counts:\n{gender_counts}")
    
    # Plot the pie chart
    try:
        plt.figure(figsize=(6, 6))
        gender_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90)
        plt.title('Gender Distribution (Including Unknown)')
        plt.ylabel('')  # Hide the y-label
        plt.savefig('gender_distribution.png')  # Save the plot as a PNG file
        plt.show()  # Display the plot if possible
        plt.close()  # Close the plot to free up memory
    except Exception as e:
        print(f"An error occurred while plotting: {e}")

    
def user_stats(df):
    """Displays statistics on bikeshare users."""
    print(f'\nCalculating User Stats in {city.title()} for {month.title()} month(s) {day.title()} day(s)...\n')
    start_time = time.time()

    # Counts of user types
    user_types = df['User Type'].value_counts()

    # Counts of gender
    gender_counts = df['Gender'].value_counts() if 'Gender' in df else None

    # Earliest, most recent, and most common year of birth
    earliest_birth_year = df['Birth Year'].min() if 'Birth Year' in df else None
    most_recent_birth_year = df['Birth Year'].max() if 'Birth Year' in df else None
    most_common_birth_year = df['Birth Year'].mode()[0] if 'Birth Year' in df and not df['Birth Year'].empty else None

    # Create a DataFrame with the statistics
    stats_data = {
        'Statistic': ['User  Types', 'Gender Counts', 'Earliest Birth Year', 'Most Recent Birth Year', 'Most Common Birth Year'],
        'Value': [user_types.to_dict(), gender_counts.to_dict() if gender_counts is not None else 'N/A', earliest_birth_year, most_recent_birth_year, most_common_birth_year]
    }
    
    stats_df = pd.DataFrame(stats_data)

    # Print the table using tabulate
    print(tabulate(stats_df, headers='keys', tablefmt='markdown'))

    """Plots user type counts as a bar chart."""
    try:
        user_types.plot(kind='bar')
        plt.title('User  Types')
        plt.xlabel('User  Type')
        plt.ylabel('Count')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('user_types.png')  # Save the plot as a PNG file
        plt.show()  # Display the plot if possible
        plt.close()  # Close the plot to free up memory
    except Exception as e:
        print(f"An error occurred while plotting user types: {e}")

    plot_gender_distribution(df)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)
    
def age_group_stats(df):
    """Displays statistics on user age groups and plots a pie chart."""
    print(f'\nCalculating Age Group Stats...\n')
    start_time = time.time()

    # Check if 'Birth Year' exists in the DataFrame
    if 'Birth Year' not in df.columns:
        print("'Birth Year' column is missing in the DataFrame.")
        return

    # Calculate current age
    current_year = pd.to_datetime('now').year
    df['Age'] = current_year - df['Birth Year']

    # Define age bins and labels
    bins = [0, 17, 24, 34, 44, 54, 64, 100]  # Age groups
    labels = ['Under 18', '18-24', '25-34', '35-44', '45-54', '55-64', '65+']
    
    # Create a new column for age groups
    df['Age Group'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)

    # Count the number of users in each age group
    age_group_counts = df['Age Group'].value_counts().sort_index()

    # Create a DataFrame for better display
    age_group_df = pd.DataFrame({
        'Age Group': age_group_counts.index,
        'Count': age_group_counts.values
    })

    # Print the table using tabulate
    print(tabulate(age_group_df, headers='keys', tablefmt='markdown'))

    # Plotting the pie chart
    try:
        plt.figure(figsize=(8, 8))
        age_group_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90)
        plt.title('Age Group Distribution')
        plt.ylabel('')  # Hide the y-label
        plt.savefig('age_group_distribution.png')  # Save the plot as a PNG file
        plt.show()  # Display the plot if possible
        plt.close()  # Close the plot to free up memory
    except Exception as e:
        print(f"An error occurred while plotting age group distribution: {e}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def main():
    while True:
        # Reset global variables
        global city, month, day
        city = ''
        month = ''
        day = ''
        city, month, day = get_filters()
        df = load_data(city, month, day)
        display_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        age_group_stats(df)
        rush_hour_analysis(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.strip().lower() != 'yes':
            break

if __name__ == "__main__":
    main()

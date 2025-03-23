#Import libraries :
import pandas as pd
import numpy as np
import time
"""Libraries Using : Numpy , Pandas for Data Manipulation and Time library.
 Project target :  explore data for bikeshare in Three cities in US (Chicago, Washington, and NYC).
"""
#Loading data from datasets 'CSVs'
CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york': 'new_york_city.csv',
    'washington': 'washington.csv'
}


# Valid values of cities-months and days in lists.
valid_cities = ['chicago', 'new york', 'washington']
valid_months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
valid_days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']

def get_filters():
    """
    Ask user to select filters for city, month, and day.

    Returns:
        city (str): name of the city to analyze
        month (str): name of the month to filter by or 'all'
        day (str): name of the day of week to filter by or 'all'
    """
    print("Welcome! Let's explore US bikeshare data.")

    # Get the input from user for a city.
    while True:
        city = input("Choose a city (Chicago, New York, Washington): ").strip().lower()
        if city in valid_cities:
            break
        print("Invalid city. Try again.")

    # Ask for Filter type.
    while True:
        filter_choice = input("Would you like to filter by 'month', 'day', or 'none'? ").strip().lower()

        if filter_choice == 'month':
            month = input("Enter a month (January - June) or 'all': ").strip().lower()
            if month in valid_months:
                day = 'all'
                break
            print("Invalid month. Try again.")

        elif filter_choice == 'day':
            day = input("Enter a day of the week or 'all': ").strip().lower()
            if day in valid_days:
                month = 'all'
                break
            print("Invalid day. Try again.")

        elif filter_choice == 'none':
            month = day = 'all'
            break

        else:
            print("Invalid input. Please type 'month', 'day', or 'none'.")

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Load data for the specified city and apply filters.

    Args:
        city (str): city name
        month (str): selected month or 'all'
        day (str): selected day of the week or 'all'

    Returns:
        df (DataFrame): pandas DataFrame with filtered data
    """

    df = pd.read_csv(CITY_DATA[city])



    df['start_time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['start_time'].dt.month
    df['day_name'] = df['start_time'].dt.day_name()

    if month != 'all':
        month_index = valid_months.index(month) + 1
        df = df[df['month'] == month_index]

    if day != 'all':
        df = df[df['day_name'].str.lower() == day]

    return df

def time_stats(df):
    """
    Display statistics on the most frequent times of travel.
    """
    print("\nCalculating Most Frequent Travel Times...\n")
    start = time.time()

    most_common_month = df['month'].mode()[0]
    print("Most Common Month:", valid_months[most_common_month - 1].title())

    most_common_day = df['day_name'].mode()[0]
    print("Most Common Day of Week:", most_common_day)

    df['hour'] = df['start_time'].dt.hour
    common_hour = df['hour'].mode()[0]
    suffix = 'AM' if common_hour < 12 else 'PM'
    display_hour = common_hour if common_hour <= 12 else common_hour - 12
    print(f"Most Common Start Hour: {display_hour} {suffix}")

    print(f"\nThis took {time.time() - start:.2f} seconds.")
    print('-' * 40)

def station_stats(df):
    """
    Display statistics on the most popular stations and trips.
    """
    print("\nCalculating Most Popular Stations and Trips...\n")
    start = time.time()

    start_station = df['Start Station'].mode()[0]
    print("Most Frequent Start Station:", start_station)

    end_station = df['End Station'].mode()[0]
    print("Most Frequent End Station:", end_station)

    df['trip'] = df['Start Station'] + " to " + df['End Station']
    common_trip = df['trip'].mode()[0]
    print("Most Frequent Trip:", common_trip)

    print(f"\nThis took {time.time() - start:.2f} seconds.")
    print('-' * 40)



def trip_duration_stats(df):
    """
    Display total and average trip durations.
    """
    print("\nCalculating Trip Durations...\n")
    start = time.time()

    total_duration = df['Trip Duration'].sum()
    minutes, seconds = divmod(total_duration, 60)
    hours, minutes = divmod(minutes, 60)
    print(f"Total Travel Time: {int(hours)}h {int(minutes)}m {int(seconds)}s")


    average_duration = int(df['Trip Duration'].mean())
    avg_min, avg_sec = divmod(average_duration, 60)
    if avg_min >= 60:
        avg_hr, avg_min = divmod(avg_min, 60)
        print(f"Average Travel Time: {avg_hr}h {avg_min}m {avg_sec}s")
    else:
        print(f"Average Travel Time: {avg_min}m {avg_sec}s")

    print(f"\nThis took {time.time() - start:.2f} seconds.")
    print('-' * 40)



def stats_user(df, city):
    """
    Display statistics on bikeshare users.
    """
    print("\nCalculating User Stats...\n")
    start = time.time()

    user_counts = df['User Type'].value_counts()
    print("User Types:\n", user_counts)

    #Statistics of gender.
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print("\nGender Distribution:\n", gender_counts)
    else:
        print("\nNo gender data available for", city.title())



    #Statistics of birth year.
    if 'Birth Year' in df.columns:
        earliest = int(df['Birth Year'].min())
        latest = int(df['Birth Year'].max())
        common = int(df['Birth Year'].mode()[0])
        print(f"\nEarliest Birth Year: {earliest}")
        print(f"Most Recent Birth Year: {latest}")
        print(f"Most Common Birth Year: {common}")
    else:
        print("\nNo birth year data available for", city.title())

    print(f"\nThis took {time.time() - start:.2f} seconds.")
    print('-' * 40)

def individual_data(df):
    """
    Display individual trip data if requested by The User.
    """
    index = 0
    chunk_size = 5
    total_rows = len(df)

    while index < total_rows:
        show_data = input("Would you like to see individual trip data? Y/N : ").strip().lower()
        if show_data == 'yes':
            print(df.iloc[index:index+chunk_size])
            index += chunk_size
        else:
            break
def main():
    """
    Main function to run the program .
    """
    while True:
        # Get user filters
        city, month, day = get_filters()
        print(f"\nYou Selected: {city.title()} | Month: {month.title()} | Day: {day.title()}")

        # Load filtered data
        df = load_data(city, month, day)

        # Display various statistics
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        stats_user(df, city)
        individual_data(df)

        # Ask if user wants to restart
        restart = input("\nWould you like to restart the program? Y/N : ").strip().lower()
        if restart != 'yes':
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
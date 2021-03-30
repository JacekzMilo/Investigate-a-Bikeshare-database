import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    cities = list(CITY_DATA.keys())

    city = ''

    while city not in cities:
        city = str(input("Would you like to see data for Chicago, New York City, or Washington?: ").lower())

    print('chosen city: {}'.format(city))

    months = ['All', 'January', 'February', 'March', 'April', 'May', 'June']

    month = ''

    while month not in months:
        month = str(input("Which month? January, February, March, April, May, June, All?: ").title())

    if month.lower() == 'all':
        month = range(1, len(months[1:])+1)
    else:
        month = [months.index(month)]

    days = [-1,0,1,2,3,4,5,6]

    day = ''

    while day not in days:
        day = int(input("Which day? Please type your response as an integer (e.g., Monday=0, -1 is all): "))
        print('-'*40)

    if day == -1:
        day = days[1:]
    else:
        day = [day]

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['Day_of_week'] = df['Start Time'].dt.weekday
    df['Hour'] = df['Start Time'].dt.hour

    # filter by month to create the new dataframe
    df = df.loc[df['Month'].isin(month)]

    # filter by day to create the new dataframe
    df = df.loc[df['Day_of_week'].isin(day)]

    return df
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()


    common_month = df['Month'].mode()[0]
    print('Most common month: ', common_month)

    common_day = df['Day_of_week'].mode()[0]
    print('Most common day: ', common_day)

    common_hour = df['Hour'].mode()[0]
    print('Most common hour: ', common_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    common_start_station = df['Start Station'].mode()[0]
    print('Most common start station: ', common_start_station)

    common_end_station = df['End Station'].mode()[0]
    print('Most common end station: ', common_end_station)

    common_combination_stations = df.groupby(["Start Station", "End Station"]).size().idxmax()

    print('most common combination stations', common_combination_stations)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    travel_duration = df['Trip Duration'].sum()
    print('Total travel time: ', travel_duration)

    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time: ', mean_travel_time)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_type = df['User Type'].count()
    print('Count of user types: ', user_type)


    if "Gender" not in df.columns:
        print('No info about gender ')

    else:
        gender_count = df['Gender'].value_counts()

        print('Count of males and females:\n', gender_count)

    if 'Birth Year' not in df.columns:
        print('No info about birth year ')
    else:
        earliest = df['Birth Year'].min()
        print('Earliest year of birth: ', earliest)

        most_recent = df['Birth Year'].max()
        print('Most recent year of birth: ', most_recent)

        most_common = df['Birth Year'].mode()[0]
        print('Most common year of birth: ', most_common)

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        user_input = input('\nWould you like to see more data?\nPlease enter yes or no\n').lower()
        if user_input in ('yes', 'y'):
            i = 0
            while True:
                print(df.iloc[i:i+5])
                i += 5
                more_data = input('Would you like to see more data? Please enter yes or no: ').lower()
                if more_data not in ('yes', 'y'):
                    break


        restart = input('\nWould you like to restart? Enter yes or no.\n')


        while restart.lower() != 'yes' and restart.lower() != 'no':
            restart = input('\nWould you like to restart? Enter yes or no.\n')

        if restart == 'no':
            break

if __name__ == "__main__":
	main()

import time
import pandas as pd
import numpy as np
import os

city_data = { 'chicago': 'chicago.csv',
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
    print('\nHello! Let\'s explore some US bikeshare data!\n')
    time.sleep(1)

    cities = ['chicago','new york city','washington']
    months = ['all','january','february','march','april','may','june']
    days = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']

# get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = str(input('Which city would you like to take a closer look at? \n Chicago, New York City, or Washington?\n    ')).lower()
        if city in cities:
            break
        else:
            print('Your input for month was not valid.  Please try again. \n')
            time.sleep(1)

# get user input for month (all, january, february, ... , june)
    while True:
        month = str(input('\nWhich month would you like to focus on? \n all, January, February, March, April, May, or June?\n    ')).lower()
        if month in months:
            break
        else:
            print('Your input for month was not valid.  Please try again. \n')
            time.sleep(1)

# get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = str(input('\nWhich day would you like? \n all, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n    ')).lower()
        if day in days:
            break
        else:
            print('Your input for month was not valid.  Please try again. \n')
            time.sleep(1)

    print('-'*40)
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
    df = pd.read_csv(city_data[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df.insert(2,'Month',df['Start Time'].dt.month_name())
    df.insert(3,'Day of Week',df['Start Time'].dt.weekday_name)

    if month != 'all':
        month = month.title()
        df = df[df['Month'] == month]

    if day != 'all':
        day = day.title()
        df = df[df['Day of Week'] == day]

    df.insert(4,'Hour',df['Start Time'].dt.hour)

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'all':
        com_month = df['Month'].mode()[0]
        print('    {} is the most common month for travel.\n'.format(com_month))
    else:
        print('    Since you\'ve selected {} to filter the data. It is, unsurprisingly, the most common month to start a ride in the available dataset.\n'.format(month.title()))

    # display the most common day of week
    if day == 'all':
        com_day = df['Day of Week'].mode()[0]
        print('    {} is the most common day to have a ride.\n'.format(com_day))
    else:
        print('    Since you\'ve selected {} to filter the data. It is, unsurprisingly, the most common day to have a ride in the available dataset.\n'.format(day.title()))

    # display the most common start hour
    com_hour = df['Hour'].mode()[0]
    if com_hour == 1 or com_hour == 21:
        sup_script = 'st'
    elif com_hour == 2 or com_hour == 22:
        sup_script = 'nd'
    elif com_hour == 3 or com_hour == 23:
        sup_script = 'rd'
    else:
        sup_script = 'th'

    print('    The {}{} hour of the day is the most common hour to start a trip.\n'.format(com_hour,sup_script))

    print("\nThis took %s seconds." % (time.time() - start_time))
    signal()
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    com_start_station = df['Start Station'].mode()[0]
    print('    The most common station to start a trip at is {}.\n'.format(com_start_station))

    # display most commonly used end station
    com_end_station = df['End Station'].mode()[0]
    print('    The most common station to end a trip at is {}.\n'.format(com_end_station))

    # display most frequent combination of start station and end station trip
    df['Start and Stop'] = df['Start Station'] + ',' + df['End Station']
    com_start_end_combo = df['Start and Stop'].mode()[0]
    start_loc, stop_loc = com_start_end_combo.split(',')

    print('    The most common trip is from {} to {}.'.format(start_loc,stop_loc))

    print("\nThis took %s seconds." % (time.time() - start_time))
    signal()
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    hours = int(np.sum(df['Trip Duration']) // 3600)
    minutes = int((np.sum(df['Trip Duration']) % 3600) // 60)
    seconds = round(float(np.sum(df['Trip Duration']) - np.product(hours*3600) - np.product(minutes*60)),2)

    print('\n    Total travel time during this time period was {:,} hours, {:,} minutes, and {:,} seconds.'.format(hours, minutes, seconds))

    # display mean travel time
    avg_trip = np.mean(df['Trip Duration'])

    avg_hour = int(avg_trip // 3600)
    avg_min = int((avg_trip % 3600) // 60)
    avg_sec = round(float((avg_trip % 3600) % 60),2)

    print('\n    The average trip was {} hours, {} minutes, and {} seconds.'.format(avg_hour,avg_min,avg_sec))

    # display the longest travel time
    max_trip = np.max(df['Trip Duration'])

    max_hour = int(max_trip // 3600)
    max_min = int((max_trip % 3600) // 60)
    max_sec = round(float((max_trip % 3600) % 60),2)

    print('\n    The longest trip was {} hours, {} minutes, and {} seconds.'.format(max_hour,max_min,max_sec))

    # display the shortest travel time
    min_trip = np.min(df['Trip Duration'])

    min_hour = int(min_trip // 3600)
    min_min = int((min_trip % 3600) // 60)
    min_sec = round(float((min_trip % 3600) % 60),2)

    print('\n    The shortest trip was {} hours, {} minutes, and {} seconds.'.format(min_hour,min_min,max_sec))

    print("\nThis took %s seconds." % (time.time() - start_time))
    signal()
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_count = df.groupby(['User Type'])['User Type'].count()
    print('    {:,} of users were Customers while Subscribers make up {:,} of the remaining users.\n'.format(user_count['Customer'],user_count['Subscriber']))

    # Display counts of gender
    if city == 'washington':
        print('    There is no gender data for Washington.\n')
    else:
        gender_count = df.groupby(['Gender'])['Gender'].count()

        print('    {:,} of users were Female while {:,} of users were Male.'.format(gender_count['Female'],gender_count['Male']))

    # Display earliest, most recent, and most common year of birth
    if city == 'washington':
        print('    There is no birthdate data for Washington.')
    else:
        earliest_birth = int(np.min(df['Birth Year']))
        most_recent_birth = int(np.max(df['Birth Year']))
        mode_birth = int(df['Birth Year'].mode())

        print('\n    The earliest birth year was {}.'.format(earliest_birth))
        print('\n    The most recent birth year was {}.'.format(most_recent_birth))
        print('\n    The most common birth year was {}.'.format(mode_birth))

    print("\nThis took %s seconds." % (time.time() - start_time))
    signal()
    print('-'*40)

def signal():
    """Pauses the program until the user prompts it to continue."""
    input('\nPress enter to continue.')

def main():
    while True:
        city, month, day = get_filters()

        filters = input('\nIt looks like you entered {}, {}, and {} as your city, month, and day filters.  Are these correct?  Please enter yes or no.\n    '.format(city,month,day))
        if filters != 'yes':
            print('\nThe program will be restarted now.')
            time.sleep(1)
            print('-'*40)
            continue

        df = load_data(city, month, day)

        time_stats(df, month, day)
        time.sleep(1)
        station_stats(df)
        time.sleep(1)
        trip_duration_stats(df)
        time.sleep(1)
        user_stats(df,city)

        raw_df = input('\nWould you like to see a sample of the raw data for this analysis?  Enter yes or no.\n')
        if raw_df == 'yes':
            print(df.head())

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break




if __name__ == "__main__":
	main()

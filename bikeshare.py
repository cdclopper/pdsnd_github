import time
import pandas as pd
import numpy as np

days_of_the_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

monthes = ["january", "february", "march", "april", "may", "june"]

city_data = { 'chicago': r'C:\Users\Brooke\Desktop\Udacity\Programing\Project_3\project_3_repo\pdsnd_github\chicago.csv',
              'new york': r'C:\Users\Brooke\Desktop\Udacity\Programing\Project_3\project_3_repo\pdsnd_github\new_york_city.csv',
              'washington': r'C:\Users\Brooke\Desktop\Udacity\Programing\Project_3\project_3_repo\pdsnd_github\washington.csv'
              }

def get_filters():
    """ gets the user imput """  

    print('Hi, I can share some bikeshare data with you', '\n')

    """while loop to ensure valid input for city """
    while True:
        print('For which city would you like to see data?')
        city = input("Chicago, New York, or Washington: ")
        if city.lower() == 'chicago' or city.lower() == 'new york' or city.lower() == 'washington':
            print('\n')
            break
        else:
            print("\nYou may have made a typo, please try again.")

    """while loop to ensure valid input for time_filter """
    while True:
        print("Would you like to filter the data by month, day, both or not at all?")
        time_filter = input("Type 'none' for no time filter: ")
        if time_filter.lower() == 'month' or time_filter.lower() == 'day' or time_filter.lower() == 'both' or time_filter.lower() == 'none':
            print('\n')
            break
        else:
            print("\nI couldn't understand, perhaps you made a typo. Please try again.")

    """filter to get month"""
    if time_filter.lower() == 'month' or time_filter.lower() == 'both':

        """while loop to ensure valid input for month """
        while True:
            print('Which month?')
            month = input("January, February, March, April, May or June: ")
            if month.lower() in monthes:
                print('\n')
                break
            else:
                print("\nI didn't get that, did you make a typo? Please try again.")
    else:
        month = None

    """filter to get day of week"""
    if time_filter.lower() == 'day' or time_filter.lower() == 'both':

        """while loop to ensure valid input for day variable"""
        while True:
            print('Which day?')
            day = input("Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday: ")
            if day.lower() in days_of_the_week:
                print('\n')
                break
            else:
                print("Can't compute. Maybe a typo, please try again.", '\n')
    else:
        day = None
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
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(city_data[city.lower()])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract start minute, hour, month, and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday
    df['start_hour'] = df['Start Time'].dt.hour

    # extract start station end station to create new column
    df['Start-End Station'] = df['Start Station'] + " to " + df['End Station']


    # filter by month if applicable
    if month != None:
        # use the index of the months list to get the corresponding int
        month = monthes.index(month.lower())+1
    
        # filter by month to create the new dataframe
        is_month = df['month']==month
        df = df[is_month]

    # filter by day of week if applicable
    if day != None:
        # filter by day of week to create the new dataframe
        day = days_of_the_week.index(day.lower())
        is_day = df['day_of_week']==day
        df = df[is_day]
    return df

def time_stats(df):
    """Displays statistics on the most frequen times of travel."""

    print('Calculating the most frequent times of travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = monthes[df['month'].mode()[0] - 1]
    print("The busiest month in was {}".format(popular_month.title()))

    # display most common day of week
    popular_day = days_of_the_week[df['day_of_week'].mode()[0]]
    print("The busiest day of the week was {}".format(popular_day.title()))

    # display most common start hour
    popular_hour = int(df['start_hour'].mode()[0])

    # for p.m. time

    if popular_hour > 12:
        popular_hour = popular_hour - 12
        popular_hour = str(popular_hour) + " p.m."

    # for a.m. time
    
    else:
        popular_hour = str(popular_hour) + " a.m."
    print("The busiest starting hour was {}".format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
        
def station_stats(df):
    """displays statistics on the most popular stations and trip."""

    print('\nCalculating the most popular stations and trip...\n')
    start_time = time.time()

    # displays most used start station
    
    popular_start_station = df['Start Station'].mode()[0]
    print("The most popular starting station in was {}".format(popular_start_station.title()))

    # displays most used end station

    popular_end_station = df['End Station'].mode()[0]
    print("The most popular ending station was {}".format(popular_end_station.title()))

    # displays most frequent combination of start station and end station

    popular_station_combination = df['Start-End Station'].mode()[0]
    print("The most frequent combination of start station \nand end station was {}".format(popular_station_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculation trip duration...\n')
    start_time = time.time()

    # display total travel time

    duration = df['Trip Duration'].sum()
    duration_in_hours = duration / (60*60)
    duration_in_minutes = 60 * (duration_in_hours - int(duration_in_hours))
    duration_in_seconds = 60 * (duration_in_minutes - int(duration_in_minutes))
    print("The total travel time was {} hours, {} minutes, {} seconds.".format(int(duration_in_hours), int(duration_in_minutes), int(duration_in_seconds)))

    # display mean travel time

    duration = df['Trip Duration'].mean()
    duration_in_hours = duration / (60*60)
    duration_in_minutes = 60 * (duration_in_hours - int(duration_in_hours))
    duration_in_seconds = 60 * (duration_in_minutes - int(duration_in_minutes))
    print("The average travel time was {} hours, {} minutes, {} seconds.".format(int(duration_in_hours), int(duration_in_minutes), int(duration_in_seconds)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    
    # Displays counts of user types
    print("The breakdown of users is \n{}".format(df['User Type'].value_counts()))

    # Displays counts of gender
    # Test if city is washington, no gender yob data for washington
    if city.lower() == 'washington':
        print("Sorry, no gender or birth year data for {}".format(city.title()), '\n')
    else:
        # Displays counts of gender
        print("The breakdown of genders is \n{}".format(df['Gender'].value_counts()), '\n')

        # Displays most common, earliest, and most recent user's year of birth
        print("The most common year of birth of customers is {}".format(int(df['Birth Year'].mode()[0])))
        print("The youngest customer was born in {}".format(int(df['Birth Year'].max())))

        # sorts by most recent transaction
        most_recent = df.sort_values(by=['End Time'], ascending=True)
        print("The year of birth of the most recent customer was {}.".format(int(most_recent['Birth Year'].iloc[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    answer = 'yes'
    count = 1
    while answer.lower() == 'yes':
        if count == 1:
            answer = input("\nType 'yes' if you would you like to see 5 rows of raw data: ")
        else:
            answer = input("\nType 'yes' if you would like to see another 5 rows of raw data: ")
        if answer.lower() != 'yes':
            break
        first_row = ((count-1) * 5)
        last_row = (count * 5)
        print(df.iloc[first_row:last_row])
        count = count + 1
 
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        input('Press enter to continue...')
        station_stats(df)
        input('Press enter to continue...')
        trip_duration_stats(df)
        input('Press enter to continue...')
        user_stats(df, city)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no: ')
        if restart.lower() != 'yes':
            break
if __name__ == "__main__":
    main()

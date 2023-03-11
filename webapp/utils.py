import datetime


def get_times_intervals():

    time_intervals = list()

    start_time = datetime.time(9, 0)  # Start time: 9:00 AM
    end_time = datetime.time(20, 0)  # End time: 8:00 PM

    delta = datetime.timedelta(hours=1)
    current_date = datetime.date.today()

    for day in range(3):
        current_time = datetime.datetime.combine(current_date, start_time)  # Initialize current time for the day
        while current_time.time() <= end_time:
            time_intervals.append(current_time) # Output current time
            current_time += delta  # Increment current time by the time interval
        current_date += datetime.timedelta(days=1)

    return  [{'label': t.strftime("%m/%d/%Y %I:%M %p"), 'value': t.strftime("%Y%m%dT%H%M%S")} for i, t in enumerate(time_intervals, 1)]


if __name__ == '__main__':
    print(get_times_intervals())


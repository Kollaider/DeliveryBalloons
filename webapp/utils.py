from datetime import datetime, timedelta


def get_times_intervals():
    # Set the start date and time to now
    start_time = datetime.now()

    # Set the end date to 3 days from now
    end_time = start_time + timedelta(days=3)

    # Generate time intervals every hour between start_time and end_time
    time_intervals = []
    while start_time < end_time:
        # Remove the minutes and seconds components
        start_time = start_time.replace(minute=0, second=0, microsecond=0)
        time_intervals.append(start_time)
        start_time += timedelta(hours=1)

    return  [{'label': t.strftime("%Y-%m-%d %H:%M"), 'value': i} for i, t in enumerate(time_intervals, 1)]

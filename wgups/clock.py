from configparser import ConfigParser


class Clock:

    def __init__(self, time, start_of_day):
        """
        Create a clock object set at a particular time
        :param time: time representing number of seconds since start time :int
        """

        self._time = time
        self._start_time = self.parse_time_string(start_of_day)

    @property
    def time(self):
        """
        :return: value of _time (number of seconds since start time)

        Wost Case runtime complexity: O(1)
        Best Case runtime complexity: O(1)
        """
        return self._time

    @property
    def start_time(self):
        """
        Returns start_time in string format: HH:MM AM/PM

        :return: start time in string format

        Worst Case runtime complexity: O(1)
        Best Case runtime complexity: O(1)
        """
        result = ""
        hour = self._start_time[0]
        minute = self._start_time[1]
        am_pm = "AM"
        if hour > 12:
            am_pm = "PM"
            hour -= 12
        minute_str = str(minute)
        if len(minute_str) == 1:
            minute_str = "0" + minute_str
        return f"{hour}:{minute_str} {am_pm}"

    def forward_seconds(self, seconds):
        """
        Move clock forward by given number of seconds
        :param seconds: number of seconds to move clock forward
        :return: none

        Worst Case Runtime Complexity: O(1)
        Best Case Runtime Complexity: O(1)
        """
        self._time += seconds

    def forward_minutes(self, minutes):
        """
        Move clock forward by given number of minutes
        :param minutes: number of minutes to move clock forward
        :return: none

        Worst Case runtime complexity: O(1)
        Best Case runtime complexity: O(1)
        """
        self._time += minutes * 60

    def forward_hours(self, hours):
        """
        Move clock forward by given number of hours
        :param hours: number of hours to move the clock forward
        :return: none

        Worst Case Runtime Complexity: O(1)
        Best Case Runtime Complexity: O(1)
        """
        self._time += hours * 60 * 60

    def forward_time(self, hours, minutes, seconds):
        """
        Move clock forward by given numbers of hours, minutes, and seconds
        :param hours: number of hours to move clock forward
        :param minutes: number of minutes to move clock forward
        :param seconds: number of seconds to move clock forward
        :return: none

        Worst Case Runtime Complexity: O(1)
        Best Case Runtime Complexity: O(1)
        """
        self.forward_hours(hours)
        self.forward_minutes(minutes)
        self.forward_seconds(seconds)

    @staticmethod
    def to_time_string(time, start_of_day):
        """
        Converts _time to string format: HH:MM AM/PM
        :return: current time in string format

        Worst Case Runtime Complexity: O(1)
        Best Case Runtime Complexity: O(1)
        """
        # current time in number of seconds since start time
        seconds_left = time

        # divide seconds left by number of seconds in an hour
        hours, seconds_left = divmod(seconds_left, 60 * 60)

        # divide seconds left by number of seconds in a minute
        minutes, seconds_left = divmod(seconds_left, 60)

        start_time = Clock.parse_time_string(start_of_day)

        # Calculate current hour and minute
        hours = start_time[0] + hours
        minutes = start_time[1] + minutes

        # If minutes is greater or equal to 60, increment hours and subtract minutes
        # by number of minutes in an hour
        if minutes >= 60:
            hours += 1
            minutes -= 60
        am_pm = "AM"

        # If minutes is only one digit, add a leading zero
        minutes_str = str(minutes)
        if len(minutes_str) == 1:
            minutes_str = "0" + minutes_str

        # If hours is greater than 12, then am_pm becomes "PM" and hours subtracted by 12
        if hours > 12:
            am_pm = "PM"
            hours -= 12

        # return time in string format
        return f"{hours}:{minutes_str} {am_pm}"

    @staticmethod
    def parse_time_string(time):
        """
        Convert time string to a tuple of format: (HH, MM)
        :param time: String representing a time in format: HH:MM AM/PM
        :return: tuple representation of time: (HH, MM)

        Worst Case Runtime Complexity: O(1)
        Best Case Runtime Complexity: O(1)
        """

        # strip any leading or trailing spaces
        time.strip()

        # hour is substring from beginning of string to first occurrence of ':'
        hour = int(time[:time.index(":")])

        # minute is substring from first occurrence of ':' to second occurrence of a space
        minute = int(time[time.index(":") + 1:time.index(" ")])

        # AM/PM is substring from first occurrence of space to end of string
        am_pm = time[time.index(" ") + 1:]

        # if am_pm is "PM" add 12 hours to hour
        if am_pm.lower() == "pm":
            hour += 12

        # return tuple representing hour and minute
        return hour, minute

    @staticmethod
    def seconds_since_start(time, start_time):
        """
        Convert time string to number of seconds since start time
        :param time: time string in format: HH:MM AM/PM to be converted
        :param start_time: the method counts the number of seconds from this time
        :return: number of seconds since start time
        """

        # initialize num_seconds to zero
        num_seconds = 0

        # convert start_time to hour, minute tuple
        start_time = Clock.parse_time_string(start_time)

        # convert current time to hour, minute tuple
        time = Clock.parse_time_string(time)

        # Calculate number of seconds since start
        num_seconds += (time[0] - start_time[0]) * 60 * 60
        num_seconds += (time[1] - start_time[1]) * 60

        # return number of seconds since start
        return num_seconds

    def __str__(self):
        """
        Returns a string representation of the object
        :return: string representation of the object

        Worst Case Runtime Complexity: O(1)
        Best Case Runtime Complexity: O(1)
        """
        return self.to_time_string()



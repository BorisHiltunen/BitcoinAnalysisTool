"""time_engine.py: Contains four helper functions."""

from datetime import datetime, timezone


class TimeForm:
    """
    Class that is in charge of the application's helper functions
    That focus on the time.
    """

    def get_timestamps_from_input(self, dates: str):
        """Helper function that returns tuple containing two timestamps."""

        string_to_date1 = datetime.fromisoformat(dates[:10])
        string_to_date2 = datetime.fromisoformat(dates[11:])

        utc_time1 = string_to_date1.replace(tzinfo=timezone.utc)
        utc_time2 = string_to_date2.replace(tzinfo=timezone.utc)

        utc_timestamp1 = utc_time1.timestamp()
        utc_timestamp2 = utc_time2.timestamp()

        return (utc_timestamp1, utc_timestamp2)

    def get_date_from_timestamp(self, timestamp):
        """Helper function that converts timestamp into a date."""

        date = datetime.fromtimestamp(timestamp / 1e3)
        return date

    def get_date_from_input(self, dates: str):
        """Helper function that converts input to datetime."""

        string_to_date1 = datetime.fromisoformat(dates[:10])
        string_to_date2 = datetime.fromisoformat(dates[11:])

        return (string_to_date1, string_to_date2)

    def datetime_object_from_timestamp(self, timestamp):
        """Helper function that converts timestamp into a datetime_object."""

        compare_date = self.get_date_from_timestamp(
            timestamp).strftime("%Y-%m-%d, %H:%M:%S")
        year = compare_date[:4]
        month = compare_date[5:7]
        day = compare_date[8:10]

        datetime_object = datetime(int(year), int(month), int(day))

        return datetime_object

"""timestamp_engine.py: Contains two helper function."""

from datetime import datetime, timezone


class TimeForm:
    """
    Class that is in charge of the application's helper functions.
    That focus on the time.
    """

    def get_timestamps_from_input(self, dates: str):
        """Helper function that returns tuple containing two timestamps."""

        count = 0

        year1 = ""
        month1 = ""
        day1 = ""

        year2 = ""
        month2 = ""
        day2 = ""

        while count < len(dates):
            if (count == 2 or count == 5 or count == 10
                    or count == 13 or count == 16):
                count += 1
                continue
            else:
                if count < 2:
                    day1 += dates[count]
                elif count < 5:
                    month1 += dates[count]
                elif count < 11:
                    year1 += dates[count]
                elif count < 13:
                    day2 += dates[count]
                elif count < 16:
                    month2 += dates[count]
                elif count < 21:
                    year2 += dates[count]
            count += 1

        date1_in_correct_form = f"{year1}-{month1}-{day1}"
        date2_in_correct_form = f"{year2}-{month2}-{day2}"

        string_to_date1 = datetime.fromisoformat(date1_in_correct_form)
        string_to_date2 = datetime.fromisoformat(date2_in_correct_form)

        utc_time1 = string_to_date1.replace(tzinfo=timezone.utc)
        utc_time2 = string_to_date2.replace(tzinfo=timezone.utc)

        utc_timestamp1 = utc_time1.timestamp()
        utc_timestamp2 = utc_time2.timestamp()

        return (utc_timestamp1, utc_timestamp2)

    def get_date_from_timestamp(self, timestamp):
        """Helper function that converts timestamp into a date."""

        date = datetime.utcfromtimestamp(timestamp).strftime(
            '%Y-%m-%d %H:%M:%S')
        return date

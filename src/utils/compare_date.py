from datetime import datetime

def geq(date_str1: str, date_str2: str, date_format: str = '%Y-%m-%d') -> bool:
    """
    Test if date_str1 >= date_str2.

    Parameters
    ----------
    date_str1 : str
        The first date string to compare.
    date_str2 : str
        The second date string to compare.
    date_format : str, optional
        The format of the date strings. Default is '%Y-%m-%d'.

    Returns
    -------
    bool
        True if date1 is greater than or equal to date2, False otherwise.
    """
    date1 = datetime.strptime(date_str1, date_format)
    date2 = datetime.strptime(date_str2, date_format)

    return date1 >= date2

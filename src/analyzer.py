from collections import defaultdict
from typing import List, Tuple

def count_cookies_on_target_date(cookie_records: List[Tuple[str, str]], target_date: str) -> dict[str, int]:
    """ 
        This function counts how many times each cookie appears on the target date.
        
        Args:
            cookie_records: This is list of (cookie, date_string) tuples
            target_date: This is a date string in the YYYY-MM-DD format
        
        Returns:
            A dictionary which maps each cookie string to its occurrence count on the target date
    """
    counts: dict[str, int] = defaultdict(int)

    for cookie, date in cookie_records:
        if date == target_date:
            counts[cookie] += 1
        elif date < target_date:
            # Since the file is sorted descending, once we go
            # below our target date, there's nothing left to find
            break
    return counts

def find_most_active_cookies(counts: dict[str, int]) -> List[str]:
    """ 
        This function identifies the most active cookie(s) from a frequency count.

        If multiple cookies share the highest count, all of them are returned.
        This handles ties as required by the problem specification.
        
        Args:
            counts: This is a dictionary of cookie -> count
        
        Returns:
            A list of most active cookie(s) or an Empty list if no cookies are found.
    """
    if not counts:
        return []

    max_count = max(counts.values())
    return [cookie for cookie, count in counts.items() if count == max_count]
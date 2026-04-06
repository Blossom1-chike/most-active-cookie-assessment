from src.analyzer import count_cookies_on_target_date, find_most_active_cookies

"""
    Unit tests for the analyzer module (count_cookies_on_target_date, find_most_active_cookies).
    
    Each test is fully independent — data is defined locally per test,
    never shared via module-level state. This ensures tests can run in
    any order and produce consistent results.
    
    Naming convention: test_<function>_<scenario>
    Long descriptive names are intentional — they serve as documentation
    and make failures immediately understandable without reading the body.
"""

class TestCountCookies:

    def test_count_cookies_returns_correct_count_for_cookie_appearing_multiple_times(self):
        """
        A cookie appearing more than once on the target date should have
        its count reflect the exact number of appearances.
        """
        records = [
            ("AtY0laUfhglK3lC7", "2018-12-09"),
            ("AtY0laUfhglK3lC7", "2018-12-09"),  # appears twice
        ]

        counts = count_cookies_on_target_date(records, "2018-12-09")

        assert counts["AtY0laUfhglK3lC7"] == 2

    def test_count_cookies_returns_count_of_one_for_cookie_appearing_once(self):
        """
        A cookie appearing exactly once on the target date should
        have a count of 1.
        """
        records = [("SAZuXPGUrfbcn5UA", "2018-12-09")]

        counts = count_cookies_on_target_date(records, "2018-12-09")

        assert counts["SAZuXPGUrfbcn5UA"] == 1

    def test_count_cookies_excludes_cookies_that_appear_only_on_other_dates(self):
        """
        Cookies that appear exclusively on dates other than the target
        must not appear in the result at all.
        """
        records = [
            ("AtY0laUfhglK3lC7", "2018-12-09"),
            ("4sMM2LxV07bPJzwf", "2018-12-08"),  # a different date
        ]

        counts = count_cookies_on_target_date(records, "2018-12-09")

        assert "4sMM2LxV07bPJzwf" not in counts

    def test_count_cookies_returns_empty_dict_when_no_records_match_target_date(self):
        """
        When no records exist for the target date, the result should be
        an empty dictionary — not an error.
        """
        records = [
            ("AtY0laUfhglK3lC7", "2018-12-09"),
            ("SAZuXPGUrfbcn5UA", "2018-12-08"),
        ]

        counts = count_cookies_on_target_date(records, "2018-12-01")

        assert counts == {}

    def test_count_cookies_returns_empty_dict_for_empty_record_list(self):
        """
        An empty record list is valid input and should return an empty
        dictionary without raising an error.
        """
        counts = count_cookies_on_target_date([], "2018-12-09")

        assert counts == {}

    def test_count_cookies_counts_multiple_distinct_cookies_on_same_date(self):
        """
        When multiple different cookies appear on the target date,
        each should be counted independently and correctly.
        """
        records = [
            ("AtY0laUfhglK3lC7", "2018-12-09"),
            ("SAZuXPGUrfbcn5UA", "2018-12-09"),
            ("5UAVanZf6UtGyKVS", "2018-12-09"),
            ("AtY0laUfhglK3lC7", "2018-12-09"),
        ]

        counts = count_cookies_on_target_date(records, "2018-12-09")

        assert counts["AtY0laUfhglK3lC7"] == 2
        assert counts["SAZuXPGUrfbcn5UA"] == 1
        assert counts["5UAVanZf6UtGyKVS"] == 1

    def test_count_cookies_ignores_records_from_dates_before_and_after_target(self):
        """
        Records from both earlier and later dates than the target
        must be excluded from the result.
        """
        records = [
            ("cookie_future", "2018-12-10"),   # after target
            ("cookie_target", "2018-12-09"),   # on target
            ("cookie_past",   "2018-12-08"),   # before target
        ]

        counts = count_cookies_on_target_date(records, "2018-12-09")

        assert "cookie_target" in counts
        assert "cookie_future" not in counts
        assert "cookie_past" not in counts

class TestFindMostActive:

    def test_find_most_active_cookies_returns_single_cookie_when_one_has_highest_count(self):
        """
        When exactly one cookie has a higher count than all others,
        only that cookie should be returned.
        """
        counts = {"AtY0laUfhglK3lC7": 2, "SAZuXPGUrfbcn5UA": 1, "5UAVanZf6UtGyKVS": 1}

        result = find_most_active_cookies(counts)

        assert result == ["AtY0laUfhglK3lC7"]

    def test_find_most_active_cookies_returns_all_cookies_when_two_are_tied(self):
        """
        When two cookies share the highest count, both must be returned.
        Order is not guaranteed, so we compare as sets.
        """
        counts = {"cookie_a": 3, "cookie_b": 3, "cookie_c": 1}

        result = find_most_active_cookies(counts)

        assert set(result) == {"cookie_a", "cookie_b"}

    def test_find_most_active_cookies_returns_all_cookies_when_all_are_tied(self):
        """
        When every cookie in the dict shares the same count,
        all of them should be returned.
        """
        counts = {"cookie_a": 2, "cookie_b": 2, "cookie_c": 2}

        result = find_most_active_cookies(counts)

        assert set(result) == {"cookie_a", "cookie_b", "cookie_c"}

    def test_find_most_active_cookies_returns_empty_list_for_empty_input(self):
        """
        An empty counts dictionary should return an empty list,
        not raise an exception. This is the expected behaviour when
        no cookies exist for a given date.
        """
        result = find_most_active_cookies({})

        assert result == []

    def test_find_most_active_cookies_returns_only_cookie_when_one_exists(self):
        """
        A dictionary with a single cookie should always return that
        cookie as the most active, regardless of its count.
        """
        counts = {"only_cookie": 5}

        result = find_most_active_cookies(counts)

        assert result == ["only_cookie"]

    def test_find_most_active_cookies_does_not_return_cookies_below_max_count(self):
        """
        Cookies with counts lower than the maximum must never appear
        in the result, even if their counts are close to the max.
        """
        counts = {"winner": 4, "close_second": 3, "low": 1}

        result = find_most_active_cookies(counts)

        assert "close_second" not in result
        assert "low" not in result
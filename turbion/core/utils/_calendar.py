# -*- coding: utf-8 -*-
from datetime import date, datetime
from django.utils.dates import MONTHS

class YearIter(object):
    def __init__(self, current):
        self.current = current

    def get_next_month(self):
        if self.current.month + 1 > 12:
            return date(year=self.current.year + 1, month=1, day=1)
        return date(year=self.current.year, month=self.current.month + 1, day=1)
    next_month = property(get_next_month)

    def get_prev_month(self):
        if self.current.month - 1 <= 0:
            return date(year=self.current.year - 1, month=12, day=1)
        return date(year=self.current.year, month=self.current.month - 1, day=1)
    prev_month = property(get_prev_month)

    def get_month_name(self):
        return MONTHS[self.current.month]
    month_name = property(get_month_name)

    def get_prev_month_name(self):
        return MONTHS[self.prev_month.month]
    prev_month_name = property(get_prev_month_name)

    def get_next_month_name(self):
        return MONTHS[self.next_month.month]
    next_month_name = property(get_next_month_name)

class Calendar(object):
    def __init__(self, current=None, queryset=None):
        self.queryset = queryset is None and self.__class__.queryset or queryset
        self.current = current and current or date.today()

    def _set_current(self, current):
        self._current = current
        self.year_iter = YearIter(current)
    current = property(lambda self: self._current, _set_current)

    def get_prev_month_url(self):
        return self.get_month_url(self.year_iter.get_prev_month())

    def get_next_month_url(self):
        return self.get_month_url(self.year_iter.get_next_month())

    def get_month_url(self, date):
        raise NotImplementedError

    def get_per_day_urls(self, date):
        raise NotImplementedError

    def _get_dates(self):
        filter = {
            "%s__year" % self.date_field: self.current.year,
            "%s__month" % self.date_field: self.current.month
        }

        self._dates = self.queryset.filter(**filter).dates(self.date_field, 'day')

        return self._dates
    dates = property(_get_dates)

    def weekdays(self):
        from django.utils.dates import WEEKDAYS
        return WEEKDAYS.values()

    def __iter__(self):
        try:
            from calendar import Calendar
        except (ImportError, AttributeError):
            from turbion.core.utils.calendar24 import Calendar

        cal = Calendar()

        urls = self.get_per_day_urls(self.dates)

        for week in cal.monthdatescalendar(self.current.year, self.current.month):#FIXME: monthdates2calendar
            yield [(day.day, urls.get(day, None), day.month == self.current.month) for day in week]

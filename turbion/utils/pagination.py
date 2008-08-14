# -*- coding: utf-8 -*-
from django.core.paginator import QuerySetPaginator, Page, InvalidPage
from django import http

def split_page_number(number, per_page, page_count=None):
    number = _convert_page_number(number, page_count)

    offset = (number - 1) * per_page
    right_offset = number * per_page

    if page_count:
        max_count = page_count * per_page
        count = right_offset > max_count and max_count - offset or per_page
    else:
        count = per_page

    return offset, count

def paginate(data_set, number, per_page):
    paginator = QuerySetPaginator(data_set, int(per_page))

    if number == 'last':
        number = paginator.num_pages
    try:
        page_objects = paginator.page(number)
    except InvalidPage, e:
        raise http.Http404, "Invalid page number %s" % number

    return page_objects

def split_domains(current, total, head_num=2, tail_num=1, left_num=1, right_num=2):
    """
        >>> split_domains(1, 10, 2, 1, 1, 2)
        ([1, 2, 3], [], [10])

        >>> split_domains(2, 10, 2, 1, 1, 2)
        ([1, 2, 3, 4], [], [10])

        >>> split_domains(3, 10, 2, 1, 1, 2)
        ([1, 2, 3, 4, 5], [], [10])

        >>> split_domains(5, 10, 2, 1, 1, 2)
        ([1, 2], [4, 5, 6, 7], [10])

        >>> split_domains(7, 10, 2, 1, 1, 2)
        ([1, 2], [], [6, 7, 8, 9, 10])

        >>> split_domains(8, 10, 2, 1, 1, 2)
        ([1, 2], [], [7, 8, 9, 10])

        >>> split_domains(9, 10, 2, 1, 1, 2)
        ([1, 2], [], [8, 9, 10])

        >>> split_domains(10, 10)
        ([1, 2], [], [9, 10])
    """
    head = []
    tail = []
    center = []

    total_1 = total + 1

    if (current <= head_num) or (current - left_num <= head_num):
        head = range(1, max(current + right_num, head_num) + 1)
        tail = range(total_1 - tail_num, total_1)
    elif (current >= total - tail_num) or (current + right_num >= total - tail_num):
        head = range(1, head_num + 1)
        tail = range(min(current - left_num, total_1 - right_num), total_1)
    else:
        tail = range(total_1 - tail_num, total_1)
        head = range(1, head_num + 1)

        center = range(current - left_num, current + right_num + 1)

    return head, center, tail

if __name__ == "__main__":
    import doctest
    doctest.testmod()

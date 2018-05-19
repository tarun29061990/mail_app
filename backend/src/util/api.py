from common.exception import InvalidValueException
from enum import Enum

valid_order_by_values = ["asc", "desc"]


class ApiFiltersOperatorEnum(Enum):
    OR = "OR"
    AND = "AND"


class ApiFilters(object):
    def __init__(self, filter_str):
        self.filters = {}
        self.operators = {}
        self.keys = []
        if not filter_str:
            return
        segments = filter_str.split(";")
        for segment in segments:
            segment = segment.strip()
            if not segment:
                continue
            parts = segment.split(":", 1)
            if len(parts) < 2:
                raise InvalidValueException("Invalid filters format")
            key = parts[0]
            values = parts[1]
            if not key:
                raise InvalidValueException("Invalid filters format")
            if not values:
                continue
            if "," in values:
                self.operators[key] = ApiFiltersOperatorEnum.OR.value
                self.filters[key] = [value.strip() for value in values.split(",")]
            elif "$" in values:
                self.operators[key] = ApiFiltersOperatorEnum.AND.value
                self.filters[key] = [value.strip() for value in values.split("$")]
            else:
                self.operators[key] = ApiFiltersOperatorEnum.OR.value
                self.filters[key] = [value.strip() for value in values.split(",")]
            self.keys.append(key)

    def get(self, key, default=None):
        if key in self.filters:
            return self.filters[key][0]
        else:
            return default

    def get_list(self, key, default=None):
        if key in self.filters:
            return self.filters[key]
        else:
            return default

    def operator(self, key, default=None):
        if key in self.operators:
            return self.operators[key]
        else:
            return default

    def get_all(self, key, default=None):
        if key in self.filters:
            return self.filters[key]
        else:
            return default

    def has(self, key):
        return key in self.filters

    def get_all_keys(self):
        return self.keys


class ApiOrderBy(object):
    def __init__(self, order_by_str):
        self.order_by = {}
        self.keys = []
        if not order_by_str:
            return
        segments = order_by_str.split(";")
        for segment in segments:
            segment = segment.strip()
            if not segment:
                continue
            parts = segment.split(":", 1)
            if len(parts) < 2:
                raise InvalidValueException("Invalid orderby format")
            key = parts[0]
            value = parts[1]
            if not key:
                raise InvalidValueException("Invalid orderby format")
            if not value:
                continue
            elif valid_order_by_values.index(value) >= 0:
                self.order_by[key] = value
                self.keys.append(key)

    def get(self, key):
        if key in self.order_by:
            return self.order_by[key]

    def has(self, key):
        return key in self.order_by

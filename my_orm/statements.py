class Insert:
    def __init__(self, table_name, *columns):
        self.__query = f"INSERT INTO {table_name}"
        if columns:
            _columns = "("
            for c in columns:
                _columns += f"{c}, "
            _columns = _columns[:-2] + ')'
            self.__query += f" {_columns}"
        self.__query += f" VALUES"
        self.__columns = columns

    def values(self, *values, bulk=False):
        if bulk is False:
            _values = "("
            for v in values:
                if isinstance(v, str):
                    _values += f"'{v}', "
                else:
                    _values += f"{v}, "
            _values = _values[:-2] + ')'
        else:
            _values = ""
            for vals in values:
                _val = "("
                for v in vals:
                    if isinstance(v, str):
                        _val += f"'{v}', "
                    else:
                        _val += f"{v}, "
                _val = _val[:-2] + ')'
                _values += _val + ','
            _values = _values[:-1]
        self.__query += f" {_values} "
        return self

    def returning(self, pk_field):
        self.__query += f"RETURNING {pk_field} "
        return self

    @property
    def query(self):
        return self.__query + ";"


class Update:
    def __init__(self, table_name):
        self.__query = f"UPDATE {table_name} "

    def where(self, **kwargs):
        conditions = ""
        for k, v in kwargs.items():
            if isinstance(v, str):
                conditions += f"{k}='{v}' AND "
            else:
                conditions += f"{k}={v} AND "
        conditions = conditions[:-5]
        self.__query += f"WHERE {conditions} "
        return self

    def set(self, **kwargs):
        _set = ""
        for k, v in kwargs.items():
            if isinstance(v, str):
                _set += f"{k}='{v}', "
            else:
                _set += f"{k}={v}, "
        _set = _set[:-2]
        self.__query += f"SET {_set} "
        return self

    @property
    def query(self):
        return self.__query + ";"


class Select:
    def __init__(self, table_name, *args):
        if args:
            _args = "("
            for a in args:
                _args += f"{a}, "
            _args = _args[:-2] + ")"
        else:
            _args = "*"

        self.__query = f"SELECT {_args} FROM {table_name} "

    def where(self, **kwargs):
        conditions = ""
        for k, v in kwargs.items():
            if isinstance(v, str):
                conditions += f"{k}='{v}' AND "
            else:
                conditions += f"{k}={v} AND "
        conditions = conditions[:-5]
        self.__query += f"WHERE {conditions} "
        return self

    def join(self):
        pass

    def order_by(self, fields):
        _rule = ""
        for f in fields:
            _rule += f"{f}, "
        _rule = _rule[:-2]
        self.__query += f"ORDER BY {_rule} "
        return self

    def limit(self, limit: int):
        self.__query += f"LIMIT {limit} "
        return self

    def offset(self, offset: int):
        self.__query += f"OFFSET {offset} "
        return self

    @property
    def query(self):
        return self.__query + ";"


class Delete:
    def __init__(self, table_name):
        self.__query = f"DELETE FROM {table_name} "

    def where(self, **kwargs):
        conditions = ""
        for k, v in kwargs.items():
            if isinstance(v, str):
                conditions += f"{k}='{v}' AND "
            else:
                conditions += f"{k}={v} AND "
        conditions = conditions[:-5]
        self.__query += f"WHERE {conditions} "
        return self

    def returning(self, pk_field):
        self.__query += f"RETURNING {pk_field} "
        return self

    @property
    def query(self):
        return self.__query + ";"

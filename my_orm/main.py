from my_orm.statements import Insert, Delete, Update, Select


def select(table_name, *args, _limit=10, _offset=0, _order_by: tuple | list = None, **kwargs):
    query = Select(table_name, *args)
    if kwargs:
        query.where(**kwargs)
    if _order_by is not None:
        query.order_by(_order_by)

    query.limit(_limit)
    query.offset(_offset)
    return query


def insert(table_name, fields: tuple | list, *values, pk_field=None):
    query = Insert(table_name, *fields)
    bulk = False
    if values and (isinstance(values[0], tuple) or isinstance(values, list)):
        bulk = True
    query.values(*values, bulk=bulk)
    if pk_field is not None:
        query.returning(pk_field)
    return query


def update(table_name, _set: dict, where: dict = None):
    query = Update(table_name)
    query.set(**_set)
    if where:
        query.where(**where)
    return query


def delete(table_name, pk_field=None, **kwargs):
    query = Delete(table_name)
    if kwargs:
        query.where(**kwargs)

    if pk_field is not None:
        query.returning(pk_field)
    return query

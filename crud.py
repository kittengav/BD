from database import get_connection
from my_orm.main import *


async def select_objects(table_name, *args, _limit=10, _offset=0,
                         _order_by=None, **kwargs):
    query = select(table_name, *args, _limit=_limit,
                   _offset=_offset, _order_by=_order_by,
                   **kwargs)
    print(query.query)
    conn = await get_connection()
    result = await conn.fetch(query.query)
    await conn.close()
    return result


async def insert_objects(table_name, fields, *args, pk_field=None):
    query = insert(table_name, fields, *args, pk_field=pk_field)
    print(query.query)
    conn = await get_connection()
    result = await conn.fetch(query.query)
    await conn.close()
    return result


async def update_objects(table_name, _set: dict, where: dict = None):
    query = update(table_name, _set, where)
    print(query.query)
    conn = await get_connection()
    result = await conn.execute(query.query)
    await conn.close()
    return result


async def delete_objects(table_name, pk_field=None, **kwargs):
    query = delete(table_name, pk_field=pk_field, **kwargs)
    print(query.query)
    conn = await get_connection()
    result = await conn.fetch(query.query)
    await conn.close()
    return result

# asyncio.run(insert_objects("animal_types", ("name", "description"),
#                            ("Рысь", "Крадется"),
#                            ("Мышь", "Грызет"),
#                            ("Жираф", "Высокий"),
#                            ("Пантера", "черная"),
#                            ("Слон", "Насрал"),
#                            ("Пингвин", "скользит"),
#                            ("Панда", "упала"),
#                            ("Попугай", "пикабу"),
#                            ("Змея", "шипит"),
#                            ("Тарантул", "АААААА блЯДЬ"),
#                            ("Бегемот", "любит больших"),
#                            ("Крокодил", "пусть бегут неуклюже...")
#                            )
#             )

# asyncio.run(select_objects("animal_types", id=6))

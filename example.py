from apps.sqliteobject import SQLiteObject

sql_obj = SQLiteObject()

tablename = 'selenium'
columns = ['field_1', 'field_2', 'field_3']
values = ['value_1', 'value_2', 'value_3']

sql_obj.create_table(tablename, columns)
sql_obj.insert_data(tablename, dict(zip(columns, values)))
sql_obj.update_data(tablename, {'field_1': '1'}, {'field_2': '666'})

print("Tables:", sql_obj.show_tables())
print("Values:", sql_obj.select_data(tablename))
print("Columns:", sql_obj.show_columns(tablename))

sql_obj.delete_data(tablename)
sql_obj.drop_table(tablename)

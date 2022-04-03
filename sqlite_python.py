import sqlite3


class DataBase:
    @staticmethod
    def connect_data_base(data_base_name):
        """
        the one function of this method is return the connection with database;
        :param data_base_name: Name of database that will be connected."""
        """
        :param connect: Object that will contain the connection.
        """
        connect = sqlite3.connect(f'{data_base_name}' '.db')
        return connect

    @staticmethod
    def formatted_list_values(list_values):
        """
        Get the values in list format and creates the same values in string format adding \t\t in the starts each
        values;
        :param list_values: List of values.
        """
        """
        :param tab_values: does iteration for each value in list of values and adding, in the starts, whitespace.
        :param formatted_values: uses join method to concatenate all values in a one string of values formatted.
        """
        tab_values = ['\t\t' + value for value in list_values]
        formatted_values = ', \n'.join(tab_values)
        return formatted_values

    @staticmethod
    def format_value(_value):
        if isinstance(_value, str):
            _new_info = f"'{_value}'"
        else:
            _new_info = str(_value)
        return _new_info

    def __init__(self, data_base_name):
        """
        Creates a local copy of data_base_name
        :param self._data_base_name: Local copy of required variable of the class.
        """
        self._data_base_name = data_base_name

    def __delitem__(self, table_name, param_search, key):
        """Delete some item in table;
        :param table_name: Name of table;
        :param param_search: Parameter that will be used to search item;
        :param key: Item to delete.
        """
        with self.connect_data_base(self._data_base_name) as connect:
            cursor = connect.cursor()
            cursor.execute(f'DELETE FROM {table_name} WHERE {param_search} = ?', (key,))
            connect.commit()

    def create_table(self, table_name, list_vars):
        """
        Responsible for creating a table;
        :param table_name: Name of table;
        :param list_vars: List of the columns of table;
       """
        with self.connect_data_base(self._data_base_name) as connect:
            """
            Connects to the database and defines the header of command and joins it in a one string that will be 
            execute.
            :param table_header: defines the header of command.
            :param table_vars: get a result of formatted_list_values(list_vars);
            :param command: concatenates the components of the command.
            cursor.execute(command): sends the full command to sqlite.
            """
            cursor = connect.cursor()
            table_header = f"""CREATE TABLE IF NOT EXISTS {table_name}(\n"""
            table_vars = self.formatted_list_values(list_vars)
            command = table_header + table_vars + '\n);'
            cursor.execute(command)

    def load_tables_names(self):
        """This function will load the table names in database"""
        with self.connect_data_base(self._data_base_name) as connect:
            cursor = connect.cursor()
            cursor.execute("""
            SELECT name FROM sqlite_master WHere type='table' ORDER BY name
            """)
            """
            return: for each tuple in cursor.fetchall(), for each value in this tuple, add this value in a list
            and returns the list
            example: ['example1', 'example2', ...].
            """
            return [table for table_tuple in cursor.fetchall() for table in table_tuple]

    def table_columns(self, table_names):
        """
        The function will be return a list of columns in some table;
        :param table_names: List of table names |this instance need be a list|.
        """
        table_columns = []
        with self.connect_data_base(self._data_base_name) as connect:
            cursor = connect.cursor()
            for name in table_names:
                cursor.execute(f"""
                PRAGMA table_info({name})
                """)
                columns = [column[1] for column in cursor.fetchall()]
                table_columns.append((name, columns))
            return table_columns

    def read_table(self, table_name):
        """
        Read the table values;
        :param table_name: Name of table that will be read.
        """
        """
        at the beginning it will check to see if the value of table_name is in the database in the database.
        """
        if table_name not in self.load_tables_names():
            return 0
        with self.connect_data_base(self._data_base_name)as connect:
            cursor = connect.cursor()
            cursor.execute(f"""
            SELECT * FROM {table_name}
            """)
            lines = [line for line in cursor.fetchall()]
            return lines

    def insert_data(self, table_name, data):
        """
        The function will insert information in the table;
        :param table_name: Name of the table that will be used;
        :param data: Information that will be passed to table (need be a list).
        """
        if table_name not in self.load_tables_names():
            return 0
        with self.connect_data_base(self._data_base_name)as connect:
            cursor = connect.cursor()
            items = self.table_columns([table_name])
            for item in items:
                name, columns = item
                formatted_columns = ', '.join(columns)
            if len(data) != len(columns):
                raise f'Past information does not match the required information!'
            else:
                new_data = []
                for info in data:
                    formatted_info = self.format_value(info)
                    new_data.append(formatted_info)
                values = ', '.join(new_data)
                cursor.execute(f"""
                                INSERT INTO {table_name} ({formatted_columns})
                                VALUES ({values})
                                """)
                connect.commit()

    def add_colum(self, table_name, column):
        """
        Add a column in a some table;
        :param table_name: Name of table that be used;
        :param column: Name of column and your type.
        """
        if table_name not in self.load_tables_names():
            return None
        with self.connect_data_base(self._data_base_name) as connect:
            cursor = connect.cursor()
            cursor.execute(f"""
            ALTER TABLE {table_name}
            ADD COLUMN {column};
            """)
            connect.commit()

    def locator(self, table_name, id_search, info):
        """
        This function is a locator that will search some id in table for desired information;
        :param table_name: Table name;
        :param id_search: id to be used to search in table for one information
        :param info: information to find;
        :return: Return a line that correspond to the information passed.
        """
        with self.connect_data_base(self._data_base_name) as connect:
            cursor = connect.cursor()
            cursor.execute(f'SELECT * FROM {table_name} WHERE {id_search} = ?', (info,))
            return cursor.fetchone()

    def update_value(self, table_name, name_id, search_id, column, value):
        """
        This function will update some value in a some table;
        :param table_name: Name of table that will be updated;
        :param name_id: Columns to search;
        :param search_id: Value to be used to find item into column passed;
        :param column: Columns to be used for update value;
        :param value: value to update in the desired column;
        """
        with self.connect_data_base(self._data_base_name) as connect:
            cursor = connect.cursor()
            if table_name not in self.load_tables_names():
                return None
            cursor.execute(f'UPDATE {table_name} SET {column} = {self.format_value(value)} '
                           f'WHERE {name_id} = ?', (search_id,))
            connect.commit()

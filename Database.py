import sqlite3

class Database:
    
    tables = {} #stores table_name:columns key pairs of all tables in db
    
    def __init__(self, db_name):
        '''Creates or connects to database and interaction cursor. 
        Checks for existing tables storing needed info for methods.'''
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()
        res = self.c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [table for table in res]
        for table in tables:
            cols = self.get_col_names(table[0])
            self.tables[table[0]] = cols
    
    def get_col_names(self, table_name):
        '''Returns a list of column names from a specified table.'''
        self.c.execute("SELECT * from {}".format(table_name))
        return [member[0] for member in self.c.description]
    
    def create_table(self, table_name, columns):
        '''Adds new table to database. 
        columns = list of tuple pairs of (column_name, data_type)
        e.g. [('colname1', 'TEXT'), ('colname2', 'TEXT')]
        data_type options = NULL, INTEGER, REAL, TEXT, BLOB'''
        column_string = ''
        for column in columns:
            if column == columns[-1]:
                column_info = '{} {}'.format(column[0], column[1])
            else:
                column_info = '{} {}, '.format(column[0], column[1])
            column_string += column_info
        table_creation = 'CREATE TABLE IF NOT EXISTS {}({})'.format(table_name, column_string)
        self.c.execute(table_creation)
        columns = [column[0] for column in columns] 
        self.tables[table_name] = columns
       
    def data_entry(self, table_name, values, columns=None):
        '''Enters new data into specified table.
        columns = list of column names e.g. ['colname1', 'colname2']
        values = list of tuples, were tuples are ordered by column
        e.g. ('colname1_value', 'colname2_value')
        '''
        if not columns:
            columns = self.tables[table_name]
        column_string = ''
        for column in columns:
            if column == columns[-1]:
                column_info = '{}'.format(column)
            else:
                column_info = '{}, '.format(column)
            column_string += column_info
        placeholders = '?, ' * (len(columns)-1) + '?'
        entry = 'INSERT INTO {} ({}) VALUES({})'.format(table_name, column_string, placeholders)
        self.c.execute(entry, values)
        self.conn.commit()
    
    def read_from_table(self, table_name):
        '''Returns all values from specified table.'''
        read = 'SELECT * FROM {}'.format(table_name)
        self.c.execute(read)
        data = self.c.fetchall()
        return data
    
    def close_database(self):
        '''Closes cursor and connection to database.'''
        self.c.close()
        self.conn.close()
        
if __name__ == "__main__":
    db = Database('revert_file.db')
    #~ columns = [('original_file_path', 'TEXT'), ('new_file_path', 'TEXT')]
    #~ db.create_table('revert_table', columns)
    #~ db.create_table('revert1', columns)
    #~ values = ('C:\\Users\\dougl\\Desktop', 'C:\\Users\\dougl\\Desktop')
    #~ db.data_entry('revert1', values)
    #~ print(db.read_from_table('revert'))
    print(db.tables)
    #~ help(Database)





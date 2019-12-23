import sqlite3
from sqlite3 import Error
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return conn
 
 
def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
def get_values_by_id(conn,repo_id):
    dic = {}
    cur = conn.cursor()
    cur.execute("SELECT * FROM github WHERE repository_ID = " + str(repo_id))
    column=get_column_names(conn)
    rows = cur.fetchall()
    counter = 0
    print(rows)
    for row in rows:
        for data in row:
            
            dic[column[counter]] = data
            counter = counter + 1
                
    return dic
def insert_value(conn,keys,values):
    sql = 'INSERT INTO github('
    string = ""
    for key in keys:
        string = string  + str(key) + ','
    sql = sql + string[0:-1] + ')' + '\n'
    sql = sql + 'VALUES('
    string  = ""
    for value in values:
        string = string  + '?,'
    sql = sql + string[0:-1] + ')'
    cur = conn.cursor()
    count = cur.execute(sql,values)
    conn.commit()
    return count
def update_value(conn,keys,values,repo_id):
    sql = 'UPDATE github\n'
             # SET priority = ? ,
              #    begin_date = ? ,
               #   end_date = ?
              #WHERE id = ?
    sql = sql + 'SET '
    for key in keys:
        sql = sql + ' ' +  str(key) + ' = ? ,'
    sql = sql[0:-1] + '\n' + 'where repository_ID = ?'
    
    cur = conn.cursor()
    cur.execute(sql, values + [repo_id])
    conn.commit()
def get_column_names(conn):
    column_names = []
    cursor = conn.execute('select * from github')
    colnames=cursor.description
    for row in colnames:
        column_names.append(row[0])
    return column_names
def get_values(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM github")
    column=get_column_names(conn)
    rows = cur.fetchall()
    output = []
    for row in rows:
        dic = {}
        counter = 0
        for data in row:
            
            dic[column[counter]] = data
            counter = counter + 1
        output.append(dic)
                
    return output      

def setup():
    conn = None
    database = r"pythonsqlite.db"
    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS github (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        repository_ID TEXT ,
                                        name TEXT,
                                        url TEXT,
                                        created_date DATETIME,
                                        last_push_date DATETIME,
                                        description TEXT,
                                        stars  INTEGER
                                    ); """
 
    # create a database connection
    conn = create_connection(database)
 
    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_projects_table)
    return conn
##def main():
##    database = r"pythonsqlite.db"
##    #repository_ID = models.CharField(max_length=2000)
##    #name = models.CharField(max_length=2000,blank=True,null=True)
##    #url = models.CharField(max_length=2000,blank=True,null=True)
##    #created_date = models.DateTimeField()
##    #last_push_date = models.DateTimeField()
##    #description = models.CharField(max_length=2000,blank=True,null=True)
##    #stars = models.PositiveIntegerField()
##    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS github (
##                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
##                                        repository_ID TEXT ,
##                                        name TEXT,
##                                        url TEXT,
##                                        created_date DATETIME,
##                                        last_push_date DATETIME,
##                                        description TEXT,
##                                        stars  INTEGER
##                                    ); """
## 
##    # create a database connection
##    conn = create_connection(database)
## 
##    # create tables
##    if conn is not None:
##        # create projects table
##        create_table(conn, sql_create_projects_table)
##        values = {'repository_ID': 55584627,
##     'name': 'http-prompt',
##     'description': 'HTTPie + prompt_toolkit = an interactive command-line HTTP client featuring autocomplete and syntax highlighting',
##     'created_date':
##     '2016-04-06T07:24:35Z',
##     'last_push_date': '2019-08-09T11:34:22Z',
##     'url': 'https://api.github.com/repos/eliangcs/http-prompt',
##     'stars': 7595}
##        #print(insert_value(conn,list(values.keys()),tuple(values.values())))
##        print(get_values(conn))
##        keys = ['name','stars']
##        values = ['magic',0]
##        repo_id = 55584627
##        print(update_value(conn,keys,values,repo_id))
## 
##        # create tasks table
##        #create_table(conn, sql_create_tasks_table)
##    else:
##        print("Error! cannot create the database connection.")
## 
## 
##if __name__ == '__main__':
##    main()

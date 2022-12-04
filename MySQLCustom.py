from mysql.connector import connect, Error
from app.model import PostSchema, UserSchema


def serverConnection(host_name, user_name, user_password):
    connection = None
    try:
        connection = connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        if connection.is_connected():
            print("MySQL Database connection successful.")
        else:
            print('MySQL Database connection unsuccessful.')
    except Error as err:
        print(f"Error: '{err}'")
    return connection


class MySQLCustom:

    def __init__(self, host='localhost', user='root', password=''):
        try:
            self.my_db = serverConnection(host, user, password)
            self.cursor = self.my_db.cursor(buffered=True)
        except Error as e:
            print(e)

    def is_connected(self):
        return self.my_db.is_connected()

    def create_database(self, name_db: str):
        state_flag = False
        try:
            self.cursor.execute('CREATE DATABASE IF NOT EXISTS {};'.format(name_db))
            state_flag = True
        except Error as e:
            print(e)
        return state_flag

    def create_user_table(self, database: str, user_table_name='default_user_table'):
        state_flag = False
        try:
            self.cursor.execute('USE {}'.format(database))
            self.cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS {} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100),
                    email VARCHAR(100),
                    password VARCHAR(100)
                );'''.format(user_table_name)
            )
            self.cursor.execute('DESC {};'.format(user_table_name))
            state_flag = True
        except Error as e:
            print(e)
        return state_flag

    def create_default_table(self, database: str, table_name='default_table', seeding_flag: bool = True):
        state_flag = False
        try:
            self.cursor.execute('USE {}'.format(database))
            self.cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS {} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(100),
                    link VARCHAR(200),
                    description VARCHAR(400),
                    tags VARCHAR(400)
                );'''.format(table_name)
            )
            self.cursor.execute('DESC {};'.format(table_name))
            if not self.is_empty_table(db_name=database, table_name=table_name):  # If not already exists information
                # self.cursor.execute('TRUNCATE TABLE {}'.format(table_name))  # Clear table information for security
                self.cursor.executemany(
                    ''' INSERT INTO {} (title, link, description, tags) VALUES (%s, %s, %s, %s)'''.format(table_name),
                    [
                        (
                            'Notion', 'https://notion.so',
                            'All in one tool to organize teams and ideas. Write, plan, collaborate, and get organized.',
                            'organization,planning,collaboration,writing,calendar'
                        ),
                        (
                            'json-server', 'https://github.com/typicode/json-server',
                            'Fake REST API based on a json schema. Useful for mocking and creating APIs for front-end '
                            'devs to consume in coding challenges.',
                            'api,json,schema,node,github,rest'
                        ),
                        (
                            'fastify', 'https://www.fastify.io/',
                            'Extremely fast and simple, low-overhead web framework for NodeJS. Supports HTTP2.',
                            'web,framework,node,http2,https,localhost'
                        )
                    ]
                )
            state_flag = True
        except Error as e:
            print(e)
        return state_flag

    def is_empty_table(self, db_name: str, table_name: str):
        self.cursor.execute('USE {}'.format(db_name))
        self.cursor.execute('SELECT EXISTS (SELECT 1 FROM {})'.format(table_name))
        info = self.cursor.fetchone()
        return bool(info[0])

    def get_table_json(self, table_name: str, column='*', flag_tags=False):
        json_data = []
        try:
            self.cursor.execute('SELECT {0} FROM {1}'.format(column, table_name))
            row_headers = [x[0] for x in self.cursor.description]  # this will extract row headers
            rv = self.cursor.fetchall()
            for result in rv:
                json_data.append(dict(zip(row_headers, result)))
            if flag_tags:
                for tool in json_data:
                    tool['tags'] = (tool['tags'].split(','))
        except Error as e:
            print(e)
        return json_data

    def filter_by_id(self, table_name: str, id: int):
        filter_tool = {}
        json_table = self.get_table_json(table_name=table_name, flag_tags=True)
        for tool in json_table:
            if tool['id'] == id:
                filter_tool = tool
        return filter_tool if filter_tool else {'error': 'There is no tool with id = {}'.format(id)}

    def filter_by_tag(self, table_name: str, tag: str):
        json_table = self.get_table_json(table_name=table_name, flag_tags=True)
        filter_tools = []
        for tool in json_table:
            if tag in tool['tags']:
                filter_tools.append(tool)
        return filter_tools

    def post_new_tool(self, table_name: str, new_tool: PostSchema):
        dict_tool = dict(new_tool)
        table_json = self.get_table_json(table_name=table_name, flag_tags=True)
        table_len = len(table_json)
        try:
            self.cursor.execute(
                ''' INSERT INTO {0} (title, link, description, tags) VALUES (%s, %s, %s, %s)'''.format(table_name),
                (dict_tool['title'], dict_tool['link'], dict_tool['description'],
                 ','.join(str(i) for i in dict_tool['tags']))
            )
            self.commit()
            dict_tool['id'] = table_json[table_len-1]['id'] + 1  # add id as preview table len + 1
        except Error as e:
            print(e)
        return dict_tool

    def delete_tool_by_id(self, table_name: str, id: int):
        json_table = self.get_table_json(table_name=table_name, flag_tags=True)
        delete_flag = False
        for tool in json_table:
            if tool['id'] == id:
                try:
                    self.cursor.execute('DELETE FROM {0} WHERE id = {1}'.format(table_name, id))
                    self.commit()
                    delete_flag = True
                except Error as e:
                    return {'error': e}
        return {} if delete_flag else {'error': 'There is no tool with id = {}'.format(id)}

    def user_signup(self, table_name: str, new_user: UserSchema):
        dict_user = dict(new_user)
        try:
            self.cursor.execute(
                ''' INSERT INTO {0} (name, email, password) VALUES (%s, %s, %s)'''.format(table_name),
                (dict_user['name'], dict_user['email'], dict_user['password'])
            )
            self.commit()
        except Error as e:
            print(e)
        return dict_user

    def commit(self):
        try:
            self.my_db.commit()
        except Error as e:
            print(e)

    def close(self):
        try:
            self.cursor.close()
            self.my_db.close()
            print('MySQL connection is closed.')
        except Error as e:
            print(e)

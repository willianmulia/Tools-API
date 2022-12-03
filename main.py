import uvicorn
from fastapi import FastAPI, Body, Depends
from app.model import PostSchema, UserSchema, UserLoginSchema
from MySQLCustom import MySQLCustom
from credentials import credentials
from app.auth.jwt_handler import sighJWT
from app.auth.jwt_bearer import JWTBearer


db_name = 'db_tools'
table_name = 'tools'
user_table_name = 'users'


app = FastAPI()  # Create FastAPI instance

# Create MYSQLCustom instance
my_db = MySQLCustom(
    host=credentials.get('HOST'),
    user=credentials.get('USER'),
    password=credentials.get('PASSWORD')
)

# Creating e seeding database e tables
if my_db.is_connected():
    state_flag = my_db.create_database(db_name)
    if state_flag:
        state_flag = my_db.create_default_table(database=db_name, table_name=table_name)
        user_state_flag = my_db.create_user_table(database=db_name, user_table_name=user_table_name)
        if state_flag:
            my_db.commit()
            print('MySQL database online....')


@app.get('/', tags=['hello'])
def hello():
    return {'message': 'WELCOME TO API'}


# Get All Tools
@app.get('/tools', tags=['tools'])
def get_tools():
    return my_db.get_table_json(table_name=table_name, flag_tags=True)


# Get single post {id}
@app.get('/tools/{id}', tags=['tools'])
def get_tool_by_id(id: int):
    return my_db.filter_by_id(table_name=table_name, id=id)


# Get single post by Tag
@app.get('/tools/{tag}', tags=['tools'])
def get_tool_by_tag(tag: str):
    return my_db.filter_by_tag(table_name=table_name, tag=tag)


# Post a single tool
@app.post('/tools', dependencies=[Depends(JWTBearer())], tags=['tools'])
def add_new_tool(tool: PostSchema):
    return my_db.post_new_tool(table_name=table_name, new_tool=tool)


@app.delete('/tools/{id}', dependencies=[Depends(JWTBearer())], tags=['tools'])
def delete_tool(id: int):
    return my_db.delete_tool_by_id(table_name=table_name, id=id)


# User Signup [ Create a new user ]
@app.post('/user/signup', tags=['user'])
def user_signup(user: UserSchema = Body()):
    my_db.user_signup(table_name=user_table_name, new_user=user)
    return sighJWT(user.email)


def check_user(data: UserLoginSchema):
    available_users = my_db.get_table_json(table_name=user_table_name)
    for user in available_users:
        if user['email'] == data.email and user['password'] == data.password:
            return True
    return False


@app.post('/user/login', tags=['user'])
def user_login(user: UserLoginSchema = Body()):
    if check_user(user):
        return sighJWT(user.email)
    else:
        return {'error': 'Invalid login details'}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=3000)

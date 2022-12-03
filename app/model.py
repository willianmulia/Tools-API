from pydantic import BaseModel, Field, EmailStr


class PostSchema(BaseModel):
    title: str = Field(default=None)
    link: str = Field(default=None)
    description: str = Field(default=None)
    tags: list = Field(default=None)

    class Config:
        schema_extra = {
            'title': 'NewToolSchema',
            'link': 'new_tool_link.com',
            'description': 'This is a new tool description',
            'tags': ['tag1', 'tag2', 'tag3']
        }


class UserSchema(BaseModel):
    name: str = Field(default=None)
    email: EmailStr = Field(default=None)
    password: str = Field(default=None)

    class Config:
        the_schema = {
            'name': 'Will',
            'email': 'willianmulia@gmail.com',
            'password': '123'
        }


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(default=None)
    password: str = Field(default=None)

    class Config:
        the_schema = {
            'email': 'willianmulia@gmail.com',
            'password': '123'
        }

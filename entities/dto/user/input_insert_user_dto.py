from pydantic import BaseModel, Field


class InputInsertUserDto(BaseModel):
    user_name: str = Field('', example='hoge')
    mail_address: str = Field('', example='hoge@gmail.com')
    password: str = Field('', example='p@sword')

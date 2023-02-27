from pydantic import BaseModel, Field


class InputUpdateUserDto(BaseModel):
    user_name: str = Field('', example='hoge')
    mail_address: str = Field('', example='hoge@gmail.com')
    password: str = Field('', example='p@sword')

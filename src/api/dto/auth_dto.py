from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from models import UserStatus


class AuthRequestDTO(BaseModel):
    email: EmailStr = Field(..., description="Email пользователя", examples=["user@example.com"])
    password: str = Field(..., description="Пароль", examples=["SecurePass123"])


class AuthResponseDTO(BaseModel):
    access_token: str = Field(
        ...,
        description="Access токен для авторизации запросов",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."]
    )
    refresh_token: str = Field(
        ...,
        description="Refresh токен для обновления пары",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."]
    )
    token_type: str = Field(default="bearer", description="Тип токена", examples=["bearer"])
    expires_in: int = Field(..., description="Время жизни access токена в секундах", examples=[1800])



class RefreshRequestDTO(BaseModel):
    refresh_token: str = Field(
        ...,
        description="Refresh токен для получения новой пары",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."]
    )


class LogoutRequestDTO(BaseModel):
    refresh_token: str = Field(
        ...,
        description="Refresh токен для инвалидации",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."]
    )

class MessageResponseDTO(BaseModel):
    message: str = Field(..., description="Текст сообщения", examples=["Успешный выход из системы"])


class UserResponseDTO(BaseModel):
    id: int = Field(
        ...,
        description="Уникальный идентификатор пользователя",
        examples=["1"]
    )
    email: str = Field(..., description="Email пользователя", examples=["user@example.com"])
    status: UserStatus = Field(..., description="Статус аккаунта", examples=["active"])
    created_at: datetime = Field(..., description="Дата регистрации", examples=["2024-01-15T10:30:00Z"])

    model_config = {"from_attributes": True}

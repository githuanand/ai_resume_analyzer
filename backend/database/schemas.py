from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class JobMatchResponse(BaseModel):
    match_score: int
    strong_skills: list[str]
    missing_skills: list[str]
    recommendations: list[str]
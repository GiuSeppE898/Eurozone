from pydantic import BaseModel
class Goal(BaseModel):
    secondo: int
    minuto: int
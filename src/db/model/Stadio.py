from pydantic import BaseModel
class Stadio(BaseModel):
    stadium_id : int
    stadium_name : str
    stadium_city : str
    stadium_country_code : str
    stadium_capacity : int
    stadium_latitude : complex
    stadium_longitude : complex
    stadium_pitch_length : float
    stadium_pitch_width : float
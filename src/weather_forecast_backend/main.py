from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Query
from pydantic import BaseModel
import httpx

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class WeatherResponse(BaseModel):
    city: str
    temperature: float
    humidity: float

OPENWEATHER_API_KEY = ""
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"

@app.get("/weather", response_model=WeatherResponse)
async def get_weather(city: str = Query(..., description="Nome da cidade")):
    async with httpx.AsyncClient() as client:
        params = {"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric", "lang": "pt_br"}
        response = await client.get(BASE_URL, params=params)
        if response.status_code != 200:
            return WeatherResponse(city=city, temperature=0, humidity=0)
        data = response.json()
        return WeatherResponse(
            city=data["name"],
            temperature=data["main"]["temp"],
            humidity=data["main"]["humidity"],
        )

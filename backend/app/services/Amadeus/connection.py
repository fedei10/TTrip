from amadeus import Client, ResponseError
from app.config import Settings


amadeus = Client(
    client_id=Settings.AMADEUS_API_KEY,
    client_secret=Settings.AMADEUS_API_SECRET
)   


def test_amadeus_connection():
    try:
        response = amadeus.schedule.flights.get(
    carrierCode='TK',
    flightNumber='1816',
    scheduledDepartureDate='2026-02-13'
)

        print(response.data)
        return response.data
    except ResponseError as error:
        return f"Error: {error}"
    

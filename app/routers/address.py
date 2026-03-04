from fastapi import HTTPException, APIRouter
from geopy.geocoders import Nominatim
#db depend

router = APIRouter(prefix="/address", tags=["Address"])

geolocator = Nominatim(user_agent="fast_food")

@router.get("/location")
async def get_location(lat:float, lon:float):
    location_query = f"{lat}, {lon}"

    user_address = geolocator.reverse(location_query, language="uz")

    if not user_address:
        raise HTTPException(status_code=404, detail="Location not found!")
    
    return {
        "location": user_address.address,
        "address_details": user_address.raw.get("address")
    }
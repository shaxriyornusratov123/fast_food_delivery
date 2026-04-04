from fastapi import HTTPException, APIRouter
from geopy.geocoders import Nominatim
import asyncio

from app.database import db_dep
from app.models import Address
from app.dependencies import current_user_dep
from app.schemas.address import AddressCreateRequest, AddressCreatResponse

router = APIRouter(prefix="/address", tags=["Address"])

geolocator = Nominatim(user_agent="fast_food")


@router.get("/location")
async def get_location(lat: float, lon: float):
    location_query = f"{lat}, {lon}"

    user_address = geolocator.reverse(location_query, language="uz")

    if not user_address:
        raise HTTPException(status_code=404, detail="Location not found!")

    return {
        "location": user_address.address,
        "address_details": user_address.raw.get("address"),
    }


@router.post("/create", response_model=AddressCreatResponse)
async def create_address(
    session: db_dep, current_user: current_user_dep, create_data: AddressCreateRequest
):
    location_query = f"{create_data.latitude}, {create_data.longitude}"

    user_address = await asyncio.get_event_loop().run_in_executor(
        None, lambda: geolocator.reverse(location_query, language="uz")
    )
    if not user_address:
        raise HTTPException(status_code=404, detail="Location not found!")

    address = Address(
        user_id=current_user.id,
        location_name=user_address.address,
        latitude=create_data.latitude,
        longitude=create_data.longitude,
    )

    session.add(address)
    session.commit()
    session.refresh(address)
    return address

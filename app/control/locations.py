from fastapi import APIRouter, HTTPException
from ..models import Location
from ..dtos import LocationDto


router = APIRouter(prefix= '/location')

def get_payload(location):
    location_payload = {"city": location.city,
                        "country": location.country,
                        "zip_code": location.zip_code}
    return location_payload

@router.get("/list")
async def list_locations():
    locations=[]
    for location in Location.nodes.all():
        location_payload = get_payload(location)
        locations.append(location_payload)
    return locations


@router.post("/create")
async def create_location(location: LocationDto):
    location_new = Location(city= location.city,
                            country= location.country,
                            zip_code= location.zip_code).save()
    
    location_payload = get_payload(location)
    
    return {"location": location_payload}


@router.put("/update")
async def update_location(location: LocationDto):
    location_exists = Location.nodes.get_or_none(zip_code=location.zip_code)
    if location_exists is None:
        raise HTTPException(status=404, detail="LOCATION_NOT_FOUND")

    location_exists = Location(city= location.city,
                            country= location.country,
                            zip_code= location.zip_code).save()
    
    location_payload = get_payload(location)
    
    return {"location": location_payload}


@router.delete("/delete")
async def delete_location(zip_code:int):
    location_exists = Location.nodes.first(zip_code=zip_code)
    if location_exists is None:
        raise HTTPException(status=404, detail="LOCATION_NOT_FOUND")

    location_exists.delete()

    return {}
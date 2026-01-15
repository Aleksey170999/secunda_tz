from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from geopy.distance import geodesic

from app.db.base import get_db
from app.models.organization import Organization as OrganizationModel
from app.models.building import Building as BuildingModel
from app.models.activity import Activity as ActivityModel
from app.schemas.organization import Organization, OrganizationCreate

router = APIRouter(prefix="/organizations", tags=["organizations"])

@router.get("/{organization_id}", response_model=Organization)
async def get_organization(
    organization_id: int, 
    db: Session = Depends(get_db)
):
    db_org = db.query(OrganizationModel).filter(OrganizationModel.id == organization_id).first()
    if db_org is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    return db_org

@router.get("/", response_model=List[Organization])
async def search_organizations(
    name: Optional[str] = None,
    activity_id: Optional[int] = None,
    building_id: Optional[int] = None,
    lat: Optional[float] = None,
    lng: Optional[float] = None,
    radius_km: Optional[float] = None,
    min_lat: Optional[float] = None,
    min_lng: Optional[float] = None,
    max_lat: Optional[float] = None,
    max_lng: Optional[float] = None,
    db: Session = Depends(get_db)
):
    query = db.query(OrganizationModel)
    
    if name:
        query = query.filter(OrganizationModel.name.ilike(f"%{name}%"))
        
    if building_id:
        query = query.filter(OrganizationModel.building_id == building_id)
    
    if activity_id:
        def get_all_child_activity_ids(activity_id: int) -> List[int]:
            activity_ids = [activity_id]
            children = db.query(ActivityModel).filter(ActivityModel.parent_id == activity_id).all()
            for child in children:
                if child.level < 3:
                    activity_ids.extend(get_all_child_activity_ids(child.id))
            return activity_ids
        
        activity_ids = get_all_child_activity_ids(activity_id)
        query = query.join(OrganizationModel.activities).filter(ActivityModel.id.in_(activity_ids))
    
    if lat is not None and lng is not None and radius_km is not None:
        organizations = query.join(BuildingModel).all()
        result = []
        point = (lat, lng)
        for org in organizations:
            org_point = (org.building.latitude, org.building.longitude)
            distance = geodesic(point, org_point).kilometers
            if distance <= radius_km:
                result.append(org)
        return result
    
    if all([min_lat, min_lng, max_lat, max_lng]):
        query = query.join(BuildingModel).filter(
            BuildingModel.latitude >= min_lat,
            BuildingModel.latitude <= max_lat,
            BuildingModel.longitude >= min_lng,
            BuildingModel.longitude <= max_lng
        )
    
    return query.all()

@router.get("/buildings/{building_id}/organizations", response_model=List[Organization])
async def get_organizations_by_building(
    building_id: int, 
    db: Session = Depends(get_db)
):
    return db.query(OrganizationModel).filter(OrganizationModel.building_id == building_id).all()

@router.get("/activities/{activity_id}/organizations", response_model=List[Organization])
async def get_organizations_by_activity(
    activity_id: int,
    include_children: bool = True,
    db: Session = Depends(get_db)
):
    if include_children:
        def get_all_child_activity_ids(activity_id: int) -> List[int]:
            activity_ids = [activity_id]
            children = db.query(ActivityModel).filter(ActivityModel.parent_id == activity_id).all()
            for child in children:
                if child.level < 3:
                    activity_ids.extend(get_all_child_activity_ids(child.id))
            return activity_ids
        
        activity_ids = get_all_child_activity_ids(activity_id)
        return db.query(OrganizationModel).join(OrganizationModel.activities).filter(ActivityModel.id.in_(activity_ids)).all()
    else:
        return db.query(OrganizationModel).join(OrganizationModel.activities).filter(ActivityModel.id == activity_id).all()

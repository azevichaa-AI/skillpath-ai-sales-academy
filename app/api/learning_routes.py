from fastapi import APIRouter, HTTPException
from app.schemas.learning import LearningTrackBuildRequest
from app.services.learning_track_service import learning_track_service, learning_tracks_store

router = APIRouter(prefix="/api", tags=["learning"])

@router.post("/learning-track/build")
def build(payload: LearningTrackBuildRequest):
    track = learning_track_service.build_from_results(payload.employee_profile, payload.competency_results)
    learning_tracks_store[track["track_id"]] = track
    return track

@router.get("/learning-track/{track_id}")
def get_track(track_id: str):
    item = learning_tracks_store.get(track_id)
    if not item:
        raise HTTPException(status_code=404, detail="Learning track not found")
    return item

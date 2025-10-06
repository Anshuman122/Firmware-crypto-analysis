from fastapi import APIRouter

router = APIRouter()


@router.get("/datasets")
async def list_datasets():
    return {"datasets": []}



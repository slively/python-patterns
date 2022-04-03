
async def get_dir_sync_api(token: str):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")

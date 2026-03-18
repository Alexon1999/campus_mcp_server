from fastapi import HTTPException, status

def raise_400(detail: str):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

def raise_404(detail: str = "Ressource introuvable"):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
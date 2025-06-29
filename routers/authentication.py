from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, status
from sqlalchemy.orm import Session
from model import model, schemas
from util.util import *
from sqlalchemy.orm import Session
from typing import Annotated

router = APIRouter(tags=["authenticaton"])


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """
    
    I have't put database related queries of this section in repository
    package, for better readibility of the code.

 """ """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""


@router.post("/token", response_model=schemas.Token)
async def login(
    request: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(model.User).filter(model.User.username == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="invalid username"
        )

    if not verify_hash(user.password, request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="invalid username"
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": user.username})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
    }


@router.post("/refresh-token", response_model=schemas.Token)
async def refresh_token(refresh_token: str):
    payload = verify_token(refresh_token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": payload["sub"]})
    new_refresh_token = create_refresh_token(data={"sub": payload["sub"]})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": new_refresh_token,
    }


@router.get("/users/me", response_model=schemas.UserInfoResponse)
async def read_users_me(
    current_user: Annotated[schemas.UserInfoResponse, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    
    user = db.query(model.User).filter(model.User.id == current_user.id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

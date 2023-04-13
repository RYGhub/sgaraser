from sgaraser.server import models
import fastapi
from fastapi import Depends
from sgaraser.server import crud
from sgaraser.server import deps
from sgaraser.database.engine import Session
from sgaraser.database import tables
from sgaraser.server.authentication import auth
from typing import List

router = fastapi.routing.APIRouter(
    prefix="/api/user/v1",
    tags=["User v1"]
)


@router.get("/self", dependencies=[Depends(auth.implicit_scheme)], response_model=models.full.UserFull)
async def read_self(current_user: tables.User = fastapi.Depends(deps.dep_user)):
    return current_user


@router.get("/", dependencies=[Depends(auth.implicit_scheme)], response_model=List[models.read.UserRead])
async def read_all(current_user: tables.User = fastapi.Depends(deps.dep_user),
                   session: Session = fastapi.Depends(deps.dep_session)):
    return session.query(tables.User).all()


@router.put("/self", dependencies=[Depends(auth.implicit_scheme)], response_model=models.full.UserFull)
async def edit_self(new_user: models.edit.UserEdit, current_user: tables.User = fastapi.Depends(deps.dep_user),
                    session: Session = fastapi.Depends(deps.dep_session)):
    crud.quick_update(session, current_user, new_user)
    return current_user

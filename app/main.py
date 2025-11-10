from fastapi import FastAPI
from app.routers.customer import cart, history
from app.routers.public import resorts, search, roomtypes
from app.routers.partner import partner
from app.routers.admin import withdraw
app = FastAPI()

app.include_router(search.router)
app.include_router(resorts.router)
app.include_router(roomtypes.router)
app.include_router(cart.router)
app.include_router(partner.router)
app.include_router(history.router)
app.include_router(withdraw.router)

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.models.user_model import User
from app.models.item_model import Item
from app.models.booking_model import Booking
from app.models.cart_model import Cart
from app.routes.cart_routes import router as cart_router
from dotenv import load_dotenv
load_dotenv()

from app.database.database import Base, engine
from app.routes.payment_routes import router as payment_router

from app.routes.auth_routes import router as auth_router
from app.routes.item_routes import router as item_router
from fastapi import FastAPI, Depends
from app.services.jwt_bearer import verify_token
from app.routes.booking_routes import router as booking_router
from app.routes.admin_routes import router as admin_router
from app.routes.provider_routes import router as provider_router
from fastapi.staticfiles import StaticFiles

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
from fastapi.staticfiles import StaticFiles

app.mount("/qr_codes", StaticFiles(directory="qr_codes"), name="qr_codes")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(item_router)
app.include_router(booking_router)
app.include_router(admin_router)
app.include_router(provider_router)
app.include_router(cart_router)
app.include_router(payment_router)
@app.get("/")
def home():

    return {
        "message": "Rental Services API Running"
    }

@app.get("/dashboard")
def dashboard(user = Depends(verify_token)):

    return {
        "message": "Welcome to dashboard",
        "user": user
    }
from fastapi import FastAPI
from app.routers import auth, public, user, partner, admin

app = FastAPI(title="Resort Booking API")

# Public routes
app.include_router(public.landing.router, prefix="/", tags=["Public"])
app.include_router(public.resort.router, prefix="/resorts", tags=["Resorts"])

# Auth routes
app.include_router(auth.router, prefix="/auth", tags=["Auth"])

# User routes
app.include_router(user.customer.router, prefix="/user", tags=["User"])
app.include_router(user.booking.router, prefix="/user/bookings", tags=["User Booking"])
app.include_router(user.feedback.router, prefix="/user/feedback", tags=["Feedback"])
app.include_router(user.payment.router, prefix="/user/payment", tags=["Payment"])

# Partner routes
app.include_router(partner.resort.router, prefix="/partner/resorts", tags=["Partner Resort"])
app.include_router(partner.room_type.router, prefix="/partner/room-types", tags=["Partner Room Type"])
app.include_router(partner.booking.router, prefix="/partner/bookings", tags=["Partner Booking"])
app.include_router(partner.withdraw.router, prefix="/partner/withdraw", tags=["Partner Withdraw"])

# Admin routes
app.include_router(admin.withdraw_approval.router, prefix="/admin/withdraw", tags=["Admin Withdraw"])
app.include_router(admin.report.router, prefix="/admin/reports", tags=["Admin Reports"])

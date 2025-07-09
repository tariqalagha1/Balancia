from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.routers import billing, invite, export, changelog
from core.services import auth, subscription
from modules.crm import crm_router

app = FastAPI(title="Balancia Backend")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(billing.router, prefix="/billing", tags=["Billing"])
app.include_router(invite.router, prefix="/invite", tags=["Invite"])
app.include_router(export.router, prefix="/export", tags=["Export"])
app.include_router(changelog.router, prefix="/changelog", tags=["Changelog"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(subscription.router, prefix="/subscription", tags=["Subscription"])

# Register module routers
app.include_router(crm_router.router, prefix="/crm", tags=["CRM"])

# Optional: Health check
@app.get("/health")
def health_check():
    return {"status": "ok"} 
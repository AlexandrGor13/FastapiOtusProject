import uvicorn
from fastapi import FastAPI
from api import router as api_router
from create_fastapi_app import create_app
from core.admin import create_admin_panel



app: FastAPI = create_app(
    create_custom_static_urls=True,
)
app.include_router(api_router)
create_admin_panel(app)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True,
    )
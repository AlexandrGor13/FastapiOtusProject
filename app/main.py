from fastapi import FastAPI
from app.api import router as api_router
from app.create_fastapi_app import create_app
from app.core.admin import create_admin_panel


app: FastAPI = create_app(
    create_custom_static_urls=True,
)
app.include_router(api_router)
create_admin_panel(app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        reload=True,
    )

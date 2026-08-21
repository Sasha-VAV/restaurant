import uvicorn
from src.config import Settings
from src.api.app import create_app

if __name__ == "__main__":
    settings = Settings()
    app = create_app(settings)
    uvicorn.run(app, host=settings.app.host, port=settings.app.port)

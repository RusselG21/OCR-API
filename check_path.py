from app import app  # Import the FastAPI app instance
from fastapi.routing import APIRoute


def list_routes():
    for route in app.routes:
        if isinstance(route, APIRoute):
            print(f"Path: {route.path}, Methods: {route.methods}")


if __name__ == "__main__":
    list_routes()

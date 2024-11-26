import modal
import numpy as np
import time
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = modal.App("compute-benchmark")
image = modal.Image.debian_slim().pip_install("numpy", "fastapi[standard]")

fast_api_app = FastAPI()

fast_api_app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

class TransformRequest(BaseModel):
    points: List[float]
    width: int
    height: int
    depth: int


@app.function(image=image, gpu="H100")
@modal.web_endpoint(method="POST")
async def transform_points(request: TransformRequest):
    """Transform 3D points with given dimensions"""
    points = request.points
    width = request.width
    height = request.height
    depth = request.depth

    print(f"Received points: {points}")  
    print(f"Dimensions: {width}x{height}x{depth}")  

    start_time = time.time()
    try:
        points_array = np.array(points)
        print(f"Shape of input array: {points_array.shape}")  

        transformed = points_array * (width / 1000)

        result = {
            "success": True,
            "points": transformed.tolist(),
            "time_ms": (time.time() - start_time) * 1000
        }
        print(f"Result: {result}") 
        return result

    except Exception as e:
        print(f"Error occurred: {e}") 
        return {
            "success": False,
            "error": str(e),
            "time_ms": (time.time() - start_time) * 1000
        }

if __name__ == "__main__":
    modal.runner.main(app)
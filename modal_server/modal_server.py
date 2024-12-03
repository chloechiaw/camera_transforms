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

@app.function(image=image)
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

        aspect_ratio = width / height
        fov = 60.0 * (np.pi / 180.0)  
        z_near = 0.1
        z_far = depth
        
        f = 1.0 / np.tan(fov / 2.0)
        z_range = z_near - z_far
        
        transformed = []
        for i in range(0, len(points_array), 3):
            if i + 2 < len(points_array):
                x, y, z = points_array[i], points_array[i + 1], points_array[i + 2]
                
                perspective_z = z / z_far
                if perspective_z != 0.0:
                    transformed_x = (x * f * aspect_ratio) / perspective_z
                    transformed_y = (y * f) / perspective_z
                    transformed_z = (z * (z_near + z_far) + 2.0 * z_near * z_far) / z_range
                    
                    screen_x = (transformed_x + 1.0) * width / 2.0
                    screen_y = (transformed_y + 1.0) * height / 2.0
                    
                    transformed.extend([screen_x, screen_y, transformed_z])

        result = {
            "success": True,
            "points": transformed,
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


    
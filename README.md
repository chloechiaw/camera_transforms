# camera_transforms
<img width="602" alt="Screen Shot 2024-11-25 at 6 46 39 PM" src="https://github.com/user-attachments/assets/e1908724-7a89-4c3b-b50b-c5b1ff0ca09b">



simple 3D points transform into 2D screen coordinates using perspective projection.
currently randomly generates 100,000 points with viewport size 1920 x 1080. 
outputs operation speed (ms) from /rust-wasm and /modal_server 

# frontend/my-app 
created WebAssembly module and a Modal web endpoint to compare 3D point transformations speed 

# input:  
a flat array of 3D coordinates (grouped in threes as x,y,z)
viewport_width: Width of the screen/canvas
viewport_height: Height of the screen/canvas
view_depth: Maximum viewing distance (z_far)

# calculation (in lib.rs):
Vec<f64> containing transformed points where:
x: screen x-coordinate (in pixels)
y: screen y-coordinate (in pixels)
z: depth value (useful for z-buffering)

# calculation (in modal_server.py): 
simple JSON-like dictionary with results of the transformation of 3D points 


from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
import schemas as _schemas
import services as _services
import traceback
from typing import Dict, Any

app = FastAPI(
    title="AI Photo Enhancer API",
    description="API for enhancing images using AI models",
    version="1.0.0"
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to AI Photo Enhancer API"}

@app.get("/api")
async def root():
    return {"message": "Welcome to the AI Photo Enhancer with FastAPI"}

@app.post("/api/enhance/", response_model=Dict[str, Any])
async def enhance_image(enhanceBase: _schemas._EnhanceBase = Depends()):
    """
    Enhance an image using the selected AI model.
    
    Args:
        enhanceBase: Contains the base64 encoded image and enhancement parameters
        
    Returns:
        Dictionary containing the enhanced image in base64 format and MIME type
        
    Raises:
        HTTPException: If there's an error processing the image
    """
    try:
        encoded_img = await _services.enhance(enhanceBase=enhanceBase)
        
        return {
            "mime": "image/jpeg",
            "image": encoded_img
        }
        
    except ValueError as ve:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid image data: {str(ve)}"
        )
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Error processing image: {str(e)}"
        )
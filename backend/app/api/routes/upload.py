"""
Routes for file upload functionality.
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Dict, Any
import json
import csv
import io

from app.services.file_storage import FileStorage

router = APIRouter()


@router.post("/cleanup-old-files")
async def cleanup_old_files() -> Dict[str, Any]:
    """
    Manually trigger cleanup of old uploaded files.
    
    Removes files older than 24 hours and orphaned files.
    Useful for maintenance or testing.
    
    Returns:
        Status message about cleanup operation
    """
    try:
        files_before = len(FileStorage.list_files())
        FileStorage._cleanup_old_files(max_age_hours=24)
        files_after = len(FileStorage.list_files())
        
        return {
            "status": "success",
            "message": "Cleanup completed",
            "files_removed": files_before - files_after,
            "files_remaining": files_after
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cleanup failed: {str(e)}")


@router.post("/upload-plant-data")
async def upload_plant_data(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Upload plant data file (CSV or JSON).
    
    This endpoint accepts CSV or JSON files containing plant data
    and validates the format before storing.
    
    Args:
        file: Uploaded file (CSV or JSON)
        
    Returns:
        Response with upload status and file details
    """
    # Validate file type
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")
    
    file_extension = file.filename.split('.')[-1].lower()
    if file_extension not in ['csv', 'json']:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format: {file_extension}. Only CSV and JSON are supported."
        )
    
    try:
        # Read file content
        content = await file.read()
        
        # Validate and parse based on file type
        if file_extension == 'json':
            data = json.loads(content.decode('utf-8'))
            row_count = len(data) if isinstance(data, list) else 1
        else:  # CSV
            csv_content = content.decode('utf-8')
            csv_reader = csv.DictReader(io.StringIO(csv_content))
            data = list(csv_reader)
            row_count = len(data)
        
        # Extract column names
        if isinstance(data, list) and len(data) > 0:
            columns = list(data[0].keys())
        elif isinstance(data, dict):
            columns = list(data.keys())
        else:
            columns = []
        
        # Save file to storage and get file_id
        metadata = {
            "row_count": row_count,
            "columns": columns,
            "file_size_bytes": len(content)
        }
        file_id = FileStorage.save_file(content, file.filename, metadata)
        
        return {
            "status": "success",
            "message": "File uploaded and stored successfully",
            "file_id": file_id,
            "filename": file.filename,
            "file_type": file_extension,
            "row_count": row_count,
            "columns": columns,
            "file_size_bytes": len(content)
        }
        
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid JSON format: {str(e)}"
        )
    except csv.Error as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid CSV format: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file: {str(e)}"
        )

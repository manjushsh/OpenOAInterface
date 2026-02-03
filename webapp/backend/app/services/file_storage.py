"""
File storage service for managing uploaded plant data files.
Provides in-memory storage with session management.
"""
import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional, Any
from uuid import uuid4

# Storage directory for uploaded files
UPLOAD_DIR = Path(__file__).parent.parent.parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

# In-memory registry of uploaded files
_file_registry: Dict[str, Dict[str, Any]] = {}

# Default dataset identifier
DEFAULT_DATASET_ID = "default_la_haute_borne"


class FileStorage:
    """Manages uploaded plant data files."""
    
    @staticmethod
    def save_file(file_content: bytes, filename: str, metadata: Dict[str, Any]) -> str:
        """
        Save uploaded file to disk and register it.
        
        Args:
            file_content: Raw file bytes
            filename: Original filename
            metadata: File metadata (row_count, columns, etc.)
            
        Returns:
            Unique file_id for the uploaded file
        """
        # Generate unique file ID
        file_id = str(uuid4())
        timestamp = datetime.now()
        
        # Determine file extension
        file_ext = Path(filename).suffix
        stored_filename = f"{file_id}{file_ext}"
        file_path = UPLOAD_DIR / stored_filename
        
        # Save file to disk
        with open(file_path, 'wb') as f:
            f.write(file_content)
        
        # Register in memory
        _file_registry[file_id] = {
            'file_id': file_id,
            'original_filename': filename,
            'stored_path': str(file_path),
            'file_type': file_ext.lstrip('.'),
            'uploaded_at': timestamp,
            'metadata': metadata,
        }
        
        # Cleanup old files (older than 24 hours)
        FileStorage._cleanup_old_files()
        
        return file_id
    
    @staticmethod
    def get_file_path(file_id: Optional[str]) -> Optional[str]:
        """
        Get the file path for a given file_id.
        
        Args:
            file_id: Unique file identifier (None means use default)
            
        Returns:
            Absolute path to the file, or None if not found
        """
        if file_id is None or file_id == DEFAULT_DATASET_ID:
            # Return None to signal using default dataset
            return None
        
        file_info = _file_registry.get(file_id)
        if file_info and os.path.exists(file_info['stored_path']):
            return file_info['stored_path']
        
        return None
    
    @staticmethod
    def get_file_info(file_id: str) -> Optional[Dict[str, Any]]:
        """Get metadata for a file."""
        return _file_registry.get(file_id)
    
    @staticmethod
    def list_files() -> Dict[str, Dict[str, Any]]:
        """List all registered files."""
        return _file_registry.copy()
    
    @staticmethod
    def delete_file(file_id: str) -> bool:
        """
        Delete a file from storage.
        
        Args:
            file_id: File to delete
            
        Returns:
            True if deleted, False if not found
        """
        file_info = _file_registry.get(file_id)
        if not file_info:
            return False
        
        # Delete from disk
        file_path = file_info['stored_path']
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Remove from registry
        del _file_registry[file_id]
        return True
    
    @staticmethod
    def _cleanup_old_files(max_age_hours: int = 24):
        """Remove files older than specified hours."""
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        
        files_to_delete = []
        for file_id, info in _file_registry.items():
            if info['uploaded_at'] < cutoff_time:
                files_to_delete.append(file_id)
        
        for file_id in files_to_delete:
            FileStorage.delete_file(file_id)
        
        # Also clean up orphaned files on disk (files without registry entry)
        FileStorage._cleanup_orphaned_files()
    
    @staticmethod
    def _cleanup_orphaned_files():
        """Remove files on disk that have no registry entry."""
        if not UPLOAD_DIR.exists():
            return
        
        registered_paths = {info['stored_path'] for info in _file_registry.values()}
        
        for file_path in UPLOAD_DIR.iterdir():
            if file_path.is_file() and str(file_path) not in registered_paths:
                try:
                    file_path.unlink()
                except Exception:
                    pass  # Ignore errors for orphaned file cleanup

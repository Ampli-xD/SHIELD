import os
from supabase import create_client, Client

class SupabaseHandler:
    """
    A class to handle Supabase storage operations including initialization,
    file upload, retrieval, and deletion.
    """
    
    def __init__(self, supabase_url, supabase_key):
        """
        Initialize the Supabase client
        
        Args:
            supabase_url (str): The URL of your Supabase project
            supabase_key (str): The API key for your Supabase project
        """
        self.supabase: Client = create_client(supabase_url, supabase_key)
    
    def upload_file(self, file_path, bucket_name):
        """
        Upload a file to Supabase Storage
        
        Args:
            file_path (str): Path to the file to upload
            bucket_name (str): Name of the storage bucket
            
        Returns:
            dict: Response from Supabase
        """
        with open(file_path, 'rb') as f:
            file_contents = f.read()
            
        # Extract filename from path
        filename = file_path.split('/')[-1].split('\\')[-1]
        
        # Upload file
        result = self.supabase.storage.from_(bucket_name).upload(
            path=filename,
            file=file_contents,
            file_options={"content-type": "application/octet-stream"}
        )
        
        return result
    
    def get_file_url(self, file_name, bucket_name):
        """
        Get the URL for a file in Supabase Storage
        
        Args:
            file_name (str): Name of the file
            bucket_name (str): Name of the storage bucket
            
        Returns:
            str: Public URL for the file
        """
        return self.supabase.storage.from_(bucket_name).get_public_url(file_name)
    
    def download_file(self, file_name, bucket_name, destination_path=None):
        """
        Download a file from Supabase Storage
        
        Args:
            file_name (str): Name of the file to download
            bucket_name (str): Name of the storage bucket
            destination_path (str, optional): Path where to save the file
            
        Returns:
            bytes: File contents if destination_path is None, else None
        """
        # Get file bytes
        file_bytes = self.supabase.storage.from_(bucket_name).download(file_name)
        
        # If destination path is provided, save the file
        if destination_path:
            with open(destination_path, 'wb') as f:
                f.write(file_bytes)
            return None
        
        # Otherwise return the file bytes
        return file_bytes
    
    def delete_file(self, file_name, bucket_name):
        """
        Delete a file from Supabase Storage
        
        Args:
            file_name (str): Name of the file to delete
            bucket_name (str): Name of the storage bucket
            
        Returns:
            dict: Response from Supabase
        """
        return self.supabase.storage.from_(bucket_name).remove([file_name])
    
    def list_files(self, bucket_name, path=None):
        """
        List files in a Supabase Storage bucket
        
        Args:
            bucket_name (str): Name of the storage bucket
            path (str, optional): Path prefix to filter by
            
        Returns:
            list: List of files
        """
        return self.supabase.storage.from_(bucket_name).list(path)
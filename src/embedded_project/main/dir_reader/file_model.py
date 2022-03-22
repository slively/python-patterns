from xmlrpc.client import Boolean
from pydantic import BaseModel


class FileModel(BaseModel):
    """
    Represents a file returned by the DirReaderApi.
    """
    name: str
    path: str
    is_dir: Boolean
    contents: str

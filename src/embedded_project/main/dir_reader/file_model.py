from pydantic import BaseModel


class FileModel(BaseModel):
    """
    Represents a file returned by the DirReaderApi.
    """

    name: str
    path: str
    is_dir: bool
    contents: str

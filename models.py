from pydantic import BaseModel
from typing import Dict, Any, List

class QueryRequest(BaseModel):
    session_id: str
    query: str
    schema_dict: Dict[str, Any]
    remote_path: str
    filename: str
    chat_history: List[Dict[str, str]] = []
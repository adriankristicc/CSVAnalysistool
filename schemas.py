from pydantic import BaseModel
from typing import List, Dict


class NumericStats(BaseModel):
    min: float
    max: float
    avg: float
    count: int


class CSVAnalysisResponse(BaseModel):
    file_path: str
    rows: int
    columns: int
    headers: List[str]
    numeric_stats: Dict[str, NumericStats]
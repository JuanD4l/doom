"""
ESQUEMAS DE VALIDACIÓN DE DATOS (Data Transfer Objects)
"""

try:
    from pydantic import BaseModel, Field

    class ScoreCreate(BaseModel):
        player_name: str = Field(..., min_length=1, max_length=16)
        score: int = Field(..., ge=0)
        wave: int = Field(..., ge=1)
        kills: int = Field(..., ge=0)

    class ScoreResponse(BaseModel):
        id: int
        player_name: str
        score: int
        wave: int
        kills: int
        created_at: str

except ImportError:
    # Fallback sin Pydantic para entornos mínimos
    class ScoreCreate:
        def __init__(self, **data):
            self.player_name = str(data.get("player_name", "ANONYMOUS"))[:16]
            self.score = int(data.get("score", 0))
            self.wave = int(data.get("wave", 1))
            self.kills = int(data.get("kills", 0))

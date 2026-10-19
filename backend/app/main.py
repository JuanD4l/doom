"""
================================================================================
CYBER-DOOM 2099 // BACKEND API REST
================================================================================
Servidor FastAPI con CORS habilitado, base de datos SQLite real y endpoints:
  - GET  /api/health       -> Comprobación de estado para Render
  - GET  /api/leaderboard  -> Top 10 mejores puntajes
  - POST /api/scores       -> Registrar nueva puntuación con validación
  - GET  /api/stats        -> Métricas globales del juego
================================================================================
"""

import os
import json
from datetime import datetime
from app.database import get_connection

# Intentar arranque con FastAPI para producción (Render / Railway)
try:
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel, Field

    app = FastAPI(
        title="CYBER-DOOM 2099 Leaderboard API",
        description="API REST de persistencia y ranking global para CYBER-DOOM 2099",
        version="1.0.0"
    )

    # Configuración de CORS estricto pero abierto para GitHub Pages
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    class ScorePayload(BaseModel):
        player_name: str = Field(..., min_length=1, max_length=16)
        score: int = Field(..., ge=0)
        wave: int = Field(..., ge=1)
        kills: int = Field(..., ge=0)

    @app.get("/")
    def root():
        return {
            "success": True,
            "message": "CYBER-DOOM 2099 API en línea",
            "docs": "/docs"
        }

    @app.get("/api/health")
    def health_check():
        return {
            "success": True,
            "status": "healthy",
            "service": "CYBER-DOOM 2099 Leaderboard API",
            "timestamp": datetime.utcnow().isoformat()
        }

    @app.get("/api/leaderboard")
    def get_leaderboard(limit: int = 10):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, player_name, score, wave, kills, created_at
            FROM scores
            ORDER BY score DESC, wave DESC
            LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
        conn.close()

        data = [
            {
                "id": row["id"],
                "player_name": row["player_name"],
                "score": row["score"],
                "wave": row["wave"],
                "kills": row["kills"],
                "created_at": row["created_at"]
            }
            for row in rows
        ]

        return {
            "success": True,
            "count": len(data),
            "data": data
        }

    @app.post("/api/scores")
    def submit_score(payload: ScorePayload):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO scores (player_name, score, wave, kills)
            VALUES (?, ?, ?, ?)
        """, (payload.player_name, payload.score, payload.wave, payload.kills))
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()

        return {
            "success": True,
            "message": "Puntuación registrada exitosamente",
            "data": {
                "id": new_id,
                "player_name": payload.player_name,
                "score": payload.score,
                "wave": payload.wave,
                "kills": payload.kills
            }
        }

    @app.get("/api/stats")
    def get_stats():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as total_games, SUM(kills) as total_kills, MAX(score) as max_score FROM scores")
        row = cursor.fetchone()
        conn.close()

        return {
            "success": True,
            "data": {
                "total_games": row["total_games"] or 0,
                "total_kills": row["total_kills"] or 0,
                "max_score": row["max_score"] or 0
            }
        }

except ImportError:
    # Servidor nativo de respaldo sin dependencias externas para pruebas locales inmediatas
    from http.server import HTTPServer, BaseHTTPRequestHandler
    from urllib.parse import urlparse, parse_qs

    class NativeAPIHandler(BaseHTTPRequestHandler):
        def _send_json(self, status, payload):
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.end_headers()
            self.wfile.write(json.dumps(payload).encode("utf-8"))

        def do_OPTIONS(self):
            self._send_json(200, {"success": True})

        def do_GET(self):
            url = urlparse(self.path)
            if url.path == "/api/health" or url.path == "/":
                self._send_json(200, {
                    "success": True,
                    "status": "healthy",
                    "service": "CYBER-DOOM 2099 Native API",
                    "timestamp": datetime.utcnow().isoformat()
                })
            elif url.path == "/api/leaderboard":
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT id, player_name, score, wave, kills, created_at FROM scores ORDER BY score DESC LIMIT 10")
                rows = cursor.fetchall()
                conn.close()
                data = [{"id": r["id"], "player_name": r["player_name"], "score": r["score"], "wave": r["wave"], "kills": r["kills"], "created_at": r["created_at"]} for r in rows]
                self._send_json(200, {"success": True, "data": data})
            else:
                self._send_json(404, {"success": False, "error": "Ruta no encontrada"})

        def do_POST(self):
            url = urlparse(self.path)
            if url.path == "/api/scores":
                content_len = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(content_len)
                try:
                    payload = json.loads(body)
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO scores (player_name, score, wave, kills) VALUES (?, ?, ?, ?)",
                                   (payload.get("player_name", "CYBER_MARINE"), payload.get("score", 0), payload.get("wave", 1), payload.get("kills", 0)))
                    conn.commit()
                    new_id = cursor.lastrowid
                    conn.close()
                    self._send_json(201, {"success": True, "message": "Puntuación guardada", "data": {"id": new_id}})
                except Exception as e:
                    self._send_json(400, {"success": False, "error": str(e)})
            else:
                self._send_json(404, {"success": False, "error": "Ruta no encontrada"})

    app = None

# Punto de entrada directo
if __name__ == "__main__":
    import sys
    port = int(os.getenv("PORT", 8000))
    print(f">> Iniciando CYBER-DOOM API en puerto {port}...")
    try:
        import uvicorn
        uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
    except ImportError:
        print(">> Uvicorn/FastAPI no instalados. Usando servidor HTTP nativo...")
        server = HTTPServer(("0.0.0.0", port), NativeAPIHandler)
        print(f">> Servidor nativo escuchando en http://localhost:{port}")
        server.serve_forever()

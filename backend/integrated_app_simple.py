from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict, Any

# Import stats functionality
from wrestling_api import WrestlingAPI

def create_integrated_app() -> FastAPI:
    app = FastAPI(
        title="Ultimate Wrestling Platform",
        description="Combined wrestling statistics and news platform",
        version="2.0.0"
    )

    # CORS configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Initialize wrestling stats API
    wrestling_api = WrestlingAPI()

    # Include stats routers
    app.include_router(create_stats_router(wrestling_api), prefix="/stats")

    # Health check
    @app.get("/health")
    def health():
        return {"status": "ok", "service": "Ultimate Wrestling Platform"}

    return app

def create_stats_router(wrestling_api: WrestlingAPI):
    """Create router for wrestling statistics endpoints"""
    from fastapi import APIRouter
    
    router = APIRouter(tags=["wrestling-stats"])
    
    @router.get("/wrestlers")
    def get_all_wrestlers():
        """Get all wrestlers from the database"""
        try:
            wrestlers = wrestling_api.get_all_wrestlers()
            return {"wrestlers": wrestlers}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/wrestlers/{wrestler_id}")
    def get_wrestler(wrestler_id: str):
        """Get a specific wrestler by ID"""
        try:
            wrestler = wrestling_api.get_wrestler(wrestler_id)
            if not wrestler:
                raise HTTPException(status_code=404, detail="Wrestler not found")
            return wrestler
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/search")
    def search_wrestlers(q: str = Query(..., description="Search query")):
        """Search wrestlers by name or other criteria"""
        try:
            results = wrestling_api.search_wrestlers(q)
            return {
                "query": q,
                "results": results,
                "total_found": len(results),
                "wrestlers": results
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/top-rated")
    def get_top_rated_wrestlers(limit: int = Query(10, le=50)):
        """Get top-rated wrestlers"""
        try:
            wrestlers = wrestling_api.get_top_rated_wrestlers(limit)
            return {
                "wrestlers": [w['wrestler_data'] for w in wrestlers[:limit]],
                "total": len(wrestlers)
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/database-stats")
    def get_database_stats():
        """Get database statistics"""
        try:
            stats = wrestling_api.get_database_stats()
            return stats
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/promotions")
    def get_promotions():
        """Get all promotions"""
        try:
            promotions = wrestling_api.get_promotions()
            return {"promotions": promotions}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return router

# Create the integrated app
app = create_integrated_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)

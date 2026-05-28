from pathlib import Path
from app.config import KNOWLEDGE_DIR
from app.services.rag_service import rag_service
from app.services.data_loader import load_json

class KnowledgeService:
    def search(self, query: str, limit: int = 5, competency_id: str | None = None) -> list[dict]:
        return rag_service.search(query=query, limit=limit, competency_id=competency_id)

    def get_material(self, material_id: str) -> dict | None:
        materials = load_json("learning_materials.json")
        material = next((m for m in materials if m.get("material_id") == material_id), None)
        if not material:
            return None
        path = Path(material["path"])
        full_path = KNOWLEDGE_DIR.parent / path
        content = full_path.read_text(encoding="utf-8") if full_path.exists() else ""
        return {**material, "content": content}

    def content_status(self) -> dict:
        md_files = list(KNOWLEDGE_DIR.rglob("*.md")) if KNOWLEDGE_DIR.exists() else []
        return {
            "markdown_files": len(md_files),
            "indexed_chunks": len(rag_service.chunks),
            "files": [str(p.relative_to(KNOWLEDGE_DIR.parent)) for p in md_files],
        }

knowledge_service = KnowledgeService()

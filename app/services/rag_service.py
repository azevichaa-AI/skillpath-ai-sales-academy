from dataclasses import dataclass, asdict
from pathlib import Path
import re
from app.config import KNOWLEDGE_DIR

TOKEN_RE = re.compile(r"[a-zA-Zа-яА-ЯёЁ0-9_-]+")

@dataclass
class Chunk:
    source_id: str
    title: str
    path: str
    text: str
    metadata: dict

class RagService:
    def __init__(self, knowledge_dir: Path = KNOWLEDGE_DIR):
        self.knowledge_dir = knowledge_dir
        self.chunks: list[Chunk] = []
        self.index()

    def tokenize(self, text: str) -> set[str]:
        return {t.lower() for t in TOKEN_RE.findall(text or "") if len(t) > 2}

    def split_text(self, text: str, max_chars: int = 900) -> list[str]:
        sections = [s.strip() for s in re.split(r"\n(?=## |### |# )", text) if s.strip()]
        chunks = []
        for section in sections:
            if len(section) <= max_chars:
                chunks.append(section)
            else:
                paragraphs = [p.strip() for p in section.split("\n\n") if p.strip()]
                buf = ""
                for p in paragraphs:
                    if len(buf) + len(p) > max_chars and buf:
                        chunks.append(buf.strip())
                        buf = p
                    else:
                        buf = (buf + "\n\n" + p).strip()
                if buf:
                    chunks.append(buf.strip())
        return chunks or [text[:max_chars]]

    def index(self) -> None:
        self.chunks.clear()
        if not self.knowledge_dir.exists():
            return
        for path in sorted(self.knowledge_dir.rglob("*.md")):
            text = path.read_text(encoding="utf-8")
            title = self._extract_title(text, path.stem)
            rel = path.relative_to(self.knowledge_dir.parent).as_posix()
            for i, chunk_text in enumerate(self.split_text(text)):
                self.chunks.append(Chunk(
                    source_id=f"{path.stem}::{i}",
                    title=title,
                    path=rel,
                    text=chunk_text,
                    metadata={"file_stem": path.stem, "chunk_index": i}
                ))

    def _extract_title(self, text: str, fallback: str) -> str:
        for line in text.splitlines():
            if line.startswith("# "):
                return line[2:].strip()
        return fallback.replace("_", " ").title()

    def search(self, query: str, limit: int = 5, competency_id: str | None = None) -> list[dict]:
        q_tokens = self.tokenize(query)
        if competency_id:
            q_tokens |= self.tokenize(competency_id.replace("_", " "))
        scored = []
        for chunk in self.chunks:
            hay = f"{chunk.title} {chunk.path} {chunk.text}"
            tokens = self.tokenize(hay)
            overlap = q_tokens & tokens
            bonus = 0.0
            if competency_id and competency_id in chunk.path:
                bonus += 3.0
            if query.lower() in hay.lower():
                bonus += 2.0
            score = len(overlap) + bonus
            if score > 0:
                item = asdict(chunk)
                item["score"] = round(float(score), 3)
                scored.append(item)
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:limit]

rag_service = RagService()

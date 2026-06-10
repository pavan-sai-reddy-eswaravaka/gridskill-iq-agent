from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
KB_DIR = ROOT / "knowledge_base"


class KnowledgeRetriever:
    """
    Lightweight Foundry IQ-style knowledge retriever.

    This local prototype searches synthetic knowledge documents and returns
    grounded evidence snippets with source file names.
    """

    def __init__(self, knowledge_dir=KB_DIR):
        self.knowledge_dir = Path(knowledge_dir)
        self.documents = self._load_documents()

    def _load_documents(self):
        docs = []

        for path in self.knowledge_dir.glob("*.md"):
            text = path.read_text(encoding="utf-8")
            docs.append(
                {
                    "source": path.name,
                    "text": text,
                    "chunks": self._chunk_text(text)
                }
            )

        return docs

    def _chunk_text(self, text):
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
        return paragraphs

    def search(self, query, top_k=3):
        query_terms = set(query.lower().split())
        scored_chunks = []

        for doc in self.documents:
            for chunk in doc["chunks"]:
                chunk_terms = set(chunk.lower().split())
                score = len(query_terms.intersection(chunk_terms))

                if score > 0:
                    scored_chunks.append(
                        {
                            "source": doc["source"],
                            "score": score,
                            "content": chunk
                        }
                    )

        scored_chunks.sort(key=lambda x: x["score"], reverse=True)
        return scored_chunks[:top_k]

    def retrieve_for_role(self, role, certification, skill_gap):
        query = f"{role} {certification} {skill_gap}"
        return self.search(query, top_k=5)

    def format_evidence(self, evidence_items):
        if not evidence_items:
            return "No matching evidence found in the synthetic knowledge base."

        lines = []

        for idx, item in enumerate(evidence_items, start=1):
            lines.append(f"[Evidence {idx}] Source: {item['source']}")
            lines.append(item["content"])
            lines.append("")

        return "\n".join(lines).strip()


if __name__ == "__main__":
    retriever = KnowledgeRetriever()
    results = retriever.search("Grid Operations Analyst PL-300 Power BI modelling")
    print(retriever.format_evidence(results))
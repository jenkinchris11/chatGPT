"""Placeholder AI utilities."""

from dataclasses import dataclass, field
from typing import Dict, Any, List


@dataclass
class Assistant:
    name: str
    memory: Dict[str, Any] = field(default_factory=dict)

    def suggest_hashtags(self, text: str) -> List[str]:
        """Very naive hashtag generator based on words."""
        words = [w.strip("#") for w in text.split() if len(w) > 3]
        return [f"#{w.lower()}" for w in words[:5]]

    def create_metadata(self, description: str) -> Dict[str, str]:
        """Generate fake metadata based on description."""
        tags = ",".join(self.suggest_hashtags(description))
        return {"Description": description, "Tags": tags}


@dataclass
class AIEngine:
    assistants: Dict[str, Assistant] = field(default_factory=dict)

    def get(self, name: str) -> Assistant:
        if name not in self.assistants:
            self.assistants[name] = Assistant(name=name)
        return self.assistants[name]

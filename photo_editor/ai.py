"""Placeholder AI utilities."""

from dataclasses import dataclass, field
from typing import Dict, Any, List

from PIL import Image, ImageStat, ImageFilter, ImageChops


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

    def analyze_image(self, image: Image.Image) -> Dict[str, float]:
        """Analyze basic properties of the image."""
        stats = ImageStat.Stat(image.convert("L"))
        avg = stats.mean[0]
        # crude noise estimate: average absolute deviation from median filter
        median = image.filter(ImageFilter.MedianFilter(3))
        diff_img = ImageChops.difference(image, median).convert("L")
        noise = ImageStat.Stat(diff_img).mean[0]
        return {"avg_brightness": avg, "noise": noise}

    def suggest_edit_settings(self, image: Image.Image) -> Dict[str, Any]:
        """Return naive suggestions for edits based on analysis."""
        analysis = self.analyze_image(image)
        suggestions: Dict[str, Any] = {}
        if analysis["avg_brightness"] < 110:
            suggestions["brightness"] = 1.2
        if analysis["noise"] > 10:
            suggestions["denoise"] = True
        return suggestions

    def ask_questions(self) -> List[str]:
        """Return simple questions for the user about style."""
        return [
            "What overall mood are you aiming for?",
            "Do you prefer vibrant or muted colors?",
            "Should the results look natural or highly stylized?",
        ]


@dataclass
class AIEngine:
    assistants: Dict[str, Assistant] = field(default_factory=dict)

    def get(self, name: str) -> Assistant:
        if name not in self.assistants:
            self.assistants[name] = Assistant(name=name)
        return self.assistants[name]

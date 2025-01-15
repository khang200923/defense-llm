from dataclasses import dataclass, field
import json
import random
from utils import *

words = json.loads(get("words.json"))

@dataclass
class LLM:
    secret: int = field(default_factory=lambda: " ".join(random.choices(words, k=4)))

    def instruct(self, prompt: str) -> str:
        if len(prompt) > 4096:
            return "❌ Prompt is too long. Please keep it under 4096 characters."

        output = create(
            messages=[
                systemp(get("mainsys.md").format(secret=self.secret)),
                userp(get("mainusr.md").format(prompt=prompt))
            ],
            model="gpt-4o-mini-2024-07-18",
            max_tokens=400
        ).choices[0].message.content

        check = create(
            messages=[systemp(get("guardian.md").format(secret=self.secret, prompt=prompt, response=output))],
            model="gpt-4o-mini-2024-07-18",
            max_tokens=10,
            temperature=0
        ).choices[0].message.content

        if "true" == check.lower():
            return "❌ I was about to reveal the password, but then I remembered that I'm not allowed to do that."

        return output

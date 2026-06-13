"""SkillSieve — Multi-LLM Jury security gate for skill file validation.

Before any SKILL.md content is injected into an agent backstory or context
window, SkillSieve scans it for known ClawHavoc-style adversarial patterns.

In production this would submit the content to N independent LLM judges and
require consensus approval.  Here we implement a deterministic rule-based
scan that catches the documented ClawHavoc injection taxonomy.
"""

import re


class SkillSieveViolationError(Exception):
    """Raised when a skill file fails the security scan."""


# Known adversarial patterns (ClawHavoc injection taxonomy v1.0)
_PATTERNS: tuple[re.Pattern, ...] = (
    re.compile(r"ignore\s+(all\s+)?previous\s+instructions", re.IGNORECASE),
    re.compile(
        r"you\s+are\s+now\s+in\s+(dan|jailbreak|developer)\s+mode", re.IGNORECASE
    ),
    re.compile(
        r"disregard\s+(your\s+)?(system|safety)\s+(prompt|instructions)",
        re.IGNORECASE,
    ),
    re.compile(r"<\s*script\s*>", re.IGNORECASE),
    re.compile(r"eval\s*\(|exec\s*\(|__import__\s*\(", re.IGNORECASE),
)


class SkillSieve:
    """Validates skill file content before injection into agent context.

    Rule-based scan implements the SkillSieve component of the ClawHavoc
    defence framework.  Each pattern in ``_PATTERNS`` corresponds to a
    documented injection tactic.
    """

    def validate(self, skill_name: str, content: str) -> None:
        """Raise :exc:`SkillSieveViolationError` if *content* contains an injection.

        Args:
            skill_name: Used in error messages to identify the offending file.
            content:    Raw SKILL.md text to scan.
        """
        for pattern in _PATTERNS:
            if pattern.search(content):
                raise SkillSieveViolationError(
                    f"SkillSieve blocked '{skill_name}': "
                    f"detected injection pattern /{pattern.pattern}/"
                )

    def validate_and_return(self, skill_name: str, content: str) -> str:
        """Validate *content* and return it unchanged if safe."""
        self.validate(skill_name, content)
        return content


skill_sieve = SkillSieve()

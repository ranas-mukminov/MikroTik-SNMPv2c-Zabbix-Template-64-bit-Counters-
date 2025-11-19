from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict


class AIProvider(ABC):
    """Abstract interface for AI helpers used across the repository."""

    @abstractmethod
    def generate_blueprint_suggestions(self, payload: Dict[str, Any]) -> str:
        """Return human-readable blueprint hints."""

    @abstractmethod
    def generate_cost_optimization_report(self, payload: Dict[str, Any]) -> str:
        """Return narrative cost optimization report."""

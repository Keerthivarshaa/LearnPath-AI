"""
Prompt Builder package for LearnPath AI.

This package is responsible for constructing structured prompts
using outputs from the ML, DL, OCR and NLP modules before they
are sent to a Language Model (LLM/SLM).
"""

from .prompt_builder import PromptBuilder

__all__ = ["PromptBuilder"]
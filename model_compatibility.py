"""
Model Compatibility Layer for AnkiBrain

Handles mapping of unsupported model names to compatible alternatives
for the langchain ChatOpenAI integration.

This fixes the "Error Making Cards" issue when users select GPT-5 models
that are not yet supported by the current langchain version.
"""

import logging
from typing import Dict

# Configure logging for this module
logger = logging.getLogger(__name__)

# Model mapping from unsupported models to their closest supported equivalents
MODEL_COMPATIBILITY_MAP: Dict[str, str] = {
    # GPT-5 models (not yet supported by langchain 0.0.231) -> GPT-4 alternatives
    "gpt-5": "gpt-4",
    "gpt-5-mini": "gpt-4",
    # Future-proof mappings for potential other unsupported models
    "gpt-5-turbo": "gpt-4-turbo",
    "gpt-5.0": "gpt-4",
    "gpt-5.0-mini": "gpt-4",
}

# Models known to be supported by langchain 0.0.231
SUPPORTED_MODELS = [
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-16k",
    "gpt-3.5-turbo-0613",
    "gpt-3.5-turbo-16k-0613",
    "gpt-4",
    "gpt-4-0613",
    "gpt-4-32k",
    "gpt-4-32k-0613",
    "gpt-4-turbo",
    "text-davinci-003",
    "text-davinci-002",
    "code-davinci-002",
]


def get_compatible_model_name(requested_model: str) -> str:
    """
    Get a compatible model name for the requested model.

    If the requested model is supported, returns it unchanged.
    If the requested model is not supported, returns a compatible alternative.

    Args:
        requested_model: The model name requested by the user

    Returns:
        A model name that is compatible with the current langchain version

    Examples:
        >>> get_compatible_model_name("gpt-3.5-turbo")
        'gpt-3.5-turbo'

        >>> get_compatible_model_name("gpt-5")
        'gpt-4'

        >>> get_compatible_model_name("gpt-5-mini")
        'gpt-4'
    """
    if requested_model in SUPPORTED_MODELS:
        # Model is already supported, return as-is
        return requested_model

    if requested_model in MODEL_COMPATIBILITY_MAP:
        # Model has a known mapping, use the alternative
        compatible_model = MODEL_COMPATIBILITY_MAP[requested_model]

        logger.info(
            f"Model '{requested_model}' not supported by current langchain version. "
            f"Using compatible alternative: '{compatible_model}'"
        )

        return compatible_model

    # Model is unknown - fallback to GPT-4 as it's the most capable supported model
    logger.warning(
        f"Unknown model '{requested_model}'. "
        f"Using fallback model 'gpt-4' for compatibility."
    )

    return "gpt-4"


def is_model_supported(model_name: str) -> bool:
    """
    Check if a model is directly supported by the current langchain version.

    Args:
        model_name: The model name to check

    Returns:
        True if the model is supported, False otherwise
    """
    return model_name in SUPPORTED_MODELS


def get_model_info(model_name: str) -> Dict[str, any]:
    """
    Get information about a model and its compatibility status.

    Args:
        model_name: The model name to get info for

    Returns:
        Dictionary containing model information:
        - original_model: The originally requested model name
        - compatible_model: The model name that will actually be used
        - is_mapped: True if the model was mapped to a different one
        - is_supported: True if the original model is directly supported
    """
    compatible_model = get_compatible_model_name(model_name)

    return {
        "original_model": model_name,
        "compatible_model": compatible_model,
        "is_mapped": model_name != compatible_model,
        "is_supported": is_model_supported(model_name),
    }


def log_model_usage(requested_model: str, compatible_model: str) -> None:
    """
    Log model usage for debugging and monitoring purposes.

    Args:
        requested_model: The model originally requested
        compatible_model: The model actually being used
    """
    if requested_model != compatible_model:
        logger.info(
            f"Model compatibility mapping: {requested_model} -> {compatible_model}"
        )
    else:
        logger.debug(f"Using directly supported model: {requested_model}")


# Expose main function for easy importing
__all__ = [
    "get_compatible_model_name",
    "is_model_supported",
    "get_model_info",
    "log_model_usage",
]

from dataclasses import dataclass

import litellm

from token_meter.exceptions import (
    AuthenticationError,
    ContextWindowError,
    ModelNotFoundError,
    NetworkError,
    RateLimitError,
)


@dataclass
class RunResult:
    model: str
    input_tokens: int
    output_tokens: int
    response: object


def run_completion(
    model: str,
    prompt: str,
    api_key: str,
    max_tokens: int,
) -> RunResult:
    try:
        response = litellm.completion(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            api_key=api_key,
            max_tokens=max_tokens,
        )

    except litellm.exceptions.AuthenticationError as exc:
        raise AuthenticationError("Authentication failed. Check your API key.") from exc

    except litellm.exceptions.RateLimitError as exc:
        raise RateLimitError("Rate limit reached. Please try again later.") from exc

    except litellm.exceptions.NotFoundError as exc:
        raise ModelNotFoundError(
            f"Model '{model}' was not found or is unavailable."
        ) from exc

    except litellm.exceptions.ContextWindowExceededError as exc:
        raise ContextWindowError(
            "The prompt exceeds the model's context window."
        ) from exc

    except (
        litellm.exceptions.Timeout,
        litellm.exceptions.APIConnectionError,
    ) as exc:
        raise NetworkError("Unable to reach the model provider.") from exc

    usage = response.usage

    return RunResult(
        model=model,
        input_tokens=usage.prompt_tokens,
        output_tokens=usage.completion_tokens,
        response=response,
    )

from dataclasses import dataclass
import litellm


@dataclass
class RunResult:
    model: str
    input_tokens: int
    output_tokens: int
    response: object


def run_completion(model: str, prompt: str, api_key: str, max_tokens: int) -> RunResult:
    response = litellm.completion(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        api_key=api_key,
        max_tokens=max_tokens,
    )

    usage = response.usage

    return RunResult(
        model=model,
        input_tokens=usage.prompt_tokens,
        output_tokens=usage.completion_tokens,
        response=response,
    )

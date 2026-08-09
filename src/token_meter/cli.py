import click

from token_meter.formatter import build_result, print_json, print_rich
from token_meter.pricing import calculate_costs
from token_meter.runner import run_completion
from token_meter.repl import run_repl


@click.command()
@click.option("--model", default=None, help="Model to use.")
@click.option("--prompt", default=None, help="Prompt to send to the model.")
@click.option(
    "--prompt-file",
    default=None,
    type=click.Path(exists=True, dir_okay=False),
    help="Read the prompt from a file.",
)
@click.option("--api-key", default=None, help="API key for the model provider.")
@click.option(
    "--max-tokens",
    default=256,
    type=int,
    show_default=True,
    help="Maximum completion tokens.",
)
@click.option("--json", "json_output", is_flag=True, help="Output raw JSON.")
def main(
    model: str | None,
    prompt: str | None,
    prompt_file: str | None,
    api_key: str | None,
    max_tokens: int,
    json_output: bool,
) -> None:
    """Measure LLM token usage and API costs."""

    has_prompt = prompt is not None
    has_prompt_file = prompt_file is not None

    one_shot = (
        model is not None and api_key is not None and (has_prompt or has_prompt_file)
    )

    if not one_shot:
        run_repl(
            model=model,
            api_key=api_key,
            max_tokens=max_tokens,
        )
        return

    if prompt and prompt_file:
        raise click.UsageError("Use either --prompt or --prompt-file, not both")

    if prompt_file:
        with open(prompt_file, encoding="utf-8") as file:
            prompt = file.read()

    if not model:
        raise click.UsageError("--model is required in one-shot mode.")

    if not api_key:
        raise click.UsageError("--api-key is required in one-shot mode.")

    if not prompt or not prompt.strip():
        raise click.UsageError("Prompt cannot be empty.")

    result = run_completion(
        model=model, prompt=prompt, api_key=api_key, max_tokens=max_tokens
    )

    input_cost, output_cost, total_cost = calculate_costs(result.response)

    formatted = build_result(
        model=result.model,
        input_tokens=result.input_tokens,
        output_tokens=result.output_tokens,
        input_cost=input_cost,
        output_cost=output_cost,
        total_cost=total_cost,
    )

    if json_output:
        print_json(formatted)
    else:
        print_rich(formatted)


if __name__ == "__main__":
    main()

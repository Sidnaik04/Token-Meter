import click

from token_meter.formatter import build_result, print_rich
from token_meter.pricing import calculate_costs
from token_meter.runner import run_completion
from token_meter.exceptions import (
    AuthenticationError,
    TokenMeterError,
)

PROVIDERS = {
    "OpenAI": [
        "gpt-4o-mini",
        "gpt-4o",
        "o1-mini",
    ],
    "Gemini": [
        "gemini/gemini-2.5-flash",
        "gemini/gemini-3.6-flash",
    ],
}


def choose_provider() -> str:
    provider_names = list(PROVIDERS.keys())

    click.echo("Choose provider:")
    for index, provider in enumerate(provider_names, start=1):
        click.echo(f"{index}. {provider}")

    while True:
        choice = click.prompt("Provider", type=int)

        if 1 <= choice <= len(provider_names):
            return provider_names[choice - 1]

        click.echo("Invalid choice. Try again.")


def choose_model(provider: str) -> str:
    models = PROVIDERS[provider]

    click.echo(f"\nChoose model for {provider}:")
    for index, model in enumerate(models, start=1):
        click.echo(f"{index}. {model}")

    while True:
        choice = click.prompt("Model", type=int)

        if 1 <= choice <= len(models):
            return models[choice - 1]

        click.echo("Invalid choice. Try again.")


def prompt_for_api_key(provider: str) -> str:
    return click.prompt(
        f"\nEnter {provider} API key",
        hide_input=True,
    )


def run_repl(
    model: str | None = None,
    api_key: str | None = None,
    provider: str | None = None,
    max_tokens: int = 256,
) -> None:
    if provider is None:
        provider = choose_provider()

    if model is None:
        model = choose_model(provider)

    if api_key is None:
        api_key = prompt_for_api_key(provider)

    click.echo("\nToken Meter REPL")
    click.echo("Type /model, /provider, /exit, or /quit.")
    click.echo()

    while True:
        try:
            user_input = click.prompt(
                "token-meter",
                prompt_suffix="> ",
                default="",
                show_default=False,
            )
        except (KeyboardInterrupt, EOFError):
            click.echo("\nGoodbye.")
            return

        user_input = user_input.strip()

        if not user_input:
            continue

        if user_input in ("/exit", "/quit"):
            click.echo("Goodbye.")
            return

        if user_input == "/model":
            model = choose_model(provider)
            continue

        if user_input == "/provider":
            provider = choose_provider()
            model = choose_model(provider)

            # Provider changed, so the previous API key is invalid.
            api_key = prompt_for_api_key(provider)
            continue

        if user_input.startswith("/"):
            click.echo("Unknown command. Try /model /provider /exit")
            continue

        try:
            result = run_completion(
                model=model,
                prompt=user_input,
                api_key=api_key,
                max_tokens=max_tokens,
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

            print_rich(formatted)

        except KeyboardInterrupt:
            click.echo("\nGoodbye.")
            return

        except AuthenticationError:
            click.echo("Authentication failed. Please enter your API key again.")
            api_key = prompt_for_api_key(provider)
            continue

        except TokenMeterError as exc:
            click.echo(f"Error: {exc}")
            continue

        except KeyboardInterrupt:
            click.echo("\nGoodbye.")
            return

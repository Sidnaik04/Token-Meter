import click


@click.command()
@click.option("--model", default=None, help="Model to use.")
@click.option("--prompt", default=None, help="Prompt to send to the model.")
@click.option("--prompt-file", default=None, type=click.Path(exists=True))
@click.option("--api-key", default=None, help="API key for the model provider.")
@click.option("--max-tokens", default=256, type=int, show_default=True)
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

    click.echo(f"model={model}")
    click.echo(f"prompt={prompt}")
    click.echo(f"prompt_file={prompt_file}")
    click.echo(f"api_key={'***' if api_key else None}")
    click.echo(f"max_tokens={max_tokens}")
    click.echo(f"json={json_output}")


if __name__ == "__main__":
    main()

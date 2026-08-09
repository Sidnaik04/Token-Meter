import json

from rich.console import Console
from rich.table import Table


def build_result(
    model: str,
    input_tokens: int,
    output_tokens: int,
    input_cost: float | None,
    output_cost: float | None,
    total_cost: float | None,
) -> dict:
    return {
        "model": model,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "input_cost_usd": input_cost,
        "output_cost_usd": output_cost,
        "total_cost_usd": total_cost,
    }


def print_json(result: dict) -> None:
    print(json.dumps(result, indent=2))


def print_rich(result: dict) -> None:
    table = Table(title="Token Meter")

    table.add_column("Metric")
    table.add_column("Value")

    table.add_row("Model", result["model"])
    table.add_row("Input Tokens", str(result["input_tokens"]))
    table.add_row("Output Tokens", str(result["output_tokens"]))

    input_cost = result["input_cost_usd"]
    output_cost = result["output_cost_usd"]
    total_cost = result["total_cost_usd"]

    table.add_row(
        "Input Cost",
        "Pricing unavailable" if input_cost is None else f"${input_cost:.8f}",
    )
    table.add_row(
        "Output Cost",
        "Pricing unavailable" if output_cost is None else f"${output_cost:.8f}",
    )
    table.add_row(
        "Total Cost",
        "Pricing unavailable" if total_cost is None else f"${total_cost:.8f}",
    )

    Console().print(table)

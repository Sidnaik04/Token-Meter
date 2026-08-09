import litellm


# input cost, output cost, total cost
def calculate_costs(
    response: object,
) -> tuple[float | None, float | None, float | None]:
    try:
        total_cost = litellm.completion_cost(completion_response=response)

        model = response.model
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens

        input_cost, output_cost = litellm.cost_per_token(
            model=model, prompt_tokens=input_tokens, completion_tokens=output_tokens
        )

        return (
            round(input_cost, 8),
            round(output_cost, 8),
            round(total_cost, 8),
        )

    except litellm.exceptions.NotFoundError:
        return None, None, None

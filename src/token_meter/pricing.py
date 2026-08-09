import litellm


def calculate_cost(response: object) -> float | None:
    try:
        return litellm.completion_cost(completion_response=response)
    except litellm.exceptions.NotFoundError:
        return None

from src.financial.model.refill_request import RefillRequest


def get_refill_request(*, request_id) -> RefillRequest:
    return RefillRequest.objects.get(pk=request_id)
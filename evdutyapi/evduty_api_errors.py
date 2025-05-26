from aiohttp import ClientResponse, ClientResponseError


class EVDutyApiError(ClientResponseError):
    def __init__(self, error_response: ClientResponse):
        self.request_info = error_response.request_info
        self.history = error_response.history
        self.status = error_response.status
        self.message = error_response.reason
        self.headers = error_response.headers


class EVDutyApiInvalidCredentialsError(EVDutyApiError):
    pass
import time

class RequestTimingMiddleware:
    def __init__(self, get_response):
        # I store the get_response callable to pass the request down the chain
        self.get_response = get_response

    def __call__(self, request):
        # I record the exact time the request arrives
        start_time = time.time()

        # I pass the request to the next middleware or the actual view
        response = self.get_response(request)

        # I calculate how long it took to process the request
        duration = time.time() - start_time
        
        # I print the HTTP method, the endpoint path, and the duration in milliseconds
        print(f"[Metrics] {request.method} {request.path} took {duration * 1000:.2f} ms")

        return response
import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware

# Configure logging
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class TimerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Log the incoming request
        logging.info(f"Incoming request: {request.method} {request.url}")

        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        # Log the response status and processing time
        logging.info(f"Response status: {response.status_code} (Processed in {process_time:.4f} seconds)")

        response.headers["X-Process-Time"] = str(process_time)
        print(f"Request processed in {process_time:.4f} seconds")
        return response

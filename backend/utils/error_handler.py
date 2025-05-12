from functools import wraps
from fastapi import HTTPException, status
import traceback
from backend.utils.logger import setup_logger

logger = setup_logger()


class ApiError(Exception):
    """Base class for API errors"""

    def __init__(self, status_code, detail):
        self.status_code = status_code
        self.detail = detail
        super().__init__(self.detail)


class ValidationError(ApiError):
    """Raised when input validation fails"""

    def __init__(self, detail="Validation error"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class FileProcessingError(ApiError):
    """Raised when file processing fails"""

    def __init__(self, detail="File processing error"):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)


class ModelError(ApiError):
    """Raised when model processing fails"""

    def __init__(self, detail="Model error"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)


class OpenAIError(ApiError):
    """Raised when OpenAI API call fails"""

    def __init__(self, detail="OpenAI API error"):
        super().__init__(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=detail)


def error_handler(func):
    """
    Decorator for route handlers to standardize error handling
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ApiError as e:
            # Log the error
            logger.error(f"API Error: {e.detail}")
            # Re-raise as HTTPException for FastAPI to handle
            raise HTTPException(status_code=e.status_code, detail=e.detail)
        except ValueError as e:
            # Handle validation errors
            logger.error(f"Validation Error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            # Log unexpected errors
            logger.error(f"Unexpected error: {str(e)}")
            logger.debug(traceback.format_exc())
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred"
            )

    return wrapper
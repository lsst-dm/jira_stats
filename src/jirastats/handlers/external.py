"""Handlers for the app's external root, ``/jira_stats/``."""

from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from safir.dependencies.logger import logger_dependency
from safir.metadata import get_metadata
from structlog.stdlib import BoundLogger

from ..config import config
from ..models import Index

__all__ = ["get_index", "external_router"]


class ReviewsResponseModel(BaseModel):
    """Response model for the greeting endpoint."""

    reviews: dict = Field(..., title="Tickets per reviewer")
    review_counts: dict = Field(..., title="Number of reviews per reviewer")


external_router = APIRouter()
"""FastAPI router for all external handlers."""


@external_router.get(
    "/",
    description=(
        "Document the top-level API here. By default it only returns metadata"
        " about the application."
    ),
    response_model=Index,
    response_model_exclude_none=True,
    summary="Application metadata",
)
async def get_index(
    logger: Annotated[BoundLogger, Depends(logger_dependency)],
) -> Index:
    """GET ``/jira_stats/`` (the app's external root).

    Customize this handler to return whatever the top-level resource of your
    application should return. For example, consider listing key API URLs.
    When doing so, also change or customize the response model in
    `jirastats.models.Index`.

    By convention, the root of the external API includes a field called
    ``metadata`` that provides the same Safir-generated metadata as the
    internal root endpoint.
    """
    # There is no need to log simple requests since uvicorn will do this
    # automatically, but this is included as an example of how to use the
    # logger for more complex logging.
    logger.info("Request for application metadata")

    metadata = get_metadata(
        package_name="jira_stats",
        application_name=config.name,
    )
    return Index(metadata=metadata)


@external_router.get(
    "/reviews/pipelines",
    summary="Return last 60 days of pipelines reviews",
    response_model=ReviewsResponseModel,
)
async def get_pipelines_reviews() -> ReviewsResponseModel:
    """GET ``/jira_stats/reviews/pipelines``.

    Just returns a example response for now.
    """
    return ReviewsResponseModel(
        reviews={
            "Me": "DM-XXXXX",
        },
        review_counts={
            "Me": 1,
        },
    )

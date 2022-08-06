from urllib.request import Request

from fastapi import APIRouter, FastAPI, status, HTTPException

from pydantic import BaseModel

from datazeit.gateways.database import ClickHouseGateway
from datazeit.gateways.search_engine import QuickWitGateway
from datazeit.logger import logger
from datazeit.reviews_controller import ReviewsController

app = FastAPI()
router = APIRouter(prefix="/api/v1")


class ReviewRequest(BaseModel):
    text: str


@router.get("/")
def root():
    return {"message": "Datazeit ML Engineer Challenge"}


@router.post("/reviews", status_code=status.HTTP_200_OK)
def compute_reviews_by_brand_and_product(request_payload: ReviewRequest):
    """
    Compute the amount of reviews by brand and product type
    for all products which reviews include the text sent in the
    parameters
    """

    logger.info(f"Request Payload. [name={request_payload.text}]")

    try:
        controller = ReviewsController(
            search_engine_gtw=QuickWitGateway(), database_gtw=ClickHouseGateway()
        )
        res = controller.compute_reviews(keywords=request_payload.text)

    except Exception as e:
        logger.exception(e.args[0])
        raise HTTPException(status_code=400, detail=e.args[0])

    return res


app.include_router(router)

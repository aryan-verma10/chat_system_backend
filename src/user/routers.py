from fastapi import APIRouter
from .views import login_view

router = APIRouter(prefix="/users")


router.add_api_route("/otp", login_view.post, methods=["POST"])


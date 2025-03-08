from fastapi import APIRouter
from .views import login_view, sent_otp_view

router = APIRouter(prefix="/users")


router.add_api_route("/sent-otp", sent_otp_view.post, methods=["POST"])
router.add_api_route("/login", login_view.post, methods=["POST"])


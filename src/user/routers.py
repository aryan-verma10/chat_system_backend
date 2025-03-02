from fastapi import APIRouter
from .views import user_profile_view

router = APIRouter(prefix="/users")


router.add_api_route("/", user_profile_view.get, methods=["GET"])
router.add_api_route("/", user_profile_view.post, methods=["POST"])

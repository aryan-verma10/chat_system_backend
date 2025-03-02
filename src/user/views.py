
class UserProfileView:
    async def get(self):
        return {"message": "hello world"}
    
    async def post(self):
        return {"message": "Posted Successfully."}
    


user_profile_view = UserProfileView()
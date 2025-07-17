from .forms import UserLoginForm
from .models import User


async def user_login(form: UserLoginForm) -> User | None:
    user = await User.get(email=form.email)
    if user and user.is_active and user.verify_password(form.password):
        return user

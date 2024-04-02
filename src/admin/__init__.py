from .pass_change import ChangePasswordAdmin, PasswordRecoveryAdmin
from .commons.base import CustomAjaxAdmin
from .hero import HeroAdmin

__all__ = [
    HeroAdmin,
    ChangePasswordAdmin,
    PasswordRecoveryAdmin,
    CustomAjaxAdmin,
]

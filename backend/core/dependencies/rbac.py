from fastapi import Depends, HTTPException, status

from core.services.auth import get_current_user


def require_role(*roles):
    """
    FastAPI dependency to require a user to have one of the specified roles.
    Usage: Depends(require_role("Admin", "Staff"))
    """

    def role_checker(user=Depends(get_current_user)):
        if user.role is None or user.role.name not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required role(s): {roles}",
            )
        return user

    return role_checker

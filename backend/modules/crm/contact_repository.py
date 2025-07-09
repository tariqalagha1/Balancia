from core.repository.base import BaseTenantRepository
from .models import Contact

class ContactRepository(BaseTenantRepository):
    def __init__(self, db):
        super().__init__(db, Contact)
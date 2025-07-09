from typing import Any, Type

from sqlalchemy.orm import Session


class BaseTenantRepository:
    def __init__(self, db: Session, model: Type[Any]):
        self.db = db
        self.model = model

    def get_all(self, tenant_id: int, skip: int = 0, limit: int = 100):
        return (
            self.db.query(self.model)
            .filter(self.model.tenant_id == tenant_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_id(self, obj_id: int, tenant_id: int):
        return (
            self.db.query(self.model)
            .filter(self.model.id == obj_id, self.model.tenant_id == tenant_id)
            .first()
        )

    def create(self, obj_in: dict, tenant_id: int):
        db_obj = self.model(**obj_in, tenant_id=tenant_id)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, obj_id: int, obj_in: dict, tenant_id: int):
        db_obj = self.get_by_id(obj_id, tenant_id)
        if not db_obj:
            return None
        for key, value in obj_in.items():
            setattr(db_obj, key, value)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, obj_id: int, tenant_id: int):
        db_obj = self.get_by_id(obj_id, tenant_id)
        if not db_obj:
            return None
        self.db.delete(db_obj)
        self.db.commit()
        return db_obj

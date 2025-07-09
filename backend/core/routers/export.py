import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.dependencies.rbac import require_role
from core.middleware import get_tenant_id
from core.services.user import get_all_users

from ..database import get_db
from ..export_utils import generate_excel, generate_pdf, generate_print_html

router = APIRouter()


# User List Export Endpoints
@router.get("/export/pdf/users")
async def export_users_pdf(
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id),
    current_user=Depends(require_role("Admin", "Staff")),
):
    try:
        users_data = get_all_users(db, tenant_id=tenant_id)
        headers = ["ID", "Username", "Email", "Role"]
        data = [[u.id, u.username, u.email, u.role.name] for u in users_data]
        html = f"<h1>User List</h1><table><tr>{' '.join([f'<th>{h}</th>' for h in headers])}</tr>"
        for row in data:
            html += f"<tr>{' '.join([f'<td>{col}</td>' for col in row])}</tr>"
        html += "</table>"
        return generate_pdf(html, "users.pdf")
    except Exception as e:
        logging.exception("Failed to export users PDF")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Export failed"
        )


@router.get("/export/excel/users")
async def export_users_excel(
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id),
    current_user=Depends(require_role("Admin", "Staff")),
):
    try:
        users_data = get_all_users(db, tenant_id=tenant_id)
        headers = ["ID", "Username", "Email", "Role"]
        data = [[u.id, u.username, u.email, u.role.name] for u in users_data]
        return generate_excel(data, headers, "users.xlsx")
    except Exception as e:
        logging.exception("Failed to export users Excel")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Export failed"
        )


@router.get("/print/users")
async def print_users_view(
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id),
    current_user=Depends(require_role("Admin", "Staff")),
):
    try:
        users_data = get_all_users(db, tenant_id=tenant_id)
        template = "<h1>User List</h1><ul>%s</ul>"
        user_list = "".join([f"<li>{u.username} - {u.email}</li>" for u in users_data])
        return generate_print_html(template, {"user_list": user_list})
    except Exception as e:
        logging.exception("Failed to generate user print view")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Print generation failed",
        )


# --- Invoice Export Endpoints (commented out for clean build) ---
# @router.get("/export/pdf/invoices")
# async def export_invoices_pdf(
#     db: Session = Depends(get_db),
#     tenant_id: int = Depends(get_tenant_id),
#     current_user = Depends(require_role("Admin", "Accountant"))
# ):
#     try:
#         invoices_data = invoices.get_all_invoices(db, tenant_id=tenant_id)
#         # Implementation would be similar to users but with invoice data
#         return generate_pdf("<h1>Invoices PDF</h1>", "invoices.pdf")
#     except Exception as e:
#         logging.exception("Failed to export invoices PDF")
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Invoice export failed"
#         )

# @router.get("/export/excel/invoices")
# async def export_invoices_excel(db: Session = Depends(get_db)):
#     invoices_data = invoices.get_all_invoices(db)
#     # Implementation would be similar to users but with invoice data
#     return generate_excel([], [], "invoices.xlsx")

# @router.get("/print/invoices")
# async def print_invoices_view(db: Session = Depends(get_db)):
#     return generate_print_html("<h1>Invoices Print View</h1>", {})

# --- Inventory Report Export Endpoints (commented out for clean build) ---
# @router.get("/export/pdf/inventory")
# async def export_inventory_pdf(
#     db: Session = Depends(get_db),
#     tenant_id: int = Depends(get_tenant_id),
#     current_user = Depends(require_role("Admin", "InventoryManager"))
# ):
#     try:
#         inventory_data = inventory.get_inventory_report(db, tenant_id=tenant_id)
#         # Implementation would be similar to users but with inventory data
#         return generate_pdf("<h1>Inventory Report PDF</h1>", "inventory.pdf")
#     except Exception as e:
#         logging.exception("Failed to export inventory PDF")
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Inventory export failed"
#         )

# @router.get("/export/excel/inventory")
# async def export_inventory_excel(db: Session = Depends(get_db)):
#     inventory_data = inventory.get_inventory_report(db)
#     # Implementation would be similar to users but with inventory data
#     return generate_excel([], [], "inventory.xlsx")

# @router.get("/print/inventory")
# async def print_inventory_view(db: Session = Depends(get_db)):
#     return generate_print_html("<h1>Inventory Print View</h1>", {})

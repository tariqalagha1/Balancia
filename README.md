# ⚖️ Balancia ERP

**Balancia** is a modular, multi-tenant ERP SaaS platform designed for Arabic-speaking businesses. It provides powerful, plug-and-play business modules, Arabic RTL interface, and real-time financial control—perfect for growing companies across the MENA region.

---

## 🌟 Key Features

- 🌍 **Multi-Tenant Architecture**  
  Isolated data for each tenant using secure header-based context.

- 🧑‍💼 **Role-Based Access Control**  
  Admin, Staff, Viewer roles scoped by tenant.

- 🧾 **Modular ERP System**  
  Plug-in modules: CRM, Accounting, Inventory, Billing.

- 💳 **Subscription Logic**  
  Per-user billing with feature-based access (Basic, Pro, Elite).

- 🌐 **Arabic RTL + English Support**  
  Arabic-first design with RTL layout and language toggle.

- 🪄 **Neumorphic UI**  
  Soft, modern tactile design using pure CSS.

- 🖨️ **Print & PDF Export**  
  Arabic-friendly documents ready for printing or digital delivery.

- 📊 **Excel & Chart Reports**  
  Visual dashboards and Excel exports for financial insights.

---

## 📦 Modules

| Module         | Description                              |
|----------------|------------------------------------------|
| **Auth**       | JWT login, multi-tenant scoped users     |
| **CRM**        | Leads, contacts, opportunities           |
| **Accounting** | Double-entry ledger, AR/AP, taxes        |
| **Inventory**  | Warehouses, stock control, movement      |
| **Billing**    | Tenant plans, user quota, usage metrics  |
| **PDF/Excel**  | Invoice and report exports               |
| **Charts**     | Interactive dashboards (Elite only)      |

---

## 💰 Subscription Plans

| Plan     | Max Users | Modules           | Base Price | Per User |
|----------|-----------|-------------------|------------|----------|
| **Basic**| 3         | CRM               | $9.99      | $2       |
| **Pro**  | 10        | CRM + Inventory   | $29.99     | $3       |
| **Elite**| ∞         | All + Charts      | $59.99     | $4       |

---

## 🧱 Tech Stack

| Layer        | Tech                                   |
|--------------|----------------------------------------|
| **Backend**  | FastAPI, PostgreSQL, SQLAlchemy        |
| **Frontend** | Vue.js / React (i18n, RTL enabled)     |
| **Auth**     | JWT + OAuth2                           |
| **Storage**  | S3 / MinIO                             |
| **Exporting**| WeasyPrint, openpyxl, Chart.js         |
| **DevOps**   | Docker + Docker Compose                |

---

## 🛠️ Installation (Development)

```bash
git clone https://github.com/your-org/balancia-erp.git
cd balancia-erp
docker-compose up --build
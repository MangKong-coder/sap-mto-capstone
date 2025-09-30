---
trigger: glob
globs: *.py
---

### **Cursor Rule: Python Code Standards for Capstone Project**

**Objective:**
Ensure all generated Python code for the capstone project is clean, consistent, and production-ready, while staying simple enough for academic requirements.

---

#### 1. **General Style**

* Always follow **PEP 8** (4-space indentation, snake_case for variables/functions, PascalCase for classes).
* Use **type hints** for all function signatures and class attributes.
* Add **docstrings** to modules, classes, and functions (Google-style or NumPy-style preferred).
* Avoid unused imports.
* Keep functions small and single-purpose.

---

#### 2. **Project Structure**

* Use the following base structure:

  ```
  app/
    main.py              # FastAPI entrypoint
    api/                 # Route handlers
    db/                  # Database models & session
    crud/                # Database operations
    schemas/             # Pydantic models (request/response)
    services/            # Business logic
    utils/               # Helpers
  ```
* Place each entity (e.g., SalesOrder, ProductionOrder) in **models.py**, **schemas.py**, and **crud.py** for consistency.

---

#### 3. **Database (SQLAlchemy/SQLModel)**

* Always include `created_at` and `updated_at` as `TIMESTAMPTZ` columns with defaults.
* Use **Postgres enums** for fields like `status` instead of free-text strings.
* Define relationships explicitly with `back_populates`.
* Prefer **views** for reporting/aggregated data (e.g., component usage).

---

#### 4. **FastAPI API Layer**

* Use **APIRouter** for modular endpoints.
* Every `GET all` endpoint must be **paginated**.
* Return **Pydantic schemas**, not ORM models, from routes.
* Use `Depends(get_db)` for DB session injection.

---

#### 5. **CRUD Pattern**

Each CRUD file should follow this pattern:

```python
def get_item(db: Session, item_id: int) -> Optional[Model]:
    return db.query(Model).filter(Model.id == item_id).first()

def get_items(db: Session, skip: int = 0, limit: int = 10) -> List[Model]:
    return db.query(Model).offset(skip).limit(limit).all()

def create_item(db: Session, item: SchemaCreate) -> Model:
    db_item = Model(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
```

---

#### 6. **Error Handling & Validation**

* Use `HTTPException` with proper status codes in routes.
* Validate inputs using **Pydantic validators**.
* Always check foreign key existence before insert/update.

---

#### 7. **Testing & Reliability**

* Include **pytest** tests for each module (`tests/` folder).
* Mock DB where possible for unit tests.
* Ensure database transactions are rolled back in tests.

---

#### 8. **Extra (Capstone-specific)**

* Implement core flow: Sales Order → Planned Order → Production Order → Delivery → Billing.
* Use clear **status enums** to track order progression.
* Optionally: Add a **dashboard endpoint** returning JSON that could later power a Fiori-like UI.

---

👉 With this rule in place, Cursor will consistently generate **clean Python code tailored for your MTO capstone project**.

Do you want me to also create a **ready-to-paste `rules.json`** for Cursor with this standard, so you can just drop it in?
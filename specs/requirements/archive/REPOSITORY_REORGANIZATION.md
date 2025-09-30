# Repository Layer Reorganization

## Summary

The repository layer has been reorganized into a dedicated `repositories/` subfolder within `app/crud/`.

## New Structure

```
app/crud/
├── __init__.py                           # Re-exports all repository functions
├── repositories/                         # ⭐ NEW: Repository layer subfolder
│   ├── __init__.py                       # Exports all 56 repository functions
│   ├── customers.py                      # Customer CRUD
│   ├── products.py                       # Product CRUD
│   ├── orders.py                         # Order CRUD
│   ├── order_items.py                    # OrderItem CRUD
│   ├── planned_orders.py                 # PlannedOrder CRUD
│   ├── work_orders.py                    # WorkOrder CRUD
│   ├── components.py                     # Component CRUD
│   ├── component_usages.py               # ComponentUsage CRUD
│   ├── deliveries_repo.py                # Delivery CRUD
│   ├── invoices.py                       # Invoice CRUD
│   └── order_component_usage.py          # View accessor (read-only)
├── deliveries.py                         # Legacy (existing)
├── production_orders.py                  # Legacy (existing)
├── sales_orders.py                       # Legacy (existing)
└── users.py                              # Legacy (existing)
```

## Benefits

### 1. **Clear Organization**
- New repository functions are separated from legacy CRUD files
- Easier to distinguish between old and new code
- Better code organization for future maintenance

### 2. **Modular Structure**
- Repository layer is self-contained in its own folder
- Can be extended without cluttering the main crud folder
- Clear separation of concerns

### 3. **Backward Compatibility**
- All functions still exported through `app.crud`
- Existing imports continue to work without changes
- No breaking changes for code already using these functions

## Import Paths

### Option 1: Import from main crud module (recommended)
```python
from app.crud import (
    create_customer,
    get_customer_by_id,
    list_customers,
    create_order,
    get_order_by_id,
)
```

### Option 2: Import directly from repositories
```python
from app.crud.repositories import (
    create_customer,
    get_customer_by_id,
    list_customers,
)
```

### Option 3: Import specific module
```python
from app.crud.repositories.customers import (
    create_customer,
    get_customer_by_id,
)
```

## Migration Notes

### ✅ No Code Changes Required
All existing code using `from app.crud import ...` will continue to work without modification.

### Example Usage (unchanged)
```python
from sqlalchemy.orm import Session
from app.crud import create_customer, list_orders

def my_function(db: Session):
    # Works exactly as before
    customer = create_customer(db, {"name": "John Doe"})
    orders = list_orders(db, skip=0, limit=10)
```

## Files Moved

The following 11 files were moved from `app/crud/` to `app/crud/repositories/`:

1. ✅ `customers.py`
2. ✅ `products.py`
3. ✅ `orders.py`
4. ✅ `order_items.py`
5. ✅ `planned_orders.py`
6. ✅ `work_orders.py`
7. ✅ `components.py`
8. ✅ `component_usages.py`
9. ✅ `deliveries_repo.py`
10. ✅ `invoices.py`
11. ✅ `order_component_usage.py`

## Files Unchanged

The following legacy files remain in `app/crud/`:

- ✅ `deliveries.py` (legacy)
- ✅ `production_orders.py` (legacy)
- ✅ `sales_orders.py` (legacy)
- ✅ `users.py` (legacy)

## Testing

The reorganization maintains all functionality. To verify:

```bash
# In the mto-backend directory
python3 -c "from app.crud import create_customer; print('✓ Import successful')"
```

## Next Steps

1. **Service Layer**: Build business logic using these repository functions
2. **API Layer**: Create FastAPI endpoints that call service functions
3. **Tests**: Write unit tests for repository functions
4. **Migration**: Gradually migrate legacy CRUD files to the new pattern

## Documentation Updated

- ✅ `REPOSITORY_LAYER_GUIDE.md` - Updated import paths
- ✅ `REPOSITORY_LAYER_SUMMARY.md` - Updated file structure diagram
- ✅ `REPOSITORY_REORGANIZATION.md` - This file (new)

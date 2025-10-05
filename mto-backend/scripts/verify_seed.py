"""Quick script to verify seeded data."""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app.db.session import SessionLocal
from app.models import Customer, Product, WorkCenter, Component

db = SessionLocal()

print("=" * 60)
print("DATABASE SEED VERIFICATION")
print("=" * 60)
print(f"\nTotal Counts:")
print(f"  Customers: {db.query(Customer).count()}")
print(f"  Products: {db.query(Product).count()}")
print(f"  Work Centers: {db.query(WorkCenter).count()}")
print(f"  Components: {db.query(Component).count()}")

print(f"\nSample Customers:")
for c in db.query(Customer).limit(5).all():
    print(f"  - {c.name} ({c.customer_type.value})")

print(f"\nSample Products:")
for p in db.query(Product).limit(5).all():
    print(f"  - {p.sku}: {p.name} (${p.price:,.2f})")

print(f"\nSample Work Centers:")
for wc in db.query(WorkCenter).limit(5).all():
    print(f"  - {wc.name}")

print(f"\nSample Components:")
for comp in db.query(Component).limit(5).all():
    print(f"  - {comp.part_code}: {comp.name} (${comp.cost:,.2f})")

print("=" * 60)
db.close()

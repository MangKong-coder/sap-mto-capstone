# Database Scripts

This directory contains scripts for database management and seeding.

## Available Scripts

### `create_db.py`
Creates all database tables based on SQLAlchemy models.

**Usage:**
```bash
uv run python scripts/create_db.py
```

### `seed_data.py`
Seeds the database with initial data for entities without frontend CRUD interfaces.

**Usage:**

Basic seeding (adds data to existing database):
```bash
uv run python scripts/seed_data.py
```

Clear existing data and reseed (WARNING - deletes data):
```bash
uv run python scripts/seed_data.py --clear
```

## Seed Data Overview

The seed script populates the following entities:

### 1. **Customers** (10 records)
Various customer types representing different stakeholders:

- **Departments** (3 records)
  - Engineering Department
  - Physics Department
  - Computer Science Department

- **Campus Facilities** (2 records)
  - Main Campus Facilities
  - East Campus

- **Students** (3 records)
  - Student Project - Team Alpha
  - Student Project - Team Beta
  - Robotics Club

- **Vendors** (2 records)
  - Industrial Equipment Co.
  - Tech Supply Partners

Each customer includes:
- Name, email, phone
- Address
- Customer type (DEPARTMENT, CAMPUS, STUDENT, VENDOR)

---

### 2. **Products** (10 records)
Finished goods that can be ordered:

**Custom Machinery:**
- MACH-001: Custom CNC Machine ($25,000)
- MACH-002: Automated Assembly Line ($150,000)
- MACH-003: Industrial 3D Printer ($45,000)

**Custom Equipment:**
- EQUIP-001: Laboratory Workstation ($8,500)
- EQUIP-002: Testing Apparatus ($12,000)
- EQUIP-003: Robotics Platform ($15,000)

**Electronics:**
- ELEC-001: Custom Control Panel ($3,500)
- ELEC-002: Sensor Array System ($5,200)

**Furniture:**
- FURN-001: Custom Workbench ($1,200)
- FURN-002: Laboratory Cabinet System ($2,800)

Each product includes:
- Unique SKU
- Name and description
- Price

---

### 3. **Work Centers** (7 records)
Manufacturing locations where production occurs:

1. **Main Fabrication** - CNC machines and welding equipment
2. **Assembly Line 1** - Large equipment assembly
3. **Assembly Line 2** - Electronics and small components
4. **Testing & QC** - Quality control and testing
5. **Precision Machining** - High-precision machining
6. **Electronics Workshop** - Electronic assembly and programming
7. **Paint & Finishing** - Surface treatment

Each work center includes:
- Name
- Description
- Address within manufacturing complex

---

### 4. **Components** (25 records)
Raw materials and parts used in production:

**Raw Materials:**
- MAT-STEEL-001: Steel Sheet 4x8ft ($125)
- MAT-ALUM-001: Aluminum Bar 6ft ($85)
- MAT-PLASTIC-001: ABS Plastic Sheet ($45)
- MAT-WOOD-001: Hardwood Plank 8ft ($35)

**Electronic Components:**
- ELEC-MCU-001: Microcontroller Unit ($12.50)
- ELEC-SENSOR-001: Temperature Sensor ($8)
- ELEC-MOTOR-001: Stepper Motor ($45)
- ELEC-PWR-001: Power Supply 24V ($65)
- ELEC-RELAY-001: Industrial Relay ($18)
- ELEC-CABLE-001: Control Cable 50ft ($25)

**Mechanical Parts:**
- MECH-BEARING-001: Ball Bearing Set ($22)
- MECH-GEAR-001: Precision Gear ($35)
- MECH-SHAFT-001: Drive Shaft ($55)
- MECH-BRACKET-001: Mounting Bracket ($15)
- MECH-SPRING-001: Compression Spring ($5)

**Fasteners:**
- HARD-BOLT-001: Hex Bolt M8x50 (100pcs) ($12)
- HARD-NUT-001: Lock Nut M8 (100pcs) ($8)
- HARD-WASHER-001: Washer M8 (100pcs) ($5)
- HARD-SCREW-001: Machine Screw M6 (200pcs) ($10)

**Finishing Materials:**
- FINISH-PAINT-001: Industrial Paint - Black ($35)
- FINISH-PAINT-002: Industrial Paint - Gray ($35)
- FINISH-PRIMER-001: Metal Primer ($28)
- FINISH-COAT-001: Clear Protective Coating ($42)

**Packaging:**
- PKG-BOX-001: Shipping Box Large ($8)
- PKG-FOAM-001: Protective Foam Insert ($12)

Each component includes:
- Unique part code
- Name
- Cost per unit

---

## Workflow

Typical workflow after seeding:

1. **Seed the database** with this script (customers, products, work centers, components)
2. **Create Sales Orders** via frontend (selecting customers, products, work centers)
3. **Generate Planned Orders** from sales orders
4. **Convert to Work Orders** for production
5. **Record Component Usage** during production
6. **Create Deliveries** when orders complete
7. **Generate Invoices** for billing

## Notes

- These entities are typically **read-only** in the application flow
- They are selected/referenced when creating sales orders
- The script is idempotent - you can run it multiple times (records won't duplicate if you don't use --clear)
- Use `--clear` flag with caution as it will delete ALL customers, products, work centers, and components
- The script uses transactions and will rollback on errors

## Database Setup

Full database setup from scratch:

```bash
# 1. Create tables
uv run python scripts/create_db.py

# 2. Seed reference data
uv run python scripts/seed_data.py

# 3. (Optional) Run Alembic migrations if using versioned migrations
alembic upgrade head
```

## Extending the Seed Data

To add more seed data:

1. Edit `seed_data.py`
2. Add entries to the relevant `*_data` list in the seed function
3. Run the script again

Example:
```python
# In seed_customers function, add:
{
    "name": "New Department",
    "email": "new@university.edu",
    "phone": "+1-555-0999",
    "address": "Building X, University Campus",
    "customer_type": CustomerTypes.DEPARTMENT
}
```

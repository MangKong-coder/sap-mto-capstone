# Seed Data Quick Reference

This is a quick reference guide for the seeded data in your MTO system.

## 🏢 Customers (10 total)

### Departments (3)
| ID | Name | Email | Type |
|----|------|-------|------|
| 1 | Engineering Department | engineering@university.edu | DEPARTMENT |
| 2 | Physics Department | physics@university.edu | DEPARTMENT |
| 3 | Computer Science Department | cs@university.edu | DEPARTMENT |

### Campus (2)
| ID | Name | Email | Type |
|----|------|-------|------|
| 4 | Main Campus Facilities | facilities@university.edu | CAMPUS |
| 5 | East Campus | eastcampus@university.edu | CAMPUS |

### Students (3)
| ID | Name | Email | Type |
|----|------|-------|------|
| 6 | Student Project - Team Alpha | team.alpha@student.university.edu | STUDENT |
| 7 | Student Project - Team Beta | team.beta@student.university.edu | STUDENT |
| 8 | Robotics Club | robotics@student.university.edu | STUDENT |

### Vendors (2)
| ID | Name | Email | Type |
|----|------|-------|------|
| 9 | Industrial Equipment Co. | orders@indequip.com | VENDOR |
| 10 | Tech Supply Partners | sales@techsupply.com | VENDOR |

---

## 📦 Products (10 total)

### Custom Machinery
| SKU | Name | Price |
|-----|------|-------|
| MACH-001 | Custom CNC Machine | $25,000.00 |
| MACH-002 | Automated Assembly Line | $150,000.00 |
| MACH-003 | Industrial 3D Printer | $45,000.00 |

### Custom Equipment
| SKU | Name | Price |
|-----|------|-------|
| EQUIP-001 | Laboratory Workstation | $8,500.00 |
| EQUIP-002 | Testing Apparatus | $12,000.00 |
| EQUIP-003 | Robotics Platform | $15,000.00 |

### Electronics
| SKU | Name | Price |
|-----|------|-------|
| ELEC-001 | Custom Control Panel | $3,500.00 |
| ELEC-002 | Sensor Array System | $5,200.00 |

### Furniture
| SKU | Name | Price |
|-----|------|-------|
| FURN-001 | Custom Workbench | $1,200.00 |
| FURN-002 | Laboratory Cabinet System | $2,800.00 |

---

## 🏭 Work Centers (7 total)

| ID | Name | Description |
|----|------|-------------|
| 1 | Main Fabrication | CNC machines and welding |
| 2 | Assembly Line 1 | Large equipment assembly |
| 3 | Assembly Line 2 | Electronics and small components |
| 4 | Testing & QC | Quality control and testing |
| 5 | Precision Machining | High-precision machining |
| 6 | Electronics Workshop | Electronic assembly and programming |
| 7 | Paint & Finishing | Surface treatment |

---

## 🔩 Components (25 total)

### Raw Materials (4)
| Part Code | Name | Cost |
|-----------|------|------|
| MAT-STEEL-001 | Steel Sheet 4x8ft | $125.00 |
| MAT-ALUM-001 | Aluminum Bar 6ft | $85.00 |
| MAT-PLASTIC-001 | ABS Plastic Sheet | $45.00 |
| MAT-WOOD-001 | Hardwood Plank 8ft | $35.00 |

### Electronic Components (6)
| Part Code | Name | Cost |
|-----------|------|------|
| ELEC-MCU-001 | Microcontroller Unit | $12.50 |
| ELEC-SENSOR-001 | Temperature Sensor | $8.00 |
| ELEC-MOTOR-001 | Stepper Motor | $45.00 |
| ELEC-PWR-001 | Power Supply 24V | $65.00 |
| ELEC-RELAY-001 | Industrial Relay | $18.00 |
| ELEC-CABLE-001 | Control Cable 50ft | $25.00 |

### Mechanical Parts (5)
| Part Code | Name | Cost |
|-----------|------|------|
| MECH-BEARING-001 | Ball Bearing Set | $22.00 |
| MECH-GEAR-001 | Precision Gear | $35.00 |
| MECH-SHAFT-001 | Drive Shaft | $55.00 |
| MECH-BRACKET-001 | Mounting Bracket | $15.00 |
| MECH-SPRING-001 | Compression Spring | $5.00 |

### Fasteners (4)
| Part Code | Name | Cost |
|-----------|------|------|
| HARD-BOLT-001 | Hex Bolt M8x50 (100pcs) | $12.00 |
| HARD-NUT-001 | Lock Nut M8 (100pcs) | $8.00 |
| HARD-WASHER-001 | Washer M8 (100pcs) | $5.00 |
| HARD-SCREW-001 | Machine Screw M6 (200pcs) | $10.00 |

### Finishing Materials (4)
| Part Code | Name | Cost |
|-----------|------|------|
| FINISH-PAINT-001 | Industrial Paint - Black | $35.00 |
| FINISH-PAINT-002 | Industrial Paint - Gray | $35.00 |
| FINISH-PRIMER-001 | Metal Primer | $28.00 |
| FINISH-COAT-001 | Clear Protective Coating | $42.00 |

### Packaging (2)
| Part Code | Name | Cost |
|-----------|------|------|
| PKG-BOX-001 | Shipping Box Large | $8.00 |
| PKG-FOAM-001 | Protective Foam Insert | $12.00 |

---

## 💡 Usage Tips

### Creating a Sales Order
When creating a sales order via the frontend, you'll select:
- **Customer**: Choose from the 10 customers above
- **Product**: Choose from the 10 products above  
- **Work Center**: Choose from the 7 work centers above

### Example Order Scenarios

**Scenario 1: Department Order**
- Customer: Engineering Department
- Product: Laboratory Workstation (EQUIP-001)
- Work Center: Assembly Line 2
- Quantity: 5
- Total: $42,500

**Scenario 2: Student Project**
- Customer: Robotics Club
- Product: Robotics Platform (EQUIP-003)
- Work Center: Electronics Workshop
- Quantity: 2
- Total: $30,000

**Scenario 3: Large Campus Order**
- Customer: Main Campus Facilities
- Product: Automated Assembly Line (MACH-002)
- Work Center: Main Fabrication
- Quantity: 1
- Total: $150,000

### Component Usage
When work orders are created, components can be assigned. Example BOM for Custom CNC Machine:
- MAT-STEEL-001 × 3
- ELEC-MCU-001 × 2
- ELEC-MOTOR-001 × 4
- MECH-BEARING-001 × 8
- MECH-GEAR-001 × 6
- Various fasteners and hardware

---

## 🔄 Re-seeding

To reseed the database (careful - this deletes existing data):

```bash
uv run python scripts/seed_data.py --clear
```

To add additional data without clearing:

```bash
uv run python scripts/seed_data.py
```

To verify seeded data:

```bash
uv run python scripts/verify_seed.py
```

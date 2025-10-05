"""
Script to seed the database with initial data for the Mapúa University Bookstore.

This script populates:
- Customers (STUDENTS, FACULTY, DEPARTMENTS, SUPPLIERS)
- Products (books, supplies, merchandise)
- Work Centers (bookstore locations and service areas)
- Components (raw materials and packaging items)

Run with: uv run python scripts/seed_data.py
"""

import sys
from pathlib import Path
from typing import List

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models import Customer, Product, WorkCenter, Component, CustomerTypes
from app.core.logging import logger


def seed_customers(db: Session) -> List[Customer]:
    """Seed customer data for bookstore customers."""
    logger.info("Seeding customers...")

    customers_data = [
        # Students
        {
            "name": "James Domingo",
            "email": "james.domingo@mapua.edu.ph",
            "phone": "+63-912-345-6789",
            "address": "Intramuros Campus, Dorm A-12",
            "customer_type": CustomerTypes.STUDENT,
        },
        {
            "name": "Team Innovate",
            "email": "innovate@student.mapua.edu.ph",
            "phone": "+63-917-223-1122",
            "address": "Makati Campus, Study Hall 2",
            "customer_type": CustomerTypes.STUDENT,
        },
        # Faculty
        {
            "name": "Prof. Maria Dela Cruz",
            "email": "m.delacruz@mapua.edu.ph",
            "phone": "+63-917-334-5566",
            "address": "School of IT, 3rd Floor, North Building",
            "customer_type": CustomerTypes.DEPARTMENT,
        },
        # Departments
        {
            "name": "School of Information Technology",
            "email": "sit@mapua.edu.ph",
            "phone": "+63-2-8230-0030",
            "address": "North Building, Intramuros Campus",
            "customer_type": CustomerTypes.DEPARTMENT,
        },
        {
            "name": "Office of the Registrar",
            "email": "registrar@mapua.edu.ph",
            "phone": "+63-2-8242-9541",
            "address": "Ground Floor, Administration Building",
            "customer_type": CustomerTypes.DEPARTMENT,
        },
        # Suppliers
        {
            "name": "National Book Store Inc.",
            "email": "orders@nationalbookstore.com",
            "phone": "+63-2-8899-1234",
            "address": "Quezon City, Metro Manila",
            "customer_type": CustomerTypes.VENDOR,
        },
        {
            "name": "Mapúa Printing Services",
            "email": "printing@mapua.edu.ph",
            "phone": "+63-2-8234-1122",
            "address": "Basement, Main Building, Intramuros Campus",
            "customer_type": CustomerTypes.VENDOR,
        },
    ]

    customers = [Customer(**data) for data in customers_data]
    db.add_all(customers)
    db.commit()
    logger.info(f"Seeded {len(customers)} customers")
    return customers


def seed_products(db: Session) -> List[Product]:
    """Seed product data for bookstore inventory."""
    logger.info("Seeding products...")

    products_data = [
        # Textbooks
        {"sku": "BOOK-IT101", "name": "Introduction to Computing", "description": "1st Year IT Textbook", "price": 850.00},
        {"sku": "BOOK-MATH201", "name": "Advanced Engineering Mathematics", "description": "Engineering core textbook", "price": 1200.00},
        {"sku": "BOOK-CHEM101", "name": "Basic Chemistry for Engineers", "description": "General chemistry textbook", "price": 980.00},
        # Supplies
        {"sku": "SUP-NOTE001", "name": "Mapúa College Notebook", "description": "80 pages, Mapúa-branded", "price": 65.00},
        {"sku": "SUP-PEN001", "name": "Black Gel Pen", "description": "0.5mm fine tip gel pen", "price": 25.00},
        {"sku": "SUP-CALC001", "name": "Scientific Calculator", "description": "Casio FX-991EX or equivalent", "price": 1650.00},
        {"sku": "SUP-DRAW001", "name": "Engineering Drawing Set", "description": "Contains T-square, triangles, compass", "price": 750.00},
        # Merchandise
        {"sku": "MERCH-TSHIRT", "name": "Mapúa University Shirt", "description": "Cotton t-shirt with Mapúa logo", "price": 450.00},
        {"sku": "MERCH-HOODIE", "name": "Mapúa Hoodie", "description": "Fleece hoodie, university logo printed", "price": 900.00},
        {"sku": "MERCH-TOTE", "name": "Canvas Tote Bag", "description": "Reusable tote with Mapúa print", "price": 250.00},
    ]

    products = [Product(**data) for data in products_data]
    db.add_all(products)
    db.commit()
    logger.info(f"Seeded {len(products)} products")
    return products


def seed_work_centers(db: Session) -> List[WorkCenter]:
    """Seed work centers (bookstore branches or service areas)."""
    logger.info("Seeding work centers...")

    work_centers_data = [
        {
            "name": "Main Bookstore - Intramuros",
            "description": "Main campus bookstore handling student and faculty sales.",
            "address": "Ground Floor, North Building, Intramuros Campus",
        },
        {
            "name": "Bookstore - Makati Extension",
            "description": "Smaller branch servicing Makati campus students.",
            "address": "2nd Floor, Makati Campus Lobby",
        },
        {
            "name": "Online Order Fulfillment Center",
            "description": "Handles packing and delivery for online bookstore orders.",
            "address": "Basement, Administration Building, Intramuros",
        },
    ]

    work_centers = [WorkCenter(**data) for data in work_centers_data]
    db.add_all(work_centers)
    db.commit()
    logger.info(f"Seeded {len(work_centers)} work centers")
    return work_centers


def seed_components(db: Session) -> List[Component]:
    """Seed raw materials and consumables."""
    logger.info("Seeding components...")

    components_data = [
        {"part_code": "COMP-PAPER-A4", "name": "A4 Printing Paper (500s)", "cost": 230.00},
        {"part_code": "COMP-INK-BLACK", "name": "Printer Ink - Black Cartridge", "cost": 420.00},
        {"part_code": "COMP-INK-COLOR", "name": "Printer Ink - Color Cartridge", "cost": 450.00},
        {"part_code": "COMP-BIND-SPIRAL", "name": "Spiral Binding Coil", "cost": 5.00},
        {"part_code": "COMP-COVER-PLASTIC", "name": "Plastic Book Cover Roll", "cost": 35.00},
        {"part_code": "COMP-BOX-SM", "name": "Small Packaging Box", "cost": 15.00},
        {"part_code": "COMP-BOX-LG", "name": "Large Packaging Box", "cost": 30.00},
        {"part_code": "COMP-STICKER-LBL", "name": "Price Label Stickers (Sheet)", "cost": 12.00},
    ]

    components = [Component(**data) for data in components_data]
    db.add_all(components)
    db.commit()
    logger.info(f"Seeded {len(components)} components")
    return components


def clear_existing_data(db: Session) -> None:
    """Clear existing seed data."""
    logger.warning("Clearing existing seed data...")
    try:
        db.query(Component).delete()
        db.query(WorkCenter).delete()
        db.query(Product).delete()
        db.query(Customer).delete()
        db.commit()
        logger.info("Existing data cleared")
    except Exception as e:
        logger.error(f"Error clearing data: {e}")
        db.rollback()
        raise


def seed_all(clear_first: bool = False) -> None:
    """Run all seeders."""
    db: Session = SessionLocal()

    try:
        if clear_first:
            clear_existing_data(db)

        logger.info("Starting bookstore seeding...")
        customers = seed_customers(db)
        products = seed_products(db)
        work_centers = seed_work_centers(db)
        components = seed_components(db)

        logger.info("=" * 60)
        logger.info("Mapúa University Bookstore database seeding completed successfully!")
        logger.info("=" * 60)
        logger.info(f"Seeded {len(customers)} customers")
        logger.info(f"Seeded {len(products)} products")
        logger.info(f"Seeded {len(work_centers)} work centers")
        logger.info(f"Seeded {len(components)} components")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Seed database with Mapúa University Bookstore data")
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Clear existing data before seeding (WARNING: This will delete all customers, products, work centers, and components)",
    )

    args = parser.parse_args()

    if args.clear:
        logger.warning("=" * 60)
        logger.warning("WARNING: This will delete all existing seed data!")
        logger.warning("=" * 60)
        response = input("Are you sure you want to continue? (yes/no): ")
        if response.lower() != "yes":
            logger.info("Seeding cancelled")
            sys.exit(0)

    seed_all(clear_first=args.clear)

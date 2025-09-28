from typing import Optional, List
from sqlmodel import Session, select, func, and_, or_, col
from app.models import Products
from app.schemas.products import ProductCreate, ProductUpdate


def get_products(
    session: Session,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    is_active: Optional[bool] = None
) -> tuple[List[Products], int]:
    """
    Get products with pagination and optional filtering
    
    Args:
        session: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        search: Search term to filter by name, sku, or description
        is_active: Filter by active status
        
    Returns:
        Tuple of (products_list, total_count)
    """
    # Build base query
    query = select(Products)
    count_query = select(func.count())
    
    # Apply filters
    conditions = []
    
    if search:
        search_filter = or_(
            col(Products.name).ilike(f"%{search}%"),
            col(Products.sku).ilike(f"%{search}%"),
            col(Products.description).ilike(f"%{search}%")
        )
        conditions.append(search_filter)
    
    if is_active is not None:
        conditions.append(Products.is_active == is_active)
    
    if conditions:
        filter_condition = and_(*conditions)
        query = query.where(filter_condition)
        count_query = count_query.where(filter_condition)
    
    # Get total count
    total = session.exec(count_query).one()
    
    # Apply pagination and ordering
    query = query.offset(skip).limit(limit)
    
    # Execute query
    products = list(session.exec(query).all())
    
    return products, total


def get_product_by_id(session: Session, product_id: int) -> Optional[Products]:
    """
    Get a product by its ID
    
    Args:
        session: Database session
        product_id: Products ID
        
    Returns:
        Products instance or None if not found
    """
    return session.get(Products, product_id)


def get_product_by_sku(session: Session, sku: str) -> Optional[Products]:
    """
    Get a product by its SKU
    
    Args:
        session: Database session
        sku: Products SKU
        
    Returns:
        Products instance or None if not found
    """
    statement = select(Products).where(Products.sku == sku)
    return session.exec(statement).first()


def create_product(session: Session, product_data: ProductCreate) -> Products:
    """
    Create a new product
    
    Args:
        session: Database session
        product_data: Products creation data
        
    Returns:
        Created product instance
    """
    product = Products(**product_data.model_dump())
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


def update_product(
    session: Session, 
    product_id: int, 
    product_data: ProductUpdate
) -> Optional[Products]:
    """
    Update an existing product
    
    Args:
        session: Database session
        product_id: Products ID to update
        product_data: Products update data
        
    Returns:
        Updated product instance or None if not found
    """
    product = session.get(Products, product_id)
    if not product:
        return None
    
    # Update only fields that were provided
    update_data = product_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


def delete_product(session: Session, product_id: int) -> bool:
    """
    Soft delete a product (set is_active to False)
    
    Args:
        session: Database session
        product_id: Products ID to delete
        
    Returns:
        True if product was found and deleted, False otherwise
    """
    product = session.get(Products, product_id)
    if not product:
        return False
    
    product.is_active = False
    session.add(product)
    session.commit()
    return True


def hard_delete_product(session: Session, product_id: int) -> bool:
    """
    Permanently delete a product from the database
    
    Args:
        session: Database session
        product_id: Products ID to delete
        
    Returns:
        True if product was found and deleted, False otherwise
    """
    product = session.get(Products, product_id)
    if not product:
        return False
    
    session.delete(product)
    session.commit()
    return True


def get_active_products(session: Session, limit: int = 100) -> List[Products]:
    """
    Get all active products
    
    Args:
        session: Database session
        limit: Maximum number of products to return
        
    Returns:
        List of active products
    """
    statement = select(Products).where(Products.is_active == True).limit(limit)
    return list(session.exec(statement).all())


def search_products(session: Session, search_term: str, limit: int = 50) -> List[Products]:
    """
    Search products by name, SKU, or description
    
    Args:
        session: Database session
        search_term: Term to search for
        limit: Maximum number of results
        
    Returns:
        List of matching products
    """
    search_filter = or_(
        col(Products.name).ilike(f"%{search_term}%"),
        col(Products.sku).ilike(f"%{search_term}%"),
        col(Products.description).ilike(f"%{search_term}%")
    )
    
    statement = (
        select(Products)
        .where(and_(Products.is_active == True, search_filter))
        .order_by(Products.name)
        .limit(limit)
    )
    
    return list(session.exec(statement).all())
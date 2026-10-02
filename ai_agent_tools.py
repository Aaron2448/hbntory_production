from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Item, Category

engine = create_engine("sqlite:///hbntory.db", echo=False)
SessionLocal = sessionmaker(bind=engine)

def search_inventory_by_keyword(keyword: str):
    """
    Searches inventory items by name or SKU containing the keyword.
    Acts as a tool function for AI query handling.
    """
    session = SessionLocal()
    try:
        query_pattern = f"%{keyword}%"
        items = session.query(Item).filter(
            (Item.name.ilike(query_pattern)) | (Item.sku.ilike(query_pattern))
        ).all()
        
        if not items:
            return f"No inventory items found matching keyword: '{keyword}'"
        
        results = []
        for item in items:
            results.append({
                "sku": item.sku,
                "name": item.name,
                "unit_price": item.unit_price,
                "category": item.category.name
            })
        return results
    finally:
        session.close()

def get_full_inventory_summary():
    """
    Retrieves a complete summary of all inventory items and categories.
    """
    session = SessionLocal()
    try:
        items = session.query(Item).all()
        return [
            {
                "sku": item.sku,
                "name": item.name,
                "unit_price": item.unit_price,
                "category": item.category.name
            }
            for item in items
        ]
    finally:
        session.close()

if __name__ == "__main__":
    # Local verification block
    print("Testing AI inventory search tool...")
    print(search_inventory_by_keyword("Wi-Fi"))

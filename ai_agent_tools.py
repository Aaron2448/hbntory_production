from sqlalchemy.orm import joinedload

from database import SessionLocal
from models import Category, Item


def search_inventory_by_keyword(keyword: str):
    session = SessionLocal()
    try:
        query_pattern = f"%{keyword}%"
        items = (
            session.query(Item)
            .join(Category)
            .options(joinedload(Item.category))
            .filter(
                Item.name.ilike(query_pattern)
                | Item.sku.ilike(query_pattern)
                | Category.name.ilike(query_pattern)
            )
            .all()
        )

        if not items:
            return f"No inventory items found matching keyword: '{keyword}'"

        return [
            {
                "sku": item.sku,
                "name": item.name,
                "unit_price": item.unit_price,
                "category": item.category.name,
            }
            for item in items
        ]
    finally:
        session.close()


def get_full_inventory_summary():
    session = SessionLocal()
    try:
        items = session.query(Item).options(joinedload(Item.category)).all()
        return [
            {
                "sku": item.sku,
                "name": item.name,
                "unit_price": item.unit_price,
                "category": item.category.name,
            }
            for item in items
        ]
    finally:
        session.close()


if __name__ == "__main__":
    print("Testing AI inventory search tool...")
    print(search_inventory_by_keyword("Wi-Fi"))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Category, Item

# 1. Connect to our local SQLite database
engine = create_engine("sqlite:///hbntory.db", echo=False)

# 2. Create a configured "Session" class to handle database transactions
SessionLocal = sessionmaker(bind=engine)

def seed_data():
    # Open a new database session (like opening a transaction block)
    session = SessionLocal()

    try:
        # Check if data already exists to avoid duplicate entry errors
        existing_category = session.query(Category).filter_by(name="Electronics").first()
        if existing_category:
            print("Seed data already exists. Skipping insertion.")
            return

        print("Seeding database with initial inventory...")

        # Create a Category instance
        electronics = Category(
            name="Electronics", 
            description="Hardware devices, components, and networking tools"
        )

        # Create Item instances linked to this category
        item1 = Item(
            sku="MOCK-WIFI-01", 
            name="5G Portable Wi-Fi Router", 
            unit_price=149.99, 
            category=electronics
        )
        
        item2 = Item(
            sku="MOCK-CABLE-06", 
            name="Cat 6 Ethernet Cable 10m", 
            unit_price=24.50, 
            category=electronics
        )

        # Add records to the session and commit changes to disk
        session.add(electronics)
        session.add(item1)
        session.add(item2)
        session.commit()
        
        print("Data successfully seeded!")

    except Exception as e:
        session.rollback()
        print(f"An error occurred during seeding: {e}")
    finally:
        session.close()

def query_inventory():
    session = SessionLocal()
    
    print("\n--- Querying Inventory Database ---")
    
    # Query all items and utilize ORM relationship mapping to access category data
    items = session.query(Item).all()
    
    for item in items:
        print(f"SKU: {item.sku} | Name: {item.name} | Price: ${item.unit_price:.2f} | Category: {item.category.name}")

    session.close()

if __name__ == "__main__":
    seed_data()
    query_inventory()

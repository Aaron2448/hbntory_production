from passlib.context import CryptContext

from database import SessionLocal
from models import Category, Item, User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def seed_admin():
    session = SessionLocal()
    try:
        if session.query(User).filter_by(username="admin").first():
            print("Admin user already exists. Skipping.")
            return
        password = "admin123"[:72]
        session.add(
            User(
                username="admin",
                hashed_password=pwd_context.hash(password),
            )
        )
        session.commit()
        print("Seeded admin user (admin / admin123).")
    except Exception as exc:
        session.rollback()
        print(f"An error occurred while seeding admin: {exc}")
        raise
    finally:
        session.close()


def seed_data():
    session = SessionLocal()
    try:
        existing_category = session.query(Category).filter_by(name="Electronics").first()
        if existing_category:
            print("Seed data already exists. Skipping insertion.")
            return

        print("Seeding database with initial inventory...")
        electronics = Category(
            name="Electronics",
            description="Hardware devices, components, and networking tools",
        )
        session.add_all(
            [
                electronics,
                Item(
                    sku="MOCK-WIFI-01",
                    name="5G Portable Wi-Fi Router",
                    unit_price=149.99,
                    category=electronics,
                ),
                Item(
                    sku="MOCK-CABLE-06",
                    name="Cat 6 Ethernet Cable 10m",
                    unit_price=24.50,
                    category=electronics,
                ),
            ]
        )
        session.commit()
        print("Data successfully seeded!")
    except Exception as exc:
        session.rollback()
        print(f"An error occurred during seeding: {exc}")
        raise
    finally:
        session.close()


def query_inventory():
    session = SessionLocal()
    try:
        print("\n--- Querying Inventory Database ---")
        items = session.query(Item).all()
        for item in items:
            print(
                f"SKU: {item.sku} | Name: {item.name} | "
                f"Price: ${item.unit_price:.2f} | Category: {item.category.name}"
            )
    finally:
        session.close()


if __name__ == "__main__":
    seed_admin()
    seed_data()
    query_inventory()

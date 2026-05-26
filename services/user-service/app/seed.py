from __future__ import annotations
from app.core.database import Base, SessionLocal, engine
from app.models import Role
from app.repositories import UserRepository
from app.schemas import UserCreate

USERS = [
    ('admin@astracart.dev','Astra Admin','AdminPass123!',Role.ADMIN),
    ('seller1@astracart.dev','Mira Seller','SellerPass123!',Role.SELLER),
    ('seller2@astracart.dev','Arjun Seller','SellerPass123!',Role.SELLER),
    ('customer1@astracart.dev','Nia Customer','CustomerPass123!',Role.CUSTOMER),
    ('customer2@astracart.dev','Kabir Customer','CustomerPass123!',Role.CUSTOMER),
    ('support@astracart.dev','Isha Support','SupportPass123!',Role.SUPPORT),
]

def main():
    Base.metadata.create_all(bind=engine, checkfirst=True)
    db = SessionLocal()
    repo = UserRepository(db)
    for email, name, password, role in USERS:
        if not repo.by_email(email):
            repo.create(UserCreate(email=email, full_name=name, password=password, role=role))
    db.close()
    print('Seeded user service with demo accounts')

if __name__ == '__main__':
    main()

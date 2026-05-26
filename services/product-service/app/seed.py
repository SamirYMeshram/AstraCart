from __future__ import annotations
from random import randint, uniform, choice
from app.core.database import Base, SessionLocal, engine
from app.repositories import CategoryRepository, ProductRepository
from app.schemas import CategoryCreate, ProductCreate

CATEGORIES = [
    ('Electronics','electronics','Devices, gadgets and smart accessories','Cpu'),
    ('Fashion','fashion','Premium apparel and accessories','Shirt'),
    ('Home Studio','home-studio','Home office and studio gear','Home'),
    ('Fitness','fitness','Wearables and training equipment','Dumbbell'),
    ('Beauty','beauty','Cosmetics and grooming essentials','Sparkles'),
    ('Books','books','Curated books and learning material','BookOpen'),
    ('Gaming','gaming','Consoles, peripherals and esports gear','Gamepad2'),
    ('Travel','travel','Bags and mobility essentials','Plane'),
]
NAMES = ['Aurora','Nova','Pulse','Vertex','Luxe','Orbit','Quantum','Nimbus','Atlas','Prism','Vanta','Halo','Aero','Drift','Flux','Prime','Echo','Zen','Cobalt','Ember']
TYPES = ['Wireless Headphones','Smart Backpack','Ergo Chair','Mechanical Keyboard','Hydration Bottle','LED Desk Lamp','Running Shoes','Travel Case','Gaming Mouse','Skin Serum']

def main():
    Base.metadata.create_all(bind=engine, checkfirst=True)
    db = SessionLocal(); cats = []
    cat_repo = CategoryRepository(db); prod_repo = ProductRepository(db)
    for name, slug, desc, icon in CATEGORIES:
        cat = cat_repo.by_slug(slug) or cat_repo.create(CategoryCreate(name=name, slug=slug, description=desc, icon=icon))
        cats.append(cat)
    for i in range(50):
        title = f'{choice(NAMES)} {choice(TYPES)} {i+1:02d}'
        slug = title.lower().replace(' ', '-')
        if prod_repo.by_slug(slug): continue
        price = round(uniform(29, 799), 2)
        stock = [0,1,2,3,4,5,12,25,50,99][i % 10]
        prod_repo.create(ProductCreate(
            title=title, slug=slug, description=f'{title} with premium materials, fast delivery, enterprise-grade inventory tracking and startup-grade catalog polish.',
            price=price, discount_price=round(price*0.85,2) if i % 3 == 0 else None, stock_quantity=stock, category_id=choice(cats).id,
            seller_id='seller-demo-1' if i % 2 else 'seller-demo-2', images=[f'https://images.unsplash.com/photo-15{i:08d}?auto=format&fit=crop&w=900&q=80'],
            rating=round(uniform(3.8,5.0),1), sku=f'ASTRA-{i+1:04d}'
        ), seller_id='seller-demo-1' if i % 2 else 'seller-demo-2')
    db.close(); print('Seeded product service with 8 categories and 50 products')
if __name__ == '__main__': main()

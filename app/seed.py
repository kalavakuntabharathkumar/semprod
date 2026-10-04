from sqlalchemy.orm import Session
from .models import Product

SEED = [
 ("TrailFlex Running Shoes", "Footwear", "Lightweight breathable running shoes with cushioned support for trails and daily workouts.", 79.0, "running trail breathable fitness"),
 ("CloudStep Walking Sneakers", "Footwear", "Comfortable everyday sneakers with soft foam cushioning for long city walks.", 64.0, "walking comfort sneakers casual"),
 ("Summit 28L Hiking Backpack", "Outdoor", "Weather-resistant daypack with padded straps, hydration pocket, and trail storage.", 89.0, "hiking backpack outdoor travel"),
 ("HydroSteel Insulated Bottle", "Outdoor", "Double-wall stainless steel bottle keeps drinks cold during exercise and commuting.", 25.0, "water bottle reusable gym"),
 ("PulseFit Smart Watch", "Electronics", "Fitness watch with heart-rate tracking, sleep insights, GPS workouts, and notifications.", 129.0, "smartwatch fitness gps wearable"),
 ("Studio Wireless Headphones", "Electronics", "Over-ear wireless headphones with active noise reduction and long battery life.", 119.0, "audio headphones wireless music"),
 ("ErgoMesh Office Chair", "Home Office", "Adjustable ergonomic chair with breathable mesh back and lumbar support for desk work.", 249.0, "chair ergonomic office desk"),
 ("Mechanical Keyboard Compact", "Electronics", "Compact mechanical keyboard with tactile switches for coding and productivity.", 75.0, "keyboard typing computer developer"),
 ("Everyday Cotton Hoodie", "Clothing", "Soft cotton-blend hoodie with a relaxed fit for layering in cool weather.", 42.0, "hoodie cotton casual clothing"),
 ("Insulated Travel Mug", "Kitchen", "Leak-resistant travel mug with a secure lid for hot coffee on the commute.", 22.0, "coffee mug travel insulated"),
 ("Yoga Mat Grip Pro", "Fitness", "Non-slip exercise mat with comfortable cushioning for yoga, stretching, and home workouts.", 36.0, "yoga mat workout fitness"),
 ("USB-C Fast Charger", "Electronics", "Compact USB-C wall charger with fast charging support for compatible devices.", 29.0, "charger usb c electronics mobile"),
]

def seed_products(db: Session):
    if db.query(Product).count() == 0:
        db.add_all([Product(name=n, category=c, description=d, price=price, tags=tags) for n,c,d,price,tags in SEED])
        db.commit()

from app.db.database import Base

# Import all models here to ensure they are registered with the Base
from app.models.base_model import Base
from app.models.user import User
from app.models.customer import Customer
from app.models.supplier import Supplier
from app.models.category import Category
from app.models.inventory_item import InventoryItem
from app.models.inventory_movement import InventoryMovement
from app.models.transaction import Transaction

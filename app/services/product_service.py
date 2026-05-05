from uuid import uuid4
from datetime import datetime
from typing import List
from ..domain.models import Product
from ..domain.repositories import ProductRepository
from ..utils.exceptions import ValidationError, NotFoundError

class ProductService:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    def create_product(self, name: str, calories_per_unit: int) -> Product:
        if not name.strip():
            raise ValidationError("Название продукта не может быть пустым")
        if calories_per_unit <= 0:
            raise ValidationError("Калорийность должна быть положительным числом")
        # Проверка уникальности
        existing = self.product_repo.get_by_name(name)
        if existing:
            raise ValidationError(f"Продукт с именем '{name}' уже существует")
        product = Product(
            id=uuid4(),
            name=name.strip(),
            calories_per_unit=calories_per_unit,
            created_at=datetime.utcnow()
        )
        self.product_repo.add(product)
        return product

    def get_all_products(self) -> List[Product]:
        return self.product_repo.get_all()

    def update_product(self, product_id: UUID, name: str, calories_per_unit: int) -> Product:
        product = self.product_repo.get_by_id(product_id)
        if not product:
            raise NotFoundError("Продукт не найден")
        # Проверка уникальности имени, исключая текущий
        existing = self.product_repo.get_by_name(name)
        if existing and existing.id != product_id:
            raise ValidationError(f"Продукт с именем '{name}' уже существует")
        product.name = name.strip()
        product.calories_per_unit = calories_per_unit
        self.product_repo.update(product)
        return product

    def delete_product(self, product_id: UUID) -> None:
        product = self.product_repo.get_by_id(product_id)
        if not product:
            raise NotFoundError("Продукт не найден")
        self.product_repo.delete(product_id)
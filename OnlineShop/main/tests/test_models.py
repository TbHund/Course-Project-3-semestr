from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from main.models import Size, Category, ClothingItem, ClothingItemSize, ItemImage

class SizeModelTest(TestCase):
    def setUp(self):
        self.size = Size.objects.create(name="M")

    def test_size_creation(self):
        self.assertEqual(Size.objects.count(), 1)
        self.assertEqual(self.size.name, "M")

    def test_str_representation(self):
        self.assertEqual(str(self.size), "M")

    def test_to_dict(self):
        self.assertEqual(self.size.to_dict(), {
            'id': self.size.id,
            'name': 'M',
            'class_name': 'Size'
        })

    def test_unique_name(self):
        with self.assertRaises(Exception):
            Size.objects.create(name="M")



class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="T-Shirts",
            slug="t-shirts"
        )

    def test_to_dict(self):
        ClothingItem.objects.create(
            name="Test Item",
            slug="test-item",
            category=self.category,
            price=100,
            discount=0 
        )
        data = self.category.to_dict()
        self.assertEqual(data['name'], "T-Shirts")
        self.assertEqual(data['item_count'], 1)

    def test_get_item_count(self):
        ClothingItem.objects.bulk_create([
            ClothingItem(
                name=f"Item {i}", 
                slug=f"item-{i}", 
                category=self.category, 
                price=100,
                discount=0 
            ) for i in range(3)
        ])
        self.assertEqual(self.category.get_item_count(), 3)



class ClothingItemModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="T-Shirts",
            slug="t-shirts"
        )
        self.size = Size.objects.create(name="M")
        self.item = ClothingItem.objects.create(
            name="Summer T-Shirt",
            slug="summer-t-shirt",
            category=self.category,
            price=Decimal('29.99'),
            discount=Decimal('10.00')
        )
        self.item.sizes.add(self.size)

    def test_item_creation(self):
        self.assertEqual(self.item.name, "Summer T-Shirt")
        self.assertEqual(self.item.price, Decimal('29.99'))

    def test_str_representation(self):
        self.assertEqual(str(self.item), "Summer T-Shirt")

    def test_get_price_with_discount(self):
        self.assertAlmostEqual(
            float(self.item.get_price_with_discount()),
            float(Decimal('26.991')),
            places=2
        )

        self.item.discount = Decimal('0.00')
        self.assertEqual(self.item.get_price_with_discount(), Decimal('29.99'))

    def test_to_dict(self):
        data = self.item.to_dict()
        self.assertEqual(data['name'], "Summer T-Shirt")
        self.assertEqual(data['price'], 29.99)
        self.assertEqual(len(data['sizes']), 1)
        self.assertEqual(data['sizes'][0]['size']['name'], "M")

    def test_price_validation(self):
        item = ClothingItem(
            name="Invalid",
            slug="invalid",
            category=self.category,
            price=Decimal('-10.00')
        )
        with self.assertRaises(ValidationError):
            item.full_clean()

    def test_auto_timestamps(self):
        self.assertIsNotNone(self.item.created_at)
        self.assertIsNotNone(self.item.updated_at)



class ClothingItemSizeModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test", slug="test")
        self.item = ClothingItem.objects.create(
            name="Test Item",
            slug="test-item",
            category=self.category,
            price=100,
            discount=0  
        )
        self.size = Size.objects.create(name="L")
        self.item_size = ClothingItemSize.objects.create(
            clothing_item=self.item,
            size=self.size,
            available=True
        )



class ItemImageModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test", slug="test")
        self.item = ClothingItem.objects.create(
            name="Test Item",
            slug="test-item",
            category=self.category,
            price=100,
            discount=0 
        )
        self.image = ItemImage.objects.create(
            product=self.item,
            image="test.jpg"
        )
from django.db import models


class Size(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'class_name': 'Size' 
        }


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'item_count': self.get_item_count(),  
            'class_name': 'Category'  
        }

    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['name'])]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_item_count(self):
        return ClothingItem.objects.filter(category = self).count()


class ClothingItem(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    available = models.BooleanField(default=True)
    sizes = models.ManyToManyField(Size, through='ClothingItemSize',
                                   related_name='clothing_item', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='clothing_items')
    image = models.ImageField(upload_to='product/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name
    
    def get_price_with_discount(self):
        if self.discount > 0:
            return self.price * (1 - (self.discount / 100))
        return self.price
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "available": self.available,
            "sizes": [cis.to_dict() for cis in self.clothingitemsize_set.all()],
            "category": self.category.to_dict() if self.category else None,
            "images": [img.to_dict() for img in self.images.all()],
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "price": float(self.price),
            "discount": float(self.discount),
            "price_with_discount": float(self.get_price_with_discount())
        }
    

class ClothingItemSize(models.Model):
    clothing_item = models.ForeignKey(ClothingItem, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)

    class Meta:
        unique_together = ('clothing_item', 'size')

    def to_dict(self):
        return {
            "size": self.size.to_dict() if self.size else None,
            "available": self.available
        }


class ItemImage(models.Model):
    product = models.ForeignKey(ClothingItem, related_name='images',
                                on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product/%Y/%m/%d', blank=True)

    
    def __str__(self):
        return f'{self.product.name} - {self.image.name}'
    
    def to_dict(self):
        return {
            "image_url": self.image.url if self.image else None,
            "filename": self.image.name
        }
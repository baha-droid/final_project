from django.db import models

from django.db import models

class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class CarModel(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='models')
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.brand.name} {self.name}"

class Car(models.Model):
    TYPE_CHOICES = [
        ('Легковой', 'Легковой'),
        ('Внедорожник', 'Внедорожник'),
        ('Электромобиль', 'Электромобиль'),
        ('JDM', 'JDM')
    ]

    model = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name='cars')
    year = models.PositiveIntegerField()
    price = models.PositiveIntegerField(help_text='Цена в сoмах')
    car_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.model.brand.name} {self.model.name} {self.year}"


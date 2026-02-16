from django.db import models
from django.contrib.postgres.fields import ArrayField


class Product(models.Model):
	title = models.CharField(
		max_length=500,
		null=True,
		blank=True
		)
	color = models.CharField(
		max_length=50,
		null=True,
		blank=True
		)
	memory_size = models.IntegerField(
		null=True,
		blank=True
		)
	memory_unit = models.CharField(
		max_length=10,
		null=True,
		blank=True
		)
	manufacturer = models.CharField(
		max_length=50,
		null=True,
		blank=True
		)
	price = models.IntegerField(
		null=True,
		blank=True
		)
	price_discount = models.IntegerField(
		null=True,
		blank=True
		)
	img_url = ArrayField(
		models.URLField(max_length=500),
		null=True,
		blank=True
		)
	product_code = models.CharField(
		max_length=200,
		null=True,
		blank=True
		)
	review_count = models.IntegerField(
		null=True,
		blank=True
		)
	screen_diagonal = models.CharField(
		max_length=50,
		null=True,
		blank=True
		)
	display_resolution = models.CharField(
		max_length=100,
		null=True,
		blank=True
		)
	characteristics = models.JSONField(
		null=True,
		blank=True
		)

	class Meta:
		ordering = ['title']

	def __str__(self):
		return f"Title:{self.title}"
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


class FAQCategory(models.Model):
    name = models.CharField(max_length=150)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "FAQ Category"
        verbose_name_plural = "FAQ Categories"

    def __str__(self):
        return self.name


class FAQItem(models.Model):
    category = models.ForeignKey(FAQCategory, on_delete=models.CASCADE, related_name="items")
    question = models.CharField(max_length=300)
    answer = CKEditor5Field(config_name="default")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "FAQ Item"

    def __str__(self):
        return self.question

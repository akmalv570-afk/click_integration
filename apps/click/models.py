from django.db import models
from django.utils.timezone import now

# Create your models here.


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "P", "Kutilmoqda"
        PAID = "paid", "To'langan"
        CANCELED = "canceled", "Bekor qilingan"


    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Buyurtma summasi"
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="Buyurtma holati"
    )

    created_at = models.DateTimeField(
        default=now,
        verbose_name="Yaratilgan vaqti"
    )

    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"

    def __str__(self):
        return f"Buyurtma {self.id} - {self.total_price} UZS ({self.status})"


class ClickPayment(models.Model):
    class Status(models.TextChoices):
        PROCESSING = "processing", "Jarayonda"
        CONFIRMED = "confirmed", "Muvaffaqiyatli"
        REJECTED = "rejected", "Bekor qilingan"
        CANCELED = "canceled", "Xatolik tufayli rad etilgan"

    order = models.ForeignKey(
        Order,
        on_delete=models.PROTECT,
        related_name="payments",
        verbose_name="Buyurtma"
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="To'lov summasi"
    )

    click_trans_id = models.CharField(
        max_length=255,
        unique=True,
        blank=True,
        null=True,
        verbose_name="Click Tranzaksiya ID"
    )

    click_paydoc_id = models.CharField(
        max_length=255,
        unique=True,
        blank=True,
        null=True,
        verbose_name="Click To'lov Hujjati ID"
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PROCESSING,
        verbose_name="Status"
    )

    created_at = models.DateTimeField(
        default=now,
        verbose_name="Yaratilgan vaqti"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name = "Click To'lovi"
        verbose_name_plural = "Click To'lovlari"

    def __str__(self):
        return f"To'lov {self.id} (Buyurtma {self.order.id}) - {self.status}"

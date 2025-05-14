from django.db import models
from typing import TYPE_CHECKING

from product.utils import carry


class SoftSlide(models.Model):
    height = models.IntegerField(default=0)
    width = models.IntegerField(default=0)
    cols = models.IntegerField(default=0)

    mirror: "SoftSlideMirror" = models.ForeignKey(
        "SoftSlideMirror", on_delete=models.SET_NULL, null=True, blank=True
    )

    plaid = models.BooleanField(default=False)
    plaid_type = models.IntegerField(choices=[
        (1, "Standard"),
        (2, "Vertikal"),
        (3, "Vertikal + Gorizantal")
    ], null=True,blank=True)

    castle = models.BooleanField(default=False)
    castle_pos = models.IntegerField(
        choices=[(1, "O'rtada"), (2, "Ikki chetda")], default=1
    )
    castle_sides = models.BooleanField(default=False)

    dye: "SoftSlideDye" = models.ForeignKey(
        "SoftSlideDye", on_delete=models.SET_NULL, null=True, blank=True
    )

    price = models.BigIntegerField(default=0)

    def calc_price(self):
        elements = SoftSlideElement.objects.all()
        prices = {e.name: e.calc_price(self) for e in elements}

        prices["Oyna"] = self.mirror.calc_price(self)
        prices["Kraska"] = self.dye.calc_price(self)

        total = sum(list(prices.values()))
        comiss = (total / 100) * 11

        self.price = int(total + comiss)
        return prices


class SoftSlideElement(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0)
    unit = models.CharField(max_length=255, null=True, blank=True)
    formula = models.CharField(max_length=255)

    def calc_price(self, temp: "SoftSlide"):
        lcs = {
            "n": self.price,
            "e": temp.width / 1000,
            "b": temp.height / 1000,
            "r": temp.cols,
            "s": (temp.width / 1000) * (temp.height / 1000),
            "d": temp.castle_pos,
            "sh": temp.plaid,
            "c": temp.castle,
            "carry": carry,
        }

        exec(self.formula, lcs, lcs)
        print(f"{self.name}: {lcs['res']}")
        return lcs["res"]


class SoftSlideMirror(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0)
    unit = models.CharField(max_length=255, null=True, blank=True)
    formula = models.CharField(max_length=255, default="res=s*n")

    def calc_price(self, temp: "SoftSlide"):
        lcs = {
            "n": self.price,
            "e": temp.width / 1000,
            "b": temp.height / 1000,
            "r": temp.cols,
            "s": (temp.width / 1000) * (temp.height / 1000),
            "d": temp.castle_pos,
            "sh": temp.plaid,
            "c": temp.castle,
            "carry": carry,
        }

        exec(self.formula, lcs, lcs)
        print(f"{self.name}: {lcs['res']}")
        return lcs["res"]


class SoftSlideDye(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0)
    unit = models.CharField(max_length=255, null=True, blank=True)
    formula = models.CharField(max_length=255, default="res=s*n")

    def calc_price(self, temp: "SoftSlide"):
        lcs = {
            "n": self.price,
            "e": temp.width / 1000,
            "b": temp.height / 1000,
            "r": temp.cols,
            "s": (temp.width / 1000) * (temp.height / 1000),
            "d": temp.castle_pos,
            "sh": temp.plaid,
            "c": temp.castle,
            "carry": carry,
        }

        exec(self.formula, lcs, lcs)
        print(f"{self.name}: {lcs['res']}")
        return lcs["res"]
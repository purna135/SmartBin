from email.policy import default
from gc import garbage
from django.db import models

# Create your models here.


class Bin(models.Model):
    id = models.AutoField(auto_created = True, primary_key = True)
    name = models.CharField(max_length=100)
    height = models.DecimalField(max_digits=6, decimal_places=2)
    garbage_level = models.DecimalField(max_digits=5, decimal_places=2, default=0, null=True, blank=True)
    location = models.CharField(max_length=200)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return self.name


class Garbage(models.Model):
    bin_id = models.ForeignKey(Bin, on_delete=models.CASCADE)
    garbage_level = models.IntegerField()
    garbage_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.bin_id.name)

    def save(self, *args, **kwargs):
        bin = Bin.objects.get(id = self.bin_id.id)
        garbage_percentage = (self.garbage_level/bin.height) * 100

        bin.garbage_level = garbage_percentage
        bin.save(update_fields=["garbage_level"])

        self.garbage_percentage = garbage_percentage
        super().save(*args, **kwargs)
    
    def to_dict(self):
        return {
            "Bin ID": self.bin_id.id,
            "Bin Name": self.bin_id.name,
            "Date": self.date.date(),
            "Time": self.date.time(),
            "Garbage Level": self.garbage_level,
            "Garbage Percentage": self.garbage_percentage,
        }
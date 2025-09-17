from django.db import models

class Member(models.Model):
    fname = models.CharField(max_length=255, verbose_name="Firstname")
    lname = models.CharField(max_length=255, verbose_name="Lastname")
    email = models.CharField(null=True)
    phone = models.CharField(max_length=12, null=True)
    join_date = models.DateField(null=True,auto_now_add=True)

    def __str__(self):
        return f"{self.fname} {self.lname}"
from django.db import models


class Address(models.Model):
    #aid = models.AutoField(auto_created=True, primary_key=True)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2, help_text = "Use the state abbreviation, such as PA")
    zipCode = models.CharField(max_length=5)

    class Meta:
        verbose_name_plural = 'Addresses'

    def get_serialized_data(self):
        return {
            'street': self.street,
            'city': self.city,
            'state': self.state,
            'zipCode': self.zipCode
        }

    def __str__(self):
        return '{0}, {1}, {2}'.format(self.street, self.city, self.state)

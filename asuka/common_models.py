from django.db import models




class UniversallyUniqueVariable(models.Model):
    url = models.CharField(max_length=512, blank=False, db_index=True, editable=False)

    class Meta:
        abstract = True

    def __str__(self):
        return "{}[{}]".format(self.name, self.description)
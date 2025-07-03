from django.db import models

# Create your models here.
class Topic(models.Model):
    """A topic the user is learning about"""
    text = models.CharField(max_length=250) # CharField when you want to store a small amount of text, such as name, title etc.
    date_added = models.DateTimeField(auto_now_add=True) # Record the current date and time automatically.
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # Reference to the user who created the topic

    def __str__(self):
        """Return a string representation of the model."""
        return self.text

class Entry(models.Model):
    """Something specific learned about a topic"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE) # Reference to another record in the database
    text = models.TextField() # This field doesnt need a size limit.
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        """Return a string representation of the model."""
        return self.text[:50] + "..."  # show just the first 50 characters of text

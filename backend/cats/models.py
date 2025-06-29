"""Database models for cats and their achievements."""
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Achievement(models.Model):
    """Represents an achievement that cats can earn."""

    name = models.CharField(max_length=64)

    def __str__(self):
        """Returns string representation of the achievement."""
        return self.name


class Cat(models.Model):
    """Represents a cat with owner and achievements."""

    name = models.CharField(max_length=16)
    color = models.CharField(max_length=16)
    birth_year = models.IntegerField()
    owner = models.ForeignKey(
        User, related_name='cats',
        on_delete=models.CASCADE
    )
    achievements = models.ManyToManyField(Achievement,
                                          through='AchievementCat')
    image = models.ImageField(
        upload_to='cats/images/',
        null=True,
        default=None
    )

    def __str__(self):
        """Returns string representation of the cat."""
        return self.name


class AchievementCat(models.Model):
    """Intermediate model for Cat-Achievement many-to-many relationship."""

    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)

    def __str__(self):
        """Returns combined string of achievement and cat."""
        return f'{self.achievement} {self.cat}'

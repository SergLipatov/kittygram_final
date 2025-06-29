"""Serializers for models with custom field processing."""
import base64
import datetime as dt

import webcolors
from django.core.files.base import ContentFile
from rest_framework import serializers

from .models import Achievement, AchievementCat, Cat


class Hex2NameColor(serializers.Field):
    """Converts hex color codes to their corresponding names."""

    def to_representation(self, value):
        """Returns the value unchanged."""
        return value

    def to_internal_value(self, data):
        """Converts hex to color name or raises ValidationError."""
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени')
        return data


class AchievementSerializer(serializers.ModelSerializer):
    """Serializer for Achievement model with renamed name field."""

    achievement_name = serializers.CharField(source='name')

    class Meta:
        """Meta configuration for AchievementSerializer."""

        model = Achievement
        fields = ('id', 'achievement_name')


class Base64ImageField(serializers.ImageField):
    """Handles base64-encoded image data."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class CatSerializer(serializers.ModelSerializer):
    """Main serializer for Cat model with related achievements."""

    achievements = AchievementSerializer(required=False, many=True)
    color = Hex2NameColor()
    age = serializers.SerializerMethodField()
    image = Base64ImageField(required=False, allow_null=True)
    image_url = serializers.SerializerMethodField(
        'get_image_url',
        read_only=True,
    )

    class Meta:
        """Meta configuration for CatSerializer."""

        model = Cat
        fields = (
            'id', 'name', 'color', 'birth_year', 'achievements',
            'owner', 'age', 'image', 'image_url'
        )
        read_only_fields = ('owner',)

    def get_image_url(self, obj):
        """Returns absolute URL for the cat's image if exists."""
        if obj.image:
            return obj.image.url
        return None

    def get_age(self, obj):
        """Calculates cat's age based on birth year."""
        return dt.datetime.now().year - obj.birth_year

    def create(self, validated_data):
        """Creates Cat instance with optional achievements."""
        if 'achievements' not in self.initial_data:
            cat = Cat.objects.create(**validated_data)
            return cat
        achievements = validated_data.pop('achievements')
        cat = Cat.objects.create(**validated_data)
        for achievement in achievements:
            current_achievement, status = Achievement.objects.get_or_create(
                **achievement
            )
            AchievementCat.objects.create(
                achievement=current_achievement, cat=cat
            )
        return cat

    def update(self, instance, validated_data):
        """Updates Cat instance and its achievements."""
        instance.name = validated_data.get('name', instance.name)
        instance.color = validated_data.get('color', instance.color)
        instance.birth_year = validated_data.get(
            'birth_year', instance.birth_year
        )
        instance.image = validated_data.get('image', instance.image)

        if 'achievements' not in validated_data:
            instance.save()
            return instance

        achievements_data = validated_data.pop('achievements')
        lst = []
        for achievement in achievements_data:
            current_achievement, status = Achievement.objects.get_or_create(
                **achievement
            )
            lst.append(current_achievement)
        instance.achievements.set(lst)

        instance.save()
        return instance

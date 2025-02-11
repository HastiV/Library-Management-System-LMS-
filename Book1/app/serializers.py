from rest_framework import serializers
from .models import Book, Author, Category

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'nationality']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class BookSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    category = CategorySerializer()

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'published_date', 'available_copies','category']


# book copies

class BookReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'available_copies']

    def update(self, instance, validated_data):
        if instance.available_copies > 0:
            instance.available_copies -= 1
            instance.save()
            return instance
        else:
            raise serializers.ValidationError("No copies available for reservation.")


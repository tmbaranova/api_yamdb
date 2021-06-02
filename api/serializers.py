from django.db.models import Avg
from rest_framework import serializers

from .models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    # rating = serializers.IntegerField(read_only=True, required=False)
    rating = serializers.SerializerMethodField(
        method_name='get_average_rating'
    )

    class Meta:
        fields = '__all__'
        model = Title

    def get_average_rating(self, obj):
        av_rating = obj.reviews.all().aggregate(av_rating=Avg('score'))
        if av_rating['av_rating'] is not None:
            av_rating = round(av_rating['av_rating'])
        else:
            av_rating = None
        return av_rating


class TitleCreateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True)
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug')

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment

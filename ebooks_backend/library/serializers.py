from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Book, ReadingProgress


class BookListSerializer(serializers.ModelSerializer):
    has_pdf    = serializers.SerializerMethodField()
    cover      = serializers.SerializerMethodField()

    class Meta:
        model  = Book
        fields = ['id', 'title', 'author', 'pages', 'category',
                  'cover', 'description', 'has_pdf', 'created_at']

    def get_has_pdf(self, obj):
        return bool(obj.pdf_file)

    def get_cover(self, obj):
        request = self.context.get('request')
        if obj.cover_image:
            return request.build_absolute_uri(obj.cover_image.url) if request else obj.cover_image.url
        return obj.cover_url or ''


class BookDetailSerializer(serializers.ModelSerializer):
    has_pdf = serializers.SerializerMethodField()
    pdf_url = serializers.SerializerMethodField()
    cover   = serializers.SerializerMethodField()

    class Meta:
        model  = Book
        fields = ['id', 'title', 'author', 'pages', 'category',
                  'cover', 'description', 'has_pdf', 'pdf_url',
                  'created_at', 'updated_at']

    def get_has_pdf(self, obj):
        return bool(obj.pdf_file)

    def get_pdf_url(self, obj):
        if not obj.pdf_file:
            return None
        request = self.context.get('request')
        return request.build_absolute_uri(obj.pdf_file.url) if request else obj.pdf_file.url

    def get_cover(self, obj):
        request = self.context.get('request')
        if obj.cover_image:
            return request.build_absolute_uri(obj.cover_image.url) if request else obj.cover_image.url
        return obj.cover_url or ''


class BookWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Book
        fields = ['title', 'author', 'pages', 'category',
                  'cover_url', 'cover_image', 'description', 'pdf_file']


class ReadingProgressSerializer(serializers.ModelSerializer):
    book_title  = serializers.CharField(source='book.title', read_only=True)
    book_cover  = serializers.SerializerMethodField()
    book_pages  = serializers.IntegerField(source='book.pages', read_only=True)
    book_author = serializers.CharField(source='book.author', read_only=True)

    class Meta:
        model  = ReadingProgress
        fields = ['id', 'book', 'book_title', 'book_author', 'book_cover', 'book_pages', 'page', 'updated_at']
        read_only_fields = ['updated_at']

    def get_book_cover(self, obj):
        request = self.context.get('request')
        if obj.book.cover_image:
            return request.build_absolute_uri(obj.book.cover_image.url) if request else obj.book.cover_image.url
        return obj.book.cover_url or ''


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model  = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
        )


class UserSerializer(serializers.ModelSerializer):
    is_admin = serializers.SerializerMethodField()

    class Meta:
        model  = User
        fields = ['id', 'username', 'email', 'is_admin']

    def get_is_admin(self, obj):
        return obj.is_staff or obj.is_superuser

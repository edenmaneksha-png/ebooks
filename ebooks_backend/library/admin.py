from django.contrib import admin
from .models import Book, ReadingProgress


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display  = ('title', 'author', 'category', 'pages', 'has_pdf', 'created_at')
    list_filter   = ('category',)
    search_fields = ('title', 'author')
    readonly_fields = ('created_at', 'updated_at')

    def has_pdf(self, obj):
        return bool(obj.pdf_file)
    has_pdf.boolean = True
    has_pdf.short_description = 'PDF'


@admin.register(ReadingProgress)
class ReadingProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'page', 'updated_at')
    list_filter  = ('user',)

from rest_framework import serializers
from .models import Product, Category, Branch,SizeOption,Syrup
from rest_framework import serializers
from django.utils.translation import override, gettext as _

class SyrupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Syrup
        fields = ['id', 'title_ru', 'title_uz', 'title_en', 'price']

from django.utils.translation import override
from drf_spectacular.utils import extend_schema_field

class SizeOptionSerializer(serializers.ModelSerializer):
    unit_ru = serializers.SerializerMethodField()
    unit_uz = serializers.SerializerMethodField()
    unit_en = serializers.SerializerMethodField()

    class Meta:
        model = SizeOption
        fields = ['id', 'size', 'price', 'unit_ru', 'unit_uz', 'unit_en']

    def get_translated_unit(self, obj, language_code):
        translations = {
            "ru": {"ml": "мл", "g": "г"},
            "uz": {"ml": "ml", "g": "g"},
            "en": {"ml": "ml", "g": "g"},
        }
        return translations.get(language_code, {}).get(obj.unit, obj.unit)

    @extend_schema_field(str)
    def get_unit_ru(self, obj):
        return self.get_translated_unit(obj, 'ru')

    @extend_schema_field(str)
    def get_unit_uz(self, obj):
        return self.get_translated_unit(obj, 'uz')

    @extend_schema_field(str)
    def get_unit_en(self, obj):
        return self.get_translated_unit(obj, 'en')


class ProductSerializer(serializers.ModelSerializer):
    category_title = serializers.CharField(source='category.title', read_only=True)
    branch_title = serializers.SerializerMethodField()
    branch_id = serializers.SerializerMethodField()
    size_options = SizeOptionSerializer(many=True)
    syrups = SyrupSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'title_ru', 'title_uz', 'title_en', 
            'description', 'description_ru', 'description_uz', 'description_en', 
            'category_title', 'category_id', 'slug', 'image', 
            'branch_title', 'branch_id', 'size_options', 'syrups'
        ]

    def get_branch_title(self, obj):
        return obj.category.branch.title

    def get_branch_id(self, obj):
        return obj.category.branch.id


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'title', 'title_ru', 'title_uz', 'title_en', 'slug', 'products']

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"

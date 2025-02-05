from modeltranslation.translator import translator, TranslationOptions
from .models import Branch, Category, Product, SizeOption, Syrup

class BranchTranslationOptions(TranslationOptions):
    fields = ('title', 'working_days', 'address')

class CategoryTranslationOptions(TranslationOptions):
    fields = ('title',)

class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

class SyrupTranslationOptions(TranslationOptions):
    fields = ('title',)

class SizeOptionTranslationOptions(TranslationOptions):
    fields =  ('unit',)

translator.register(Branch, BranchTranslationOptions)
translator.register(Category, CategoryTranslationOptions)
translator.register(Product, ProductTranslationOptions)
translator.register(Syrup, SyrupTranslationOptions)
translator.register(SizeOption, SizeOptionTranslationOptions)
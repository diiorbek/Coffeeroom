from modeltranslation.translator import translator, TranslationOptions
from .models import Address

class AddressTranslationOptions(TranslationOptions):
    fields = ('street', 'apartment', 'home', 'orientation')


translator.register(Address, AddressTranslationOptions)


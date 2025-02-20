from django.contrib import admin
from .models import Product, SizeOption, Category, Branch, LoyaltyCard, Syrup, IKPU

# SizeOption uchun inlayn registratsiya
class SizeOptionInline(admin.TabularInline):
    model = SizeOption
    extra = 1  # Har bir mahsulot uchun yangi bo'sh qatordan boshlash
    min_num = 1  # Kamida bitta o'lcham bo'lishi shart
    fields = ("size", "price", "unit")
    verbose_name = "Size Option"
    verbose_name_plural = "Size Options"

    def __str__(self):
        return self.size

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "branch", "is_active")  # Поля для отображения
    list_editable = ("is_active",) 
    search_fields = ("title", "description", "category__title")  
    readonly_fields = ("slug",)  
    inlines = [SizeOptionInline] 
    fieldsets = (
        ("Basic Information", {
            "fields": ("title", "title_uz", "title_ru", "title_en", "description", "description_uz", "description_ru", "description_en", "category", "packing_code", "ikpu", "slug", "image", "branch", "is_active"),
        }),
    )



# Category uchun optimallashtirilgan admin registratsiyasi
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "branch")  # Admin ro'yxatida ko'rsatish
    search_fields = ("title",)  # Qidirish qatori
    readonly_fields = ("slug",) # Slugni avtomatik yaratish


# Branch uchun optimallashtirilgan admin registratsiyasi
@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("title", "working_days", "working_time", "address")  # Ko'rinadigan ustunlar
    # search_fields = ("title", "working_days", "working_time", "address")  # Qidirish

@admin.register(IKPU)
class IKPUAdmin(admin.ModelAdmin):
    list_display = ("ikpu",)

@admin.register(LoyaltyCard)
class LoyaltyCardAdmin(admin.ModelAdmin):
    list_display = ('card_number', 'owner', 'balance', 'status', 'created_at')
    search_fields = ('card_number', 'owner__username')

class SyrupAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')
    search_fields = ('title',)

admin.site.register(Syrup, SyrupAdmin)

from django.contrib import admin
from django.db.models import Count

from cakeApp.models import Baker, Cake


# Register your models here.
class BakerAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        if request.user.is_superuser:
            return Baker.objects.annotate(num_cakes=Count('cakes')).filter(num_cakes__lt=5)
        return Baker.objects.all()

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser


class CakeAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return Baker.objects.filter(user=request.user).exists()

    def has_change_permission(self, request, obj=None):
        return obj and obj.baker.user == request.user

    def save_model(self, request, obj, form, change):
        baker_cakes = Cake.objects.filter(baker=obj.baker)
        if change:
            baker_cakes = baker_cakes.exclude(id=obj.id)

        if baker_cakes.count() >= 10:
            return

        total_price = sum(cake.price for cake in baker_cakes)
        if total_price + obj.price > 10000:
            return

        if Cake.objects.filter(name=obj.name).exclude(id=obj.id).exists():
            return

        super(CakeAdmin, self).save_model(request, obj, form, change)


admin.site.register(Cake, CakeAdmin)
admin.site.register(Baker, BakerAdmin)

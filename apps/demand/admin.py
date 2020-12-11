from django.contrib import admin
from apps.accounts.models import User
from apps.demand.models import Demand, Address, Contact


class UserAdmin(admin.ModelAdmin):
    pass


class DemandAdmin(admin.ModelAdmin):
    list_display = [
        'author',
        'description',
        'contatos',
        'address',
        'status'
    ]

    def contatos(self, obj):
        contacts = Contact.objects.filter(demand=obj.id)
        return ["%s" % (item.phone) for item in contacts]

    def address(self, obj):
        address = Address.objects.filter(demand=obj.id)
        return address


admin.site.register(Demand, DemandAdmin)
admin.site.register(User, UserAdmin)

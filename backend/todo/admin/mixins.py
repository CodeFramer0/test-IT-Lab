class HashidAdminMixin:
    def display_hashid(self, obj):
        return str(obj.id)

    display_hashid.short_description = "ID"

    def get_list_display(self, request):
        return tuple(
            "display_hashid" if field_name == "id" else field_name
            for field_name in super().get_list_display(request)
        )

    def get_readonly_fields(self, request, obj=None):
        return tuple(
            "display_hashid" if field_name == "id" else field_name
            for field_name in super().get_readonly_fields(request, obj)
        )

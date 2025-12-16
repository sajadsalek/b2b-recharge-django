from django.contrib import admin, messages
from src.financial.model.refill_request import RefillRequest
from src.financial.services.refill_request_service import approve_refill_request, reject_refill_request
from django.core.exceptions import ValidationError


@admin.register(RefillRequest)
class InvestmentRequestAdmin(admin.ModelAdmin):
    list_display = (
        "amount",
        "customer",
        "status",
    )

    list_filter = ("status",)
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [f.name for f in self.model._meta.fields if f.name != 'status']
        return []

    actions = ["approve_requests", "reject_requests"]

    def save_model(self, request, obj, form, change):
        # اگر status تغییر کرده و حالا 'approved' هست، action approve رو اجرا کن
        if 'status' in form.changed_data and obj.status == 'approved' and form.initial['status'] == 'pending':
            approve_refill_request(
                request_id=obj.id
            )
            messages.success(request, "approved")

        elif 'status' in form.changed_data and obj.status == 'rejected' and form.initial['status'] == 'pending':
            reject_refill_request(
                request_id=obj.id
            )
            messages.success(request, "rejected.")

        else:
            raise ValidationError("action not allowed")

    def approve_requests(self, request, queryset):
        for inv in queryset:
            approve_refill_request(
                request_id=inv.id,
            )

    approve_requests.short_description = "Approve-Request"

    def reject_requests(self, request, queryset):
        for inv in queryset:
            reject_refill_request(
                request_id=inv.id,
            )

    reject_requests.short_description = "Reject-Request"

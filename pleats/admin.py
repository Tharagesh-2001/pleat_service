# from django.contrib import admin
# from .models import Appointment, Appoint
# from django.core.mail import send_mail
# from django.conf import settings
# from django.contrib import messages
# # Register your models here.

# admin.site.register(Appointment)
# admin.site.register(Appoint)
# class AppointAdmin(admin.ModelAdmin):  # Renamed for consistency
#     list_display = ['customer', 'date', 'status']  # Now valid
#     list_filter = ['status', 'date']
#     search_fields = ['customer__username', 'customer__email']
    
#     actions = ['accept_selected_orders']
    
#     def accept_selected_orders(self, request, queryset):
#         updated_count = 0
#         email_errors = []
        
#         for appointment in queryset:
#             if getattr(appointment, 'status', None) == 'accepted':
#                 self.message_user(request, f'Skipped {appointment.customer.username}: already accepted.', messages.WARNING)
#                 continue
            
#             if not appointment.customer.email:
#                 email_errors.append(f"No email for {appointment.customer.username}")
#                 continue
            
#             try:
#                 appointment.status = 'accepted'
#                 appointment.save()
                
#                 # Log before sending
#                 self.message_user(request, f"Updating and emailing {appointment.customer.username} at {appointment.customer.email}", messages.INFO)
                
#                 subject = 'Booking Confirmation - Process Started'
#                 message = f'Dear {appointment.customer.username},\n\nYour appointment on {appointment.date} has been accepted, and the booking process has started. We will contact you soon with more details.\n\nBest regards,\nYour Team'
                
#                 send_mail(
#                     subject,
#                     message,
#                     settings.EMAIL_HOST_USER,
#                     [appointment.customer.email],
#                     fail_silently=False,
#                 )
#                 updated_count += 1
#                 self.message_user(request, f"Email sent to {appointment.customer.username}", messages.SUCCESS)
                
#             except Exception as e:
#                 email_errors.append(f"Failed for {appointment.customer.username}: {str(e)}")
        
#         if updated_count > 0:
#             self.message_user(request, f'Successfully accepted {updated_count} appointment(s) and sent confirmation emails.', messages.SUCCESS)
#         if email_errors:
#             self.message_user(request, f'Errors: {" | ".join(email_errors)}', messages.ERROR)
        
#     accept_selected_orders.short_description = 'Accept selected orders and send confirmation emails'




from django.contrib import admin
from .models import Appointment
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['customer', 'name', 'email', 'phone', 'service', 'date', 'time', 'status']
    list_filter = ['status', 'date', 'service']
    search_fields = ['customer__username', 'customer__email', 'name', 'email', 'service']

    actions = ['accept_selected_appointments']

    def accept_selected_appointments(self, request, queryset):
        updated_count = 0
        email_errors = []

        for appointment in queryset:
            if appointment.status == 'accepted':
                customer_name = appointment.customer.username if appointment.customer else appointment.name
                self.message_user(request, f'Skipped {customer_name}: already accepted.', messages.WARNING)
                continue

            # Use customer email if available, else direct email
            email_to_use = appointment.customer.email if appointment.customer else appointment.email
            if not email_to_use:
                customer_name = appointment.customer.username if appointment.customer else appointment.name
                email_errors.append(f"No email for {customer_name}")
                continue

            try:
                appointment.status = 'accepted'
                appointment.save()

                customer_name = appointment.customer.username if appointment.customer else appointment.name
                self.message_user(request, f"Updating and emailing {customer_name} at {email_to_use}", messages.INFO)

                subject = 'Booking Confirmation - Process Started'
                message = (
                    f'Dear {customer_name},\n\n'
                    f'Your appointment for {appointment.service} on {appointment.date} at {appointment.time} '
                    f'has been accepted, and the booking process has started. We will contact you soon with more details.\n\n'
                    f'Best regards,\nYour Team'
                )

                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [email_to_use],
                    fail_silently=False,
                )
                updated_count += 1
                self.message_user(request, f"Email sent to {customer_name}", messages.SUCCESS)

            except Exception as e:
                customer_name = appointment.customer.username if appointment.customer else appointment.name
                email_errors.append(f"Failed for {customer_name}: {str(e)}")

        if updated_count > 0:
            self.message_user(request, f'Successfully accepted {updated_count} appointment(s) and sent confirmation emails.', messages.SUCCESS)
        if email_errors:
            self.message_user(request, f'Errors: {" | ".join(email_errors)}', messages.ERROR)

    accept_selected_appointments.short_description = 'Accept selected appointments and send confirmation emails'
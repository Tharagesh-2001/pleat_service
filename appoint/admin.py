from django.contrib import admin
# from django.core.mail import send_mail
# from django.conf import settings
# from django.contrib import messages
# from .models import Appoint  # Adjust if your model import is different

# @admin.register(Appoint)
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
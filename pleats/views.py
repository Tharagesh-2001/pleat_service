from rest_framework import generics
from .models import Appointment
from .serializers import AppointmentSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from django.utils.html import format_html

@method_decorator(csrf_exempt, name='dispatch')
class AppointmentListCreate(generics.ListCreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    # def perform_create(self, serializer):
    #     appointment = serializer.save()

    #     # Email content
    #     subject = f"New Appointment from {appointment.name}"
    #     message = (
    #         f"📅 New Appointment Details:\n\n"
    #         f"Name: {appointment.name}\n"
    #         f"Email: {appointment.email}\n"
    #         f"Phone: {appointment.phone}\n"
    #         f"Service: {appointment.service}\n"
    #         f"Date: {appointment.date}\n"
    #         f"Time: {appointment.time}\n"
    #         f"Address: {appointment.address or 'N/A'}\n"
    #         f"Notes: {appointment.notes or 'N/A'}\n"
    #     )

    #     send_mail(
    #         subject,
    #         message,
    #         None,  # from email (uses DEFAULT_FROM_EMAIL)
    #         ["tharagesh.cs@gmail.com"],  # recipient (shop owner)
    #         fail_silently=False,
    #     )

    def perform_create(self, serializer):
        appointment = serializer.save()

        subject = f"📅 New Appointment from {appointment.name}"

        # Plain text fallback
        message = (
            f"New Appointment Details:\n\n"
            f"Name: {appointment.name}\n"
            f"Email: {appointment.email}\n"
            f"Phone: {appointment.phone}\n"
            f"Service: {appointment.service}\n"
            f"Date: {appointment.date}\n"
            f"Time: {appointment.time}\n"
            f"Address: {appointment.address or 'N/A'}\n"
            f"Notes: {appointment.notes or 'N/A'}\n"
        )

        # Professional HTML layout
        html_message = format_html(
            """
            <div style="font-family: Arial, sans-serif; padding:20px; color:#333;">
                <h2 style="color:#2C3E50;">📅 New Appointment Details</h2>
                <table style="border-collapse: collapse; width:100%; max-width:600px;">
                    <tr>
                        <td style="padding:8px; border:1px solid #ddd;"><b>Name</b></td>
                        <td style="padding:8px; border:1px solid #ddd;">{}</td>
                    </tr>
                    <tr>
                        <td style="padding:8px; border:1px solid #ddd;"><b>Email</b></td>
                        <td style="padding:8px; border:1px solid #ddd;">{}</td>
                    </tr>
                    <tr>
                        <td style="padding:8px; border:1px solid #ddd;"><b>Phone</b></td>
                        <td style="padding:8px; border:1px solid #ddd;">{}</td>
                    </tr>
                    <tr>
                        <td style="padding:8px; border:1px solid #ddd;"><b>Service</b></td>
                        <td style="padding:8px; border:1px solid #ddd;">{}</td>
                    </tr>
                    <tr>
                        <td style="padding:8px; border:1px solid #ddd;"><b>Date</b></td>
                        <td style="padding:8px; border:1px solid #ddd;">{}</td>
                    </tr>
                    <tr>
                        <td style="padding:8px; border:1px solid #ddd;"><b>Time</b></td>
                        <td style="padding:8px; border:1px solid #ddd;">{}</td>
                    </tr>
                    <tr>
                        <td style="padding:8px; border:1px solid #ddd;"><b>Address</b></td>
                        <td style="padding:8px; border:1px solid #ddd;">{}</td>
                    </tr>
                    <tr>
                        <td style="padding:8px; border:1px solid #ddd;"><b>Notes</b></td>
                        <td style="padding:8px; border:1px solid #ddd;">{}</td>
                    </tr>
                </table>
                <p style="margin-top:20px; font-size:14px; color:#555;">
                    ⚡ Please log in to the admin dashboard to manage this appointment.
                </p>
            </div>
            """,
            appointment.name,
            appointment.email,
            appointment.phone,
            appointment.service,
            appointment.date,
            appointment.time,
            appointment.address or "N/A",
            appointment.notes or "N/A"
        )

        send_mail(
            subject,
            message,  # plain text fallback
            None,
            ["tharagesh.cs@gmail.com"],
            fail_silently=False,
            html_message=html_message,  # ✅ this makes it professional
        )
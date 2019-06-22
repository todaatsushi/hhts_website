"""
Contains ConfirmEmail object which constructs an email to send to the related booking
upon a booking being marked confirmed.
"""
from django.core.mail import EmailMessage

class ConfirmEmail(object):
    """
    Needs a related Booking model with the booker's details.
    """
    def __init__(self, booking):
        self.booking = booking
        self.body = ""
        self.to_email = booking.contact_email
        self.subject = f"Confirmed: Booking at {booking.scheduled_at}"

    def generate_body(self):
        """
        Generates generic email body confirming the booking.
        """
        body = f"""
            Hi {self.booking.contact_name},

            Thank you for booking a tour with us. Your tour has been confirmed
            at {self.booking.scheduled_at}. We can confirm that the tour will last
            {self.booking.duration}.

            Please confirm the rest of the details below:

            Tour Information:
                - Date: {self.booking.scheduled_at}
                - Duration: {self.booking.duration}
                - Stops: {self.booking.places_to_visit}

        """

        if self.booking.is_group:
            body += f"""
                Group Information:
                    - Group name: {self.booking.group_name}
                    - Group #: {self.booking.group_number}
                    - Age range: {self.booking.age_group}
                    - Transportation: {self.booking.transportation}
            """

        body += f"""
            Extra details:
                - {self.booking.extra_details}

                
            We look forward to seeing you!

            Regards,
            Tour Team
        """

        self.body = body

    def send(self):
        email = EmailMessage(
            subject=self.subject,
            body=self.body,
            to=[self.to_email]
        )

        email.send()

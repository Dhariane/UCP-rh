import ssl
import smtplib
from django.core.mail.backends.smtp import EmailBackend

class SSLEmailBackend(EmailBackend):
    def open(self):
        if self.connection:
            return False
        
        # ✅ Contexte SSL sans vérification certificat
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode    = ssl.CERT_NONE

        try:
            if self.use_ssl:
                self.connection = smtplib.SMTP_SSL(
                    self.host, self.port,
                    timeout     = self.timeout,
                    context     = context,
                )
            else:
                self.connection = smtplib.SMTP(
                    self.host, self.port,
                    timeout = self.timeout,
                )
                if self.use_tls:
                    self.connection.ehlo()
                    self.connection.starttls(context=context)
                    self.connection.ehlo()

            if self.username and self.password:
                self.connection.login(self.username, self.password)

            return True

        except Exception as e:
            if not self.fail_silently:
                raise
            return False
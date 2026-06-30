import ssl
from django.core.mail.backends.smtp import EmailBackend


class SSLEmailBackend(EmailBackend):
    """
    Backend email personnalisé.
    - Windows (dev)  : désactive la vérification SSL (Python 3.14 bug)
    - Linux (Render) : comportement SSL normal
    """
    def open(self):
        if self.connection:
            return False

        self.connection = self.connection_class(
            self.host,
            self.port,
            timeout=self.timeout
        )

        import platform
        # ✅ Désactive SSL uniquement sur Windows (développement)
        # Sur Render (Linux), SSL normal
        if platform.system() == 'Windows':
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
        else:
            context = ssl.create_default_context()  # SSL strict en production

        try:
            self.connection.ehlo()
            if self.use_tls:
                self.connection.starttls(context=context)
                self.connection.ehlo()
            if self.username and self.password:
                self.connection.login(self.username, self.password)
            return True
        except Exception:
            if not self.fail_silently:
                raise
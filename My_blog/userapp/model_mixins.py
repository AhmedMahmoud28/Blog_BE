from django.utils.crypto import get_random_string


class UserMixin:
    def soft_delete(self):
        self.is_deleted = True
        user_email = self.email
        random = get_random_string(10)
        self.email = user_email + random
        self.save()
        return self

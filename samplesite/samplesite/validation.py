from django.core.exceptions import ValidationError


class NoForbiddenCharsValidator:
    """Пример валидатора паролей"""
    def __init__(self, forbidden_chars=(' ',)):
        self.forbidden_chars = forbidden_chars

    def validate(self, password, user=None):
        for i in self.forbidden_chars:
            if i in password:
                raise ValidationError(
                    'Пароль должен содержать не допустимые символы % ! & ? s ~'.join(self.forbidden_chars),
                    code='forbidden_chars_present')

    def get_help_text(self):
        return ValidationError(
            'Пароль должен содержать не допустимые символы % ! & ? s ~'.join(self.forbidden_chars),
            code='forbidden_chars_present')

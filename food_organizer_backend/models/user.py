from django.db import models


class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=500)
    auth_from = models.DateTimeField()
    auth_until = models.DateTimeField()
    failed_attempts = models.IntegerField()
    blocked_until = models.DateTimeField()
    recovery = models.CharField(max_length=1000)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __init__(
            self,
            _username,
            _email,
            _password,
            _auth_from,
            _auth_until,
            _failed_attempts,
            _blocked_until,
            _recovery,
            _created_at,
            _updated_at,
            *args,
            **kwargs):
        super().__init__(*args, **kwargs)
        self.username = _username
        self.email = _email
        self.password = _password
        self.auth_from = _auth_from
        self.auth_until = _auth_until
        self.failed_attempts = _failed_attempts
        self.blocked_until = _blocked_until
        self.recovery = _recovery
        self.created_at = _created_at
        self.updated_at = _updated_at

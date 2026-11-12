
from django.contrib.auth.mixins import UserPassesTestMixin


class RoleRequiredMixin(UserPassesTestMixin):

    allowed_roles = ()

    def test_func(self):
        user = self.request.user

        return (
            user.is_authenticated
            and (
                user.is_superuser
                or user.role in self.allowed_roles
            )
        )


class AdminRequiredMixin(RoleRequiredMixin):

    allowed_roles = ('ADMIN',)


class ManagerOrAdminRequiredMixin(RoleRequiredMixin):

    allowed_roles = ('ADMIN', 'MANAGER')

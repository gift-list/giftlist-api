from rest_framework import permissions


class StaffExceptCreate(permissions.BasePermission):

    def has_permission(self, request, view):
        """
        We want to allow the creation of users as open but listing for staff
        only
        :param request:
        :param view:
        :return:
        """
        permission = False

        if request.method == "POST":
            permission = True
        elif request.user.is_authenticated() and request.user.is_staff:
            permission = True

        return permission

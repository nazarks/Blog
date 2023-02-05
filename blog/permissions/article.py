from combojsonapi.permission.permission_system import PermissionForPatch, PermissionMixin, PermissionUser
from flask_combo_jsonapi.exceptions import AccessDenied
from flask_login import current_user

from blog.models.article import Article


class ArticlePatchPermission(PermissionMixin):
    PATCH_AVAILABLE_FIELDS = [
        "title",
        "body",
    ]

    def patch_permission(self, *args, user_permission: PermissionUser = None, **kwargs) -> PermissionForPatch:

        self.permission_for_patch.allow_columns = (self.PATCH_AVAILABLE_FIELDS, 10)
        return self.permission_for_patch

    def patch_data(
        self, *args, data: dict = None, obj: Article = None, user_permission: PermissionUser = None, **kwargs
    ) -> dict:

        if current_user.is_authenticated:

            if (obj and current_user.author and obj.author_id == current_user.author.id) or current_user.is_staff:
                permission_for_patch = user_permission.permission_for_patch_permission(model=Article)
                return {key: value for key, value in data.items() if key in permission_for_patch.columns}

        raise AccessDenied("no access")

from flask_combo_jsonapi import ResourceDetail, ResourceList

from blog.models import User
from blog.models.database import db
from blog.permissions.user import UserListPermission, UserPatchPermission
from blog.schemas import UserSchema


class UserList(ResourceList):
    schema = UserSchema
    data_layer = {
        "session": db.session,
        "model": User,
        "permission_get": [UserListPermission],
    }


class UserDetail(ResourceDetail):
    schema = UserSchema
    data_layer = {
        "session": db.session,
        "model": User,
        "permission_patch": [UserPatchPermission],
    }

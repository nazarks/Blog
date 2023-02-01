from combojsonapi.event.resource import EventsResource
from flask_combo_jsonapi import ResourceDetail, ResourceList

from blog.models import Article
from blog.models.database import db
from blog.permissions.article import ArticlePatchPermission
from blog.schemas import ArticleSchema


class ArticleListEvents(EventsResource):
    def event_get_count(self, _permission_user=None):
        return {"count": Article.query.count()}


class ArticleList(ResourceList):
    events = ArticleListEvents
    schema = ArticleSchema
    data_layer = {
        "session": db.session,
        "model": Article,
    }


class ArticleDetail(ResourceDetail):
    schema = ArticleSchema
    data_layer = {
        "session": db.session,
        "model": Article,
        "permission_patch": [ArticlePatchPermission],
    }

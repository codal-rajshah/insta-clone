from rest_framework.renderers import JSONRenderer
from uuid import uuid4


def set_json_renderer(response):
    response.accepted_renderer = JSONRenderer()
    response.accepted_media_type = "application/json"
    response.renderer_context = {}
    return response


def uuid_hex():
    return uuid4().hex

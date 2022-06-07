<% if eq (index .Params `database`) "mongo" -%>
from motor.motor_asyncio import AsyncIOMotorClient
<%- end %>

from py_easy_rest import PYRSanicAppBuilder
from py_easy_rest.service import PYRService
<% if eq (index .Params `database`) "mongo" -%>
from py_easy_rest_mongo_motor_repo import PYRMongoRepo
<%- end %>
<% if eq (index .Params `cacheStore`) "redis" -%>
from py_easy_rest_redis_cache import PYRRedisCache
<%- end %>
<% if eq (index .Params `cacheStore`) "memory" -%>
from py_easy_rest_memory_cache import PYRMemoryCache
<%- end %>

config = {
    "name": "ProjectExample",
    "schemas": [{
        "name": "Companies",
        "slug": "companies",
        "properties": {
            "name": {"type": "string"},
            "size": {"type": "integer"},
            "industry": {"type": "string"},
        },
        "required": ["name"],
    }, {
        "name": "Industries",
        "slug": "industries",
        "properties": {
            "name": {"type": "string"},
        },
        "required": ["name"],
    }, {
        "name": "Personal Interests",
        "slug": "personal-interests",
        "properties": {
            "name": {"type": "string"},
        },
        "required": ["name"],
    }, , {
        "name": "Technical Skills",
        "slug": "tech-skills",
        "properties": {
            "name": {"type": "string"},
        },
        "required": ["name"],
    }]
}

<% if eq (index .Params `database`) "mongo" -%>
repo = PYRMongoRepo()
<% if eq (index .Params `cacheStore`) "redis" -%>
cache = PYRRedisCache("redis://redis")
service = PYRService(config, repo=repo, cache=cache)
<% else if eq (index .Params `cacheStore`) "memory" -%>
cache = PYRMemoryCache()
service = PYRService(config, repo=repo, cache=cache)
<% else -%>
service = PYRService(config, repo=repo)
<%- end %>
<% else -%>
<% if eq (index .Params `cacheStore`) "redis" -%>
cache = PYRRedisCache("redis://redis")
service = PYRService(config, cache=cache)
<% else if eq (index .Params `cacheStore`) "memory" -%>
cache = PYRMemoryCache()
service = PYRService(config, cache=cache)
<% else -%>
service = PYRService(config)
<%- end %>
<%- end %>
sanic_app = PYRSanicAppBuilder.build(config, service)

<% if eq (index .Params `database`) "mongo" -%>
@sanic_app.listener('before_server_start')
def init(app, loop):
    mongo_db_instance = AsyncIOMotorClient("mongodb://mongo:27017/db")
    db = mongo_db_instance.get_default_database()
    repo.set_db_connection(db)
<%- end %>

sanic_app.run(
    host='0.0.0.0',
    port=8000,
    debug=True,
    auto_reload=True,
)

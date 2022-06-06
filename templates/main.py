from motor.motor_asyncio import AsyncIOMotorClient

from py_easy_rest import PYRSanicAppBuilder
from py_easy_rest.service import PYRService
from py_easy_rest_mongo_motor_repo import PYRMongoRepo


config = {
    "name": "ProjectName",
    "schemas": [{
        "name": "Mock",
        "slug": "mock",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"},
        },
        "required": ["name"],
    }]
}

repo = PYRMongoRepo()

service = PYRService(config, repo=repo)
sanic_app = PYRSanicAppBuilder.build(config, service)

@sanic_app.listener('before_server_start')
def init(app, loop):
    mongo_db_instance = AsyncIOMotorClient("mongodb://mongo:27017/db")
    db = mongo_db_instance.get_default_database()
    repo.set_db_connection(db)


sanic_app.run(
    host='0.0.0.0',
    port=8000,
    debug=True,
    auto_reload=True,
)

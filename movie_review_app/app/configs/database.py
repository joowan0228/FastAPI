from tortoise.contrib.fastapi import register_tortoise

TORTOISE_ORM = {
    "connections": {"default": "sqlite://db.sqlite3"},
    "apps": {
        "models": {
            "models": [
                "app.models.base",
                "app.models.users",
                "app.models.movies",
                "app.models.reviews",
                "app.models.likes"
            ],
            "default_connection": "default"
        }
    }
}

def init_db(app):
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=False,
        add_exception_handlers=True,
    )

import gunicorn.app.base
import gunicorn.glogging
import gunicorn.workers.sync
from app import app


class StandaloneApplication(gunicorn.app.base.BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == '__main__':
    options = {
        'bind': '0.0.0.0:9090',
        'preload': True,
        'workers': 3,
    }
    StandaloneApplication(app, options).run()

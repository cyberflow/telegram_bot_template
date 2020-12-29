import logging
from importlib import import_module, resources

logger = logging.getLogger(__name__)


class BotRouter:
    _HANDLERS = []

    @classmethod
    def clean(cls):
        cls._HANDLERS = []

    @classmethod
    def bot_handler(cls, handler_factory):
        cls._HANDLERS.append(handler_factory)
        return handler_factory

    @classmethod
    def get_handlers(cls):
        for handler in cls._HANDLERS:
            yield handler()

    @classmethod
    def get_lazy_handlers(cls):
        for handler in cls._HANDLERS:
            yield handler


def autodiscovery():
    files = resources.contents('handlers')
    plugins = [f[:-3] for f in files if f.endswith(".py") and f[0] != "_"]
    for app in plugins:
        logger.info(f"Import {app} handler module")
        module = f"handlers.{app}"
        try:
            import_module(module)
        except Exception:
            logger.error("Something went wrong importing: %s", module, exc_info=1)


bot_handler = BotRouter.bot_handler
get_handlers = BotRouter.get_handlers
get_lazy_handlers = BotRouter.get_lazy_handlers

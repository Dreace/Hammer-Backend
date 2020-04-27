import logging
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': "[%(asctime)s %(filename)s %(funcName)s %(lineno)d] %(levelname)s %(message)s",
    }},
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stderr',
            'formatter': 'default'
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console'],
    }
})

root_logger = logging.getLogger("root")


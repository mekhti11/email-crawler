import logging

DEBUG = True
USE_COLORS = True


LOGGING = {
	'version': 1,
    'disable_existing_loggers': False,

	'formatters': {
		'console': {
			'format': '[%(asctime)s] %(levelname)s::%(module)s - %(message)s',
		},
		'file': {
			'format': '[%(asctime)s] %(levelname)s::(P:%(process)d T:%(thread)d)::%(module)s - %(message)s',
		},
	},

	'handlers': {
		'console': {
			'class': 'ColorStreamHandler.ColorStreamHandler',
			'formatter':'console',
			'level': 'DEBUG',
			'use_colors': USE_COLORS,
		},
		'file': {
			'class': 'logging.handlers.TimedRotatingFileHandler',
			'formatter':'file',
			'level': 'INFO',
			'when': 'midnight',
			'filename': 'logs/pycrawler.log',
			'interval': 1,
			'backupCount': 0,
			'encoding': None,
			'delay': False,
			'utc': False,
		},
	},

	'loggers': {
		'CRAWLER_LOG': {
			'handlers': ['console', 'file'],
			'level': 'DEBUG' if DEBUG else 'INFO',
			'propagate': True,
		},
	}
}

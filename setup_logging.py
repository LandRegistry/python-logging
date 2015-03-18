import os
import logging
import logging.config
import yaml


class AuditLogger(logging.getLoggerClass()):
    """ Custom logging class, to ensure that audit log calls always succeed. """

    def __init__(self, name):
        super().__init__(name)

    def audit(self, msg, *args, **kwargs):
        msg = "[AUDIT] " + msg
        self._log(logging.CRITICAL, msg, args, **kwargs)


def get_log_path(name=None):

    # 'logs' directory name is assumed - see "logging.yaml".
    log_path = 'logs'
    return log_path if name is None else log_path + '/' + name

def setup_logging(log_path='logging.yaml', default_level=logging.INFO, env_key='LOG_CFG'):
    """Setup logging configuration. """

    logging.setLoggerClass(AuditLogger)

    if os.path.exists(log_path):
        with open(log_path, 'rt') as f:
            config = yaml.load(f.read())

        # Make sure that directory for logs exists.
        try:
            os.mkdir(get_log_path())
        except OSError as e:
            pass

        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

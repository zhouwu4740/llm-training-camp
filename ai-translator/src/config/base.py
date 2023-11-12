import yaml
from utils import logger


class Config:
    _instance = None

    # singleton pattern
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._config = None
        return cls._instance

    def initialize(self, args):
        """
        Using config file and command line arguments to set up the configuration,
        and the command line arguments have higher priority than config file.
        """
        with open(args.config_file, 'r') as f:
            config = yaml.safe_load(f)

        overridden_values = {
            arg_key: arg_value
            for arg_key, arg_value in vars(args).items()
            if arg_key in config and arg_value is not None
        }
        # command line arguments have higher priority than config file
        config.update(overridden_values)
        # store the original config dictionary
        self._instance._config = config
        logger.debug(f"Config: {self._instance._config}")

    def get_model_config(self, model_provider=None):
        if model_provider is None:
            model_provider = self._instance._config['model_provider']

        model_config = self._instance._config['model'][model_provider]
        model_default = self._instance._config['model']['default']
        overridden_values = {k: v for k, v in model_default.items() if k not in model_config}
        model_config.update(overridden_values)
        model_config["_model_provider"] = model_provider
        return model_config

    def __getattr__(self, name):
        if self._instance._config and name in self._instance._config:
            return self._instance._config[name]
        raise AttributeError(f"'Config' object has no attribute '{name}'")

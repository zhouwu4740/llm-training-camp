import yaml

from config import Config
from utils import ArgumentParser

if __name__ == '__main__':
    # with open('config.yaml', 'r') as f:
    #     config = yaml.safe_load(f)
    #     print(config)

    # 解析命令行
    argument_parser = ArgumentParser()
    args = argument_parser.parse()
    # 初始化配置单例
    config = Config()
    config.initialize(args)
    print(vars(config))

    print(config.get_model_config('chatglm'))

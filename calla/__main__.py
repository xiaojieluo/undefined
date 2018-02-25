import argparse
import sys, os
from calla import make_app
from calla.config import Config
from calla.process import start_thread, log_worker
from calla.model import db, Setting, Log, db_path, Article
# here = os.path.abspath(os.path.dirname(__file__))


def parse_args(args):
    ''' parse args'''
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-p', '--port', nargs='?', type=int)
    parser.add_argument('-c', '--config', nargs='?', type=str)

    args = parser.parse_args(args)
    return args

def init(replace = False):
    ''' 初始化工作目录
    只有有需要时才执行
    Args:
        replace 为 True 时强制覆盖数据库， 调试用
    '''
    db.connect()
    if  replace is True or not os.path.exists(db_path):
        model_list = [Article, Log]
        db.create_tables(model_list)
        for model in model_list:
            print(model)
            print(model.init())


def main():
    '''enter'''
    # init()
    args = parse_args(sys.argv[1:])
    Config.monkey_patch(args.config)

    app = make_app()
    # 开启 log 线程
    start_thread(log_worker, daemon = True)
    app.run(
        port=args.port
        )


if __name__ == '__main__':
    main()

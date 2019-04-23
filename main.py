"""定数"""
from const import *

"""標準ライブラリ"""
import json

"""外部ライブラリ"""
import requests

"""ロギング"""
from logging import config, getLogger


# ロガー設定
with open(LOGGER_PATH, encoding='UTF-8') as f:
    config.dictConfig(json.load(f))
slog = getLogger('SYSTEM')  # システムログ ( 記録が必要な処理の保存 )
tlog = getLogger('TRADE')   # トレードログ ( 取引内容の保存 )


def main():
    slog.debug('main')


if __name__ == "__main__":
    slog.info('initialize')
    main()
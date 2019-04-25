"""標準ライブラリ"""
import json

"""外部ライブラリ"""
from django.shortcuts import render
# from .models import Post

"""ロギング"""
from logging import config, getLogger


# Create your views here.

# ロガー設定
with open('logger.json', encoding='UTF-8') as f:
    config.dictConfig(json.load(f))
slog = getLogger('SYSTEM')  # システムログ ( 記録が必要な処理の保存 )
tlog = getLogger('TRADE')   # トレードログ ( 取引内容の保存 )


def post_list(request):
    slog.info('view/post_list: initialize')
    return render(request, 'view/template.html', {'title': 'TITLE'})

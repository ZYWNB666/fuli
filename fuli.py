# encoding:utf-8
import datetime
import difflib
import json
import random
import re
from time import sleep

import requests

import plugins
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from plugins import *


@plugins.register(
    name="fuli",
    desire_priority=99,
    hidden=True,
    desc="fuli插件",
    version="0.2",
    author="lanvent",
)
class fuli(Plugin):
    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        logger.info("[chajian] inited")
        # self.config = super().load_config()

    def on_handle_context(self, e_context: EventContext):
        if e_context["context"].type != ContextType.TEXT:
            return
        reply = None
        query = e_context["context"].content.strip()
        current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
        # print('时间匹配度' + time_similarity)
        image_string1 = '福利图,随机福利图,随机图,福利图片,美女图片,福利图片,随机图片'
        image_string2 = query
        image_similarity = difflib.SequenceMatcher(None, image_string1, image_string2).ratio()
        # print('福利图匹配度' + image_similarity)
        video_string1 = '福利视频,随机福利视频,随机视频,美女视频,擦边视频'
        video_string2 = query
        video_similarity = difflib.SequenceMatcher(None, video_string1, video_string2).ratio()

        if image_similarity > 0.2:
            print(query + '测试随机福利图片')
            print(image_similarity)
            # suijiurl = 'http://api.yujn.cn/api/yht.php?type=image' #旧的，需要json解析
            urls_list = ['https://api.yujn.cn/api/baisi.php',
                         'https://api.yujn.cn/api/jk.php'
                         ]
            headers = {'Content-Type': "application/x-www-form-urlencoded"}
            pt_url = random.choice(urls_list)
            print(pt_url)
            max_retries = 3  # 最大重试次数
            retry_count = 0
            while retry_count < max_retries:
                try:
                    pt_response = requests.get(pt_url, headers=headers, timeout=5)
                    pt_response.raise_for_status()
                    break
                except requests.exceptions.RequestException as e:
                    print(f"\n请求失败，原因：{e}，正在尝试重新获取...")
                    retry_count += 1
                    sleep(1)  # 延迟一秒后再次尝试
            if retry_count == max_retries:
                text = "获取数据失败"
                reply = Reply(ReplyType.ERROR, text)
            else:
                reply = Reply(ReplyType.IMAGE_URL, pt_url)
                # 资源下载到本地
                pic_res = requests.get(pt_url, stream=True)
                # 指定本地保存路径及文件名
                print(current_time)
                image_name = f'image_{current_time}.jpg'
                local_image_path = f'E:\\python项目\\chatgpt-on-wechat-master\\download\\image\\{image_name}'  # 替换为实际路径
                print(local_image_path)
                with open(local_image_path, 'wb') as f:
                    size = 0
                    for block in pic_res.iter_content(1024):
                        size += len(block)
                        f.write(block)
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS  # 事件结束，并跳过处理context的默认逻辑
        if video_similarity > 0.2:
            print(query + '测试随机福利视频')
            print(video_similarity)
            urls_list = [
                'baisis.php?type=video',
                'ksbianzhuang.php?type=video',
                'chuanda.php?type=video',
                'COS.php?type=video',
                'diaodai.php?type=video',
                'hanfu.php?type=video',
                'heisis.php?type=video',
                'jjy.php?type=video',
                'jiepai.php?type=video',
                'jksp.php?type=video',
                'luoli.php?type=video',
                'yuzu.php?type=video',
                'manyao.php?type=video',
                '/manzhan.php?type=video',
                'nvgao.php?type=video',
                'qingchun.php?type=video',
                'rewu.php?type=video',
                'sbkl.php?type=video',
                'shwd.php?type=video',
                'shejie.php?type=video',
                'tianmei.php?type=video',
                'wmsc.php?type=video',
                'xjj.php?type=video',
                'juhexjj.php?type=video',
                'ksxjjsp.php?type=video',
                'zzxjj.php?type=video',
                'yht.php?type=image',
                'ndym.php?type=video',
                'jpmt.php?type=video',
            ]
            suijiurl = random.choice(urls_list)
            pt_url = 'https://api.yujn.cn/api/' + suijiurl
            try:
                response = requests.head(pt_url, timeout=4)
                if response.status_code != 200:
                    text = "目标不可达!"
                    reply = Reply(ReplyType.ERROR, text)
                    e_context["reply"] = reply
                    e_context.action = EventAction.BREAK_PASS
                headers = {'Content-Type': "application/x-www-form-urlencoded"}
                print(pt_url)  # 打印随机URL地址
                pt_response = requests.get(pt_url, headers=headers, allow_redirects=False, timeout=10)
                pt_response.raise_for_status()
                # 获取重定向后的 URL
                video_url = pt_response.headers.get('location')
                print(video_url)  # 获取真实URL地址
                reply = Reply(ReplyType.VIDEO_URL, video_url)
                # 资源下载到本地
                pic_res = requests.get(video_url, stream=True)
                # 指定本地保存路径及文件名
                print(current_time)
                video_name = f'video_{current_time}.mp4'
                local_video_path = f'E:\\python项目\\chatgpt-on-wechat-master\\download\\video\\{video_name}'  # 替换为实际路径
                print(local_video_path)
                with open(local_video_path, 'wb') as f:
                    size = 0
                    for block in pic_res.iter_content(1024):
                        size += len(block)
                        f.write(block)
            except requests.ConnectionError:
                text = "目标不可达!"
                reply = Reply(ReplyType.ERROR, text)

            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS  # 事件结束，并跳过处理context的默认逻辑
        # return

    def get_help_text(self, **kwargs):
        help_text = "使用方法:\n@ChatGPT 福利视频\n@ChatGPT 福利图片"
        return help_text

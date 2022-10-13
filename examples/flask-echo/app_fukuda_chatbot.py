# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.


import os
import sys
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookParser, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    MemberJoinedEvent, MemberLeftEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton,
    ImageSendMessage
)

channel_access_token = "qkOur4mftIbfdHW/6XO0F5KiUxOiYymXiLMW1gqosMJ7XCTbIc6b1Y7t3oZSWywAKPvbYeFX7aBfWXIgM80+LF9mWeYblLQwWbmtBNtC+CKx1liTJhKRbLpMedmPhJt6X7IaBi7KxF5haSWP8cDTxQdB04t89/1O/w1cDnyilFU="
channel_secret = "133c746968cc0a117cac6ed6ffe428fd"

app = Flask(__name__)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)
handler = WebhookHandler(channel_secret)

#フォローされたとき（友達追加、ブロック解除）の動作

@handler.add(FollowEvent)
def handle_follow(event):
    line_bot_api.reply_message(
        event.reply_token, [
        TextSendMessage(text="はじめまして。私はながれやまはなこです。"),
        TextSendMessage(text="あなたの好きな食べ物はなんですか？")
        ]
    )


#フラグ用の変数を準備
flag_likemeat = False


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # ここをhandlerに変えるとfollowイベントを取得できることはわかった、がそれをすると他のが動かなくなるので一旦放置
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    #ユーザーへのリプライデータ格納先を用意
    def reply_box(SentMessage):

        flag_likemeat = False

    #送られたメッセージと回答を紐付ける

    #質問1
        if SentMessage == "肉":
            tmp_text = ["私も肉が好き！","今度、焼肉行こうね。"]

        if SentMessage == "魚":
            tmp_text = ("そうなんだ！","魚、おいしいよね。")

    #質問2
        if SentMessage == "家で食べる":
            #質問1の回答が肉の場合
            if flag_likemeat:
                tmp_text = ("そうなんだ！","ハンバーグとか？肉、好きなんだもんね。")
            #質問1の回答が魚の場合
            else:
                tmp_text = ("そうなんだ！","焼き魚とか？魚、好きなんだもんね。")

        if SentMessage == "外で食べる":
            #質問1の回答が肉の場合
            if flag_likemeat:
                tmp_text = ("そうなんだ！","え、もしかして焼肉？それなら私も行きたい！")
            #質問1の回答が魚の場合
            else:
                tmp_text = ("そうなんだ！","え、もしかして寿司だったりする？","私、魚べいによく行くよ！")

    #質問3
        if SentMessage == "楽しかった":
            tmp_text = ("嬉しい！","またお話ししようね。")

        if SentMessage == "最悪だった":
            tmp_text = ("そっか・・・","楽しませることができなくて、ごめんね。")

    #戻り値
        return tmp_text


    # if event is MessageEvent and message is TextMessage,以下を実行する

    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        #textsに返信内容を格納
        tmp_text = reply_box(event.message.text)

        #返信内容をアンパック
        if len(tmp_text) == 1:
            text1 = tmp_text

            line_bot_api.reply_message(
                event.reply_token, [
                TextSendMessage(text1)
                ]
       	    )

        if len(tmp_text) == 2:
            text1, text2 = tmp_text
            line_bot_api.reply_message(
                event.reply_token, [
                TextSendMessage(text1),
                TextSendMessage(text2)
                ]
   	        )

        if len(tmp_text) == 3:
            text1, text2, text3 = tmp_text
            line_bot_api.reply_message(
                event.reply_token, [
                TextSendMessage(text1),
                TextSendMessage(text2),
                TextSendMessage(text3)
                ]
   	        )

    return "OK"


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int, default=8080, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
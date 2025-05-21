def find_chatroomid(client, app_id, chatroom_name):
    # 获取好友列表
    print(client)
    fetch_contacts_list_result = client.fetch_contacts_list(app_id)
    if fetch_contacts_list_result.get('ret') != 200 or not fetch_contacts_list_result.get('data'):
        print("获取通讯录列表失败:", fetch_contacts_list_result)
        return
    # {'ret': 200, 'msg': '操作成功', 'data': {'friends': ['weixin', 'fmessage', 'medianote', 'floatbottle', 'wxid_abcxx'], 'chatrooms': ['1234xx@chatroom'], 'ghs': ['gh_xx']}}
    chatrooms = fetch_contacts_list_result['data'].get('chatrooms', [])
    if not chatrooms:
        print("获取到的群列表为空")
        return
    print("获取到的群列表:", chatrooms)

    # 获取群的简要信息
    chatrooms_info = client.get_brief_info(app_id, chatrooms)
    print("获取到的群简要信息:", chatrooms_info)
    if chatrooms_info.get('ret') != 200 or not chatrooms_info.get('data'):
        print("获取群信息失败:", chatrooms_info)
        return
    # {
    #     "ret": 200,
    #     "msg": "获取联系人信息成功",
    #     "data": [
    #         {
    #             "userName": "weixin",
    #             "nickName": "微信团队",
    #             "pyInitial": "WXTD",
    #             "quanPin": "weixintuandui",
    #             "sex": 0,
    #             "remark": "",
    #             "remarkPyInitial": "",
    #             "remarkQuanPin": "",
    #             "signature": null,
    #             "alias": "",
    #             "snsBgImg": null,
    #             "country": "",
    #             "bigHeadImgUrl": "https: //wx.qlogo.cn/mmhead/Q3auHgzwzM6H8bJKHKyGY2mk0ljLfodkWnrRbXLn3P11f68cg0ePxA/0",
    #             "smallHeadImgUrl": "https://wx.qlogo.cn/mmhead/Q3auHgzwzM6H8bJKHKyGY2mk0ljLfodkWnrRbXLn3P11f68cg0ePxA/132",
    #             "description": null,
    #             "cardImgUrl": null,
    #             "labelList": null,
    #             "province": "",
    #             "city": "",
    #             "phoneNumList": null
    #         }
    #     ]
    # }
    
    # 找对目标群的wxid
    chatrooms_info_list = chatrooms_info['data']
    if not chatrooms_info_list:
        print("获取到的群简要信息列表为空")
        return
    chatroom_id = None
    for chatroom_info_list in chatrooms_info_list:
        if chatroom_info_list.get('nickName') == chatroom_name:
            print("找到群:", chatroom_info_list)
            chatroom_id = chatroom_info_list.get('userName')
            break
    if not chatroom_id:
        print(f"没有找到群: {chatroom_name} 的wxid")
        return
    print("找到群:", chatroom_id)
    return chatroom_id
    
    
def find_inspecter(client, app_id, chatroom_id, nickname):

    chatroom_name = None
    wxid = None
    
    # 获取群成员列表
    chatroom_members = client.get_chatroom_member_list(app_id, chatroom_id)
    print("获取到的群成员列表:", chatroom_members)
    memberList = chatroom_members['data']['memberList']
    
    member = None
    for member in memberList:
        print("群成员:", member)
        print("群成员昵称:", member.get('nickName'))
        if member.get('nickName') == nickname:
            wxid = member.get('wxid')
            chatroom_name = member.get('displayName')
            if chatroom_name is None:
                chatroom_name = member.get('nickName')
            break
    return chatroom_name, wxid
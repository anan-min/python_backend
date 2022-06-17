import sys
from json import dumps
from flask import Flask, request
from flask_mail import Mail, Message
from flask_cors import CORS
from src.error import InputError
from src.other import clear_v1
from src import auth, user, users, channel, channels, dm, config, message, admin, standup


def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response


APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# mail config
APP.config['MAIL_SERVER']='smtp.gmail.com'
APP.config['MAIL_PORT'] = 465
APP.config['MAIL_USERNAME'] = 'cs1531tue17cblinker@gmail.com'
APP.config['MAIL_PASSWORD'] = '10J43k834'
APP.config['MAIL_USE_TLS'] = False
APP.config['MAIL_USE_SSL'] = True

mail = Mail(APP)



# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
        raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })


@APP.route("/auth/login/v2", methods=["POST", "GET"])
def auth_login_v2():
    payload = request.get_json()
    result = auth.auth_login_v2(payload["email"], payload["password"])
    return dumps(result)


@APP.route("/auth/register/v2", methods=["POST", "GET"])
def auth_register_v2():
    payload = request.get_json()
    email = payload["email"]
    password = payload["password"]
    name_first = payload["name_first"]
    name_last = payload["name_last"]
    result = auth.auth_register_v2(email,password,name_first,name_last)
    return dumps(result)

@APP.route("/auth/logout/v1", methods=["POST", "GET"])
def auth_logout_v1():
    payload = request.get_json()
    result = auth.auth_logout_v1(payload["token"])
    return dumps(result)


@APP.route("/auth/passwordreset/request/v1", methods=["POST", "GET"])
def auth_passwordreset_request_v1():
    payload = request.get_json()
    email = payload["email"]
    result = auth.auth_passwordreset_request_v1(email)
    reset_code = result["reset_code"]
    msg = Message('DREAM reset password', sender='cs1531tue17cblinker@gmail.com', recipients=[email])
    msg.body = f"this is your reset code: {reset_code}"
    mail.send(msg)
    result = {}
    return dumps(result)


@APP.route("/auth/passwordreset/reset/v1", methods=["POST", "GET"])
def auth_passwordreset_reset_v1():
    payload = request.get_json()
    reset_code, new_password = payload["reset_code"], payload["new_password"]
    result = auth.auth_passwordreset_reset_v1(reset_code, new_password)
    return dumps(result)



@APP.route("/dm/details/v1", methods=["POST", "GET"])
def dm_details_v1():
    payload = request.get_json()
    token, dm_id = payload["token"], payload["dm_id"]
    result = dm.dm_details_v1(token, dm_id)
    return dumps(result)


@APP.route("/dm/list/v1", methods=["POST", "GET"])
def dm_list_v1():
    payload = request.get_json()
    token = payload["token"]
    result = dm.dm_list_v1(token)
    return dumps(result)


@APP.route("/dm/create/v1", methods=["POST", "GET"])
def dm_create_v1():
    payload = request.get_json()
    token, u_ids = payload["token"], payload["u_ids"]
    result = dm.dm_create_v1(token, u_ids)
    return dumps(result)


@APP.route("/dm/remove/v1", methods=["POST", "DELETE", "GET"])
def dm_remove_v1():
    payload = request.get_json()
    token, dm_id = payload["token"], payload["dm_id"]
    result = dm.dm_remove_v1(token, dm_id)
    return dumps(result)


@APP.route("/dm/invite/v1", methods=["POST", "GET"])
def dm_invite_v1():
    payload = request.get_json()
    token, dm_id, u_ids = payload["token"], payload["dm_id"], payload["u_ids"]
    result = dm.dm_invite_v1(token, dm_id, u_ids)
    return dumps(result)


@APP.route("/dm/remove/v1", methods=["POST", "GET"])
def dm_leave_v1():
    payload = request.get_json()
    token, dm_id = payload["token"], payload["dm_id"]
    result = dm.dm_leave_v1(token, dm_id)
    return dumps(result)


@APP.route("/dm/messages/v1", methods=["POST", "GET"])
def dm_messages_v1():
    payload = request.get_json()
    token, dm_id, start = payload["token"], payload["dm_id"], payload["start"]
    result = dm.dm_messages_v1(token, dm_id, start)
    return dumps(result)

@APP.route('/dm/leave/v1', methods=['POST'])
def dm_leave():
    payload = request.get_json()
    token, dm_id = payload['token'], payload['dm_id']
    result = dm.dm_leave_v1(token, dm_id)
    return dumps(result)

@APP.route("/user/profile/v2", methods=["GET"])
def user_profile_v2():
    payload = request.get_json()
    result = user.user_profile_v2(payload['token'], payload['u_id'])
    return dumps(result)

@APP.route("/user/profile/setname/v2", methods=["PUT"])
def user_setname_v2():
    payload = request.get_json()
    name_first = request.args.get('first')
    name_last = request.args.get('last')
    result = user.user_profile_setname_v2(payload['token'], name_first, name_last)
    return dumps(result)

@APP.route("/user/profile/setemail/v2", methods=["PUT"])
def user_setemail_v2():
    payload = request.get_json()
    email = request.args.get('email')
    result = user.user_profile_setemail_v2(payload['token'], email)
    return dumps(result)

@APP.route("/user/profile/sethandle/v1", methods=["PUT"])
def user_sethandle_v1():
    payload = request.get_json()
    handle = request.args.get('handle')
    result = user.user_profile_sethandle_v1(payload['token'], handle)
    return dumps(result)

@APP.route('/user/profile/uploadphoto/v1', methods=['POST'])
def set_photo():
    payload = request.get_json()
    result = user.user_profile_uploadphoto_v1(payload['token'], payload['img_url'], payload['x_start'], payload['y_start'], payload['x_end'], payload['y_end'])
    return dumps(result)

@APP.route("/user/stats/v1", methods=['GET'])
def get_user_stats():
    payload = request.get_json()
    result = user.user_stats_v1(payload['token'])
    return dumps(result)

@APP.route("/users/all/v2", methods=["GET"])
def users_all_v2():
    payload = request.get_json()
    result = users.users_all_v1(payload['token'])
    return dumps(result)

@APP.route('/users/stats/v1', methods=['GET'])
def get_dream_stats():
    payload = request.get_json()
    result = users.users_stats_v1(payload['token'])
    return dumps(result)

@APP.route("/channel/invite/v2", methods=["POST", "GET"])
def channel_invite_v2():
    payload = request.get_json()
    token, channel_id, u_id = payload["token"], payload["channel_id"], payload["u_id"]
    result = channel.channel_invite_v2(token, channel_id, u_id)
    return dumps(result)


@APP.route("/channel/details/v2", methods=["POST", "GET"])
def channel_details_v2():
    payload = request.get_json()
    token, channel_id = payload["token"], payload["channel_id"]
    result = channel.channel_details_v2(token, channel_id)
    return dumps(result)


@APP.route("/channel/messages/v2", methods=["POST", "GET"])
def channel_messages_v2():
    payload = request.get_json()
    token, channel_id, start = payload["token"], payload["channel_id"], payload["start"]
    result = channel.channel_messages_v2(token, channel_id, start)
    return dumps(result)


@APP.route("/channel/join/v2", methods=["POST", "GET"])
def channel_join_v2():
    payload = request.get_json()
    token, channel_id = payload["token"], payload["channel_id"]
    result = channel.channel_join_v2(token, channel_id)
    return dumps(result)


@APP.route("/channel/addowner/v1", methods=["POST", "GET"])
def channel_addowner_v1():
    payload = request.get_json()
    token, channel_id, u_id = payload["token"], payload["channel_id"], payload["u_id"]
    result = channel.channel_addowner_v1(token, channel_id, u_id)
    return dumps(result)


@APP.route("/channel/removeowner/v1", methods=["POST", "GET"])
def channel_removeowner_v1():
    payload = request.get_json()
    token, channel_id, u_id = payload["token"], payload["channel_id"], payload["u_id"]
    result = channel.channel_removeowner_v1(token, channel_id, u_id)
    return dumps(result)


@APP.route("/channel/leave/v1", methods=["POST", "GET"])
def channel_leave_v1():
    payload = request.get_json()
    token, channel_id = payload["token"], payload["channel_id"]
    result = channel.channel_leave_v1(token, channel_id)
    return dumps(result)

@APP.route("/message/send/v2", methods=["POST", "GET"])
def message_send_v2():
    payload = request.get_json()
    token, channel_id, message_txt = payload["token"], payload["channel_id"], payload["message"]
    result = message.message_send_v2(token, channel_id, message_txt)
    return dumps(result)

@APP.route("/message/senddm/v1", methods=["POST", "GET"])
def message_senddm_v2():
    payload = request.get_json()
    token, dm_id, message_txt = payload["token"], payload["dm_id"], payload["message"]
    result = message.message_senddm_v1(token, dm_id, message_txt)
    return dumps(result)

@APP.route("/message/edit/v2", methods=["POST", "GET", "PUT"])
def message_edit_v2():
    payload = request.get_json()
    token, message_id, message_txt = payload["token"], payload["message_id"], payload["message"]
    result = message.message_edit_v2(token, message_id, message_txt)
    return dumps(result)

@APP.route("/message/remove/v1", methods=["POST", "GET", "DELETE"])
def message_remove_v1():
    payload = request.get_json()
    token, message_id = payload["token"], payload["message_id"]
    result = message.message_remove_v1(token, message_id)
    return dumps(result)

@APP.route("/message/share/v1", methods=["POST", "GET"])
def message_share_v1():
    payload = request.get_json()
    token, message_id, message_txt = payload["token"], payload["message_id"], payload["message"]
    channel_id, dm_id = payload["channel_id"], payload["dm_id"]
    result = message.message_share_v1(token, message_id, message_txt, channel_id, dm_id)
    return dumps(result)

@APP.route("/message/sendlater/v1", methods=["POST", "GET"])
def message_sendlater_v1():
    payload = request.get_json()
    token, channel_id, message_txt, time_sent = payload["token"], payload["channel_id"], payload["message"], payload["time_sent"]
    result = message.message_sendlater_v1(token, channel_id, message_txt, time_sent)
    return dumps(result)

@APP.route("/message/sendlaterdm/v1", methods=["POST", "GET"])
def message_sendlaterdm_v1():
    payload = request.get_json()
    token, dm_id, message_txt, time_sent = payload["token"], payload["dm_id"], payload["message"], payload["time_sent"]
    result = message.message_sendlaterdm_v1(token, dm_id, message_txt, time_sent)
    return dumps(result)

@APP.route("/channels/list/v2", methods=["POST", "GET"])
def channels_list_v1():
    payload = request.get_json()
    token = payload["token"]
    result = channels.channels_list_v2(token)
    return dumps(result)

@APP.route("/channels/listall/v2", methods=["POST", "GET"])
def channels_listall_v2():
    payload = request.get_json()
    token = payload["token"]
    result = channels.channels_listall_v2(token)
    return dumps(result)

@APP.route("/channels/create/v2", methods=["POST", "GET"])
def channels_create_v2():
    payload = request.get_json()
    token, name, is_public = payload["token"], payload["name"], payload["is_public"]
    result = channels.channels_create_v2(token, name, is_public)
    return dumps(result)

@APP.route("/standup/start/v1", methods = ["POST", "GET"])
def standup_start_v1():
    payload = request.get_json()
    token, channel_id, length = payload["token"], payload["channel_id"], payload["length"]
    result = standup.standup_start_v1(token, channel_id, length)
    return dumps(result)

@APP.route("/standup/active/v1", methods = ["POST", "GET"])
def standup_active_v1():
    payload = request.get_json()
    token, channel_id = payload["token"], payload["channel_id"]
    result = standup.standup_active_v1(token, channel_id)
    return dumps(result)

@APP.route("/standup/send/v1", methods = ["POST", "GET"])
def standup_send_v1():
    payload = request.get_json()
    token, channel_id, message = payload["token"], payload["channel_id"], payload["message"]
    result = standup.standup_send_v1(token, channel_id, message)
    return dumps(result)

if __name__ == "__main__":
    clear_v1()
    APP.run(port=config.port) # Do not edit this port



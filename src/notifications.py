'''Importing functions'''
from src.utils import load_data, save_data, token_to_id

def notifications_get_v1(token):
    '''
    :param token:
    :param dm_id:
    :return:
    '''
    """ Returns a list of users 20 most recent notifications """
    data = load_data()
    uid = token_to_id(token)
    data_notifications = data['notifications']

    return {'notifications': data_notifications[uid][0:20]}


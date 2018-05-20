from services.common import DatabaseService
from common.database import Db
from services.message import MessageService
from services.user import UserService
from model.placeholder import Placeholder
from model.user_message_mapping import UserMessageMapping
from flask_login import current_user

class MailService(DatabaseService):
    def compose(self, dict):
        with Db.get() as self._db:

            sender = UserService().get_by_email(dict['sender_email'])


            #add message
            message_dict = MessageService().convert_to_message_dict(dict)
            message_object = MessageService().add(message_dict)

            dict['message_id'] = message_object.id

            #add mapping of sender with placeholder as Sent Mail
            dict['user_id'] = sender["id"]
            MessageService().add_user_message_mapping( dict, 'sent_mail')

            #add mapping of recipient with placeholder as Inbox
            to_emails = dict['recipient_email'].split(',')
            for email in to_emails:
                recipient = UserService().get_by_email(email)
                dict['user_id'] = recipient["id"]
                MessageService().add_user_message_mapping( dict, 'inbox')

            return message_dict

    def delete(self, mapping_id):
        with Db.get() as self._db:
            #update the user message mapping by updating the placeholder as trash
            placeholder = Placeholder.get_by_name(self._db, 'trash')
            return MessageService().update_user_message_mapping(mapping_id,{'placeholder_id':placeholder.id})

    def save_to_drafts(self, dict):
        with Db.get() as self._db:
            sender = UserService().get_by_email(dict['sender_email'])


            #add message
            message_dict = MessageService().convert_to_message_dict(dict)
            message_object = MessageService().add(message_dict)

            dict['message_id'] = message_object.id

            #add mapping of sender with placeholder as Sent Mail
            dict['user_id'] = sender["id"]
            MessageService().add_user_message_mapping( dict, 'drafts')

            return message_dict
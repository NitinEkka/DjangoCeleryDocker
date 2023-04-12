import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_management.settings')
django.setup()
from rocketchat_API.rocketchat import RocketChat
from inventory_app.models import RocketChatConversation
import time
from inventory_app.signals import rocket_logger

while True:
    time.sleep(5)
    print("Started")
    rocket = RocketChat('nitin.ekka30', '1234567@', server_url='https://wireone.rocket.chat/')
    json_data = rocket.channels_history('GENERAL', count=5).json()
    log_items = RocketChatConversation.objects.all()

    if log_items.exists():
        latest_object_on_db = RocketChatConversation.objects.latest('id')
        latest_message_on_db = latest_object_on_db.text
        latest_message = json_data['messages'][0]['msg']
        if latest_message_on_db != latest_message:
            try:    
                rocket_logger.send(sender=None)
            except:
                pass
        else:
            pass
    else:
        latest_message = json_data['messages'][0]['msg']
        sender_name = json_data['messages'][0]['u']['username']
        created_time = json_data['messages'][0]['_updatedAt']
        print(latest_message_on_db)
        print(latest_message)
        RocketChatConversation.objects.create(text=latest_message,sender=sender_name,created_at=created_time)
        print(f"First Entry of {latest_message} by {sender_name} is done")

    
    
    
    
from django.dispatch import Signal
from django.dispatch import receiver
from .models import Inventory, User
from django.core import serializers
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .models import EmailLog
import json
from rocketchat_API.rocketchat import RocketChat
from .models import RocketChatConversation

threshold_signal = Signal()

@receiver(threshold_signal)
def check_threshold(sender, **kwargs):
    
    threshold = 10
    # items = Inventory.objects.filter(quantity__lte=threshold)
    farm_list_threshold = Inventory.objects.filter(quantity__lte=threshold).values_list('farm', flat=True)
    print(f"{farm_list_threshold} farm list threshold")
    cleaned_farm_list = [*set(farm_list_threshold)]
    print(f"{cleaned_farm_list} cleaned farm list")
    for farm in cleaned_farm_list:
        print(f"{farm}")
        email_querry = EmailLog.objects.filter(farm=farm)
        if email_querry.exists():
            items = Inventory.objects.filter(quantity__lte=threshold, farm=farm)
            list_farm_executive = []
            executive = User.objects.filter(role='farmexecutive', farm=farm)
            for user in executive:
                list_farm_executive.append(user.email)
            context = {'data': items, 'farm':farm}
            email_body = render_to_string('inventory_app/threshold.html', context)
            html_content = email_body
            latest_email_object = EmailLog.objects.filter(farm=farm).latest('id')
            latest_body = latest_email_object.body
            latest_receiver = latest_email_object.receiver
        
            jsonDec = json.decoder.JSONDecoder()
            latest_receiver_list = jsonDec.decode(latest_receiver)

            new_list_reciever = set(list_farm_executive) - set(latest_receiver_list)
            print(new_list_reciever)
            #new_list_reciever = list()
            if len(new_list_reciever)>0:

                if latest_body==email_body:
                    msg = EmailMultiAlternatives('Threshold Alert', 'This is HTML version', 'nitin.ekka30@gmail.com',new_list_reciever)
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()

                    email_receiver_json = json.dumps(list(list_farm_executive))

                    email_log = EmailLog.objects.create(body=email_body, receiver=email_receiver_json, farm=farm)
                    email_log.save()

                    # send body with new receiver
                else:
                    msg = EmailMultiAlternatives('Threshold Alert', 'This is HTML version', 'nitin.ekka30@gmail.com',list_farm_executive)
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()

                    email_receiver_json = json.dumps(list(list_farm_executive))

                    email_log = EmailLog.objects.create(body=email_body, receiver=email_receiver_json, farm=farm)
                    email_log.save()

                    # send new body with all
            else:
                if latest_body==email_body:
                    pass
                else:
                    msg = EmailMultiAlternatives('Threshold Alert', 'This is HTML version', 'nitin.ekka30@gmail.com',list_farm_executive)
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
                
                    email_receiver_json = json.dumps(list_farm_executive)
       
                    email_log = EmailLog.objects.create(body=email_body, receiver=email_receiver_json, farm=farm)
                    email_log.save()


            
        else:
            items = Inventory.objects.filter(quantity__lte=threshold, farm=farm)
            list_farm_executive = []
            executive = User.objects.filter(role='farmexecutive', farm=farm)
            for user in executive:
                list_farm_executive.append(user.email)
            context = {'data': items, 'farm':farm}
            email_body = render_to_string('inventory_app/threshold.html', context)
            html_content = email_body
            print(html_content)
            print(type(html_content))
            msg = EmailMultiAlternatives('Threshold Check', 'This is HTML version', 'nitin.ekka30@gmail.com',list_farm_executive)
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            email_querry = EmailLog.objects.all()
            email_receiver_json = json.dumps(list_farm_executive)
       
            email_log = EmailLog.objects.create(body=email_body, receiver=email_receiver_json, farm=farm)
            email_log.save()
    
rocket_logger = Signal()

@receiver(rocket_logger)
def rocketchat_logger(sender, **kwargs):
    print("Signal Started")
    rocket = RocketChat('nitin.ekka30', '1234567@', server_url='https://wireone.rocket.chat/')
    json_data = rocket.channels_history('GENERAL', count=5).json()
    latest_object_on_db = RocketChatConversation.objects.latest('id')
    latest_message_on_db = latest_object_on_db.text
    latest_message = json_data['messages'][0]['msg']
    if latest_message_on_db != latest_message:
        current_msg = json_data['messages'][0]['msg']
        sender_name = json_data['messages'][0]['u']['username']
        created_time = json_data['messages'][0]['_updatedAt']
        RocketChatConversation.objects.create(text=current_msg,sender=sender_name,created_at=created_time)
        print("Signal Successfully inserted the entry")
        print(current_msg)
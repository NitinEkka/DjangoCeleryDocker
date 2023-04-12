from celery import shared_task
from django.core.mail import send_mail
from .models import Inventory, User
from django.core import serializers
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from rocketchat_API.rocketchat import RocketChat
import json
from .models import RocketChatConversation, Farm
from django.core.mail import EmailMultiAlternatives
from .celery import app
from datetime import datetime, timedelta

# @shared_task
# def check_threshold():
#     threshold = 10
#     items = Inventory.objects.filter(quantity__lte=threshold)
#     if items:
#         less_json_data = serializers.serialize('json', items)
#         list_farm_executive = []
#         executive = User.objects.filter(role='farmexecutive')
#         for user in executive:
#             list_farm_executive.append(user.email)
#         context = {'data': less_json_data}
#         email_body = render_to_string('inventory_app/daily_report.html', context)
#         email = EmailMessage(
#                             'Inventory Daily Report', 
#                             email_body, 
#                             'nitin.ekka30@gmail.com',  
#                             list_farm_executive,  
#                             )
#         email.send()

#@app.task(queue='queue')
@shared_task
def daily_report():
    task_id = datetime.now().strftime('%Y%m%d%H%M%S%f')
    last_executed = daily_report.AsyncResult(task_id).date_done
    if last_executed is not None and (datetime.now() - last_executed).total_seconds() < 60:
        return "Task already executed successfully earlier"
    else:
        farm_list = Inventory.objects.values_list('farm', flat=True)
        cleaned_farm_list = [*set(farm_list)]
        print(cleaned_farm_list)
        for farm in cleaned_farm_list:
            list_farm_executive = []
            #farm_name_object = Farm.objects.get(farm=farm)
            #farm_name = farm_name_object.farm_name
            executive = User.objects.filter(role='farmexecutive', farm=farm)
        
            for user in executive:
                list_farm_executive.append(user.email)
        
            all_inventory = Inventory.objects.filter(farm=farm)
        
            farm_object = Farm.objects.get(farm_id=farm)
            farm_name = farm_object.farm_name
            context = {'data': all_inventory, 'farm': farm_name}
            email_body = render_to_string('inventory_app/daily_report.html', context)
            html_content = email_body
        
            msg = EmailMultiAlternatives('Daily Report', 'This is HTML version', 'nitin.ekka30@gmail.com',list_farm_executive)
            msg.attach_alternative(html_content, "text/html")
            msg.send()

@shared_task
def rocket_start():
    rocket = RocketChat('nitin.ekka30', '1234567@', server_url='https://wireone.rocket.chat/')
    json_data = rocket.channels_history('GENERAL', count=5).json()
    initial_msg = json_data['messages'][0]['msg']
    sender_name = json_data['messages'][0]['u']['username']
    created_time = json_data['messages'][0]['_updatedAt']
    RocketChatConversation.objects.create(text=initial_msg,sender=sender_name,created_at=created_time)

# @app.task()
# def rocket_message_log():
#     rocket = RocketChat('nitin.ekka30', '1234567@', server_url='https://wireone.rocket.chat/')
#     json_data = rocket.channels_history('GENERAL', count=5).json()
#     latest_object_on_db = RocketChatConversation.objects.latest('id')
#     latest_message_on_db = latest_object_on_db.text
#     latest_message = json_data['messages'][0]['msg']
#     if latest_message_on_db != latest_message:
#         current_msg = json_data['messages'][0]['msg']
#         sender_name = json_data['messages'][0]['u']['username']
#         created_time = json_data['messages'][0]['_updatedAt']
#         RocketChatConversation.objects.create(text=current_msg,sender=sender_name,created_at=created_time)   

#     print(f"latest_message_on_db {latest_message_on_db}")
#     print(f"latest_message {latest_message}")
    # app.send_task("rocket_message_log", queue="queue1")
      
# app.send_task("rocket_message_log", queue="queue1")


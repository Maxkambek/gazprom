import requests


def verify(phone):
    url = "http://notify.eskiz.uz/api/message/sms/send"
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDI0ODQ0NDMsImlhdCI6MTY5OTg5MjQ0Mywicm9sZSI6InVzZXIiLCJzdWIiOiIxMDUzIn0.UzXB5cWC0vANpL-fEicXZVMQIjLOab7bbCZ0rZQfXqo"}
    data = {
        'mobile_phone': phone,
        'message': f"Buyurtmangizni ko'rishingiz uchun link - localhost:5173/login-client \n Loginingiz: {phone} \n Paroliningiz: 12345678",
        'from': "4546",
        'callback_url': 'http://0.0.0.0.uz/test.php'
    }

    response = requests.post(url=url, data=data, headers=headers)
    return response

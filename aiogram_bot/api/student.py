# import requests
# from data.config import BASE_URL


# def get_student(chat_id):
#     response = requests.get(f'{BASE_URL}/api/student/get/{chat_id}')
#     return response


# def create_student(telegramId, fullname, school, class_, phone, direction):
#     data = {
#         "telegramId": telegramId,
#         "fullname": fullname,
#         "school": school,
#         "class": class_,
#         "phone": phone,
#         "direction": direction
#     }
#     response = requests.post(f'{BASE_URL}/api/student/register', data=data)
#     return response
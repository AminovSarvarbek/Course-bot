from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import User


class UserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('full_name','group_name','monthly_payment','number','day_of_registration','school','user_class','telegram_id','status')

class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('full_name','group_name','monthly_payment','number','day_of_registration','school','user_class','status')

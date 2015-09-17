from django.forms import ModelForm, PasswordInput
from django.contrib.auth.models import User
from django.forms.models import model_to_dict, fields_for_model

from models import UserProfile


class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']

    def __init__(self, instance=None, *args, **kwargs):
        _fields = ('username', )
        _initial = model_to_dict(instance.user, _fields) if instance is not None else {}
        super(ProfileForm, self).__init__(initial=_initial, instance=instance, *args, **kwargs)
        self.fields.update(fields_for_model(User, _fields))

    def save(self, *args, **kwargs):
        user = self.instance.user
        user.username = self.cleaned_data['username']
        #user.set_password(self.cleaned_data['password'])
        user.save()
        profile = super(ProfileForm, self).save(*args, **kwargs)
        return profile

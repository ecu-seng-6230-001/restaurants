from django import forms
from general.validators import validateName, validateEmail, validatePassword
from django.forms.utils import ErrorList



class DivErrorList(ErrorList):
	def __str__(self):
		return self.as_divs()
	def as_divs(self):
		if not self:
			return ''
		return '<div class="errorlist">%s</div>' % ''.join(['<div class="error font_size_07 text-danger">%s</div>' % e for e in self])



class AccountUpdate(forms.Form):
	name = forms.CharField(
		max_length = 128, label="", validators=[validateName],
		widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
	)

class AccountLogin(forms.Form):
	username = forms.CharField(
		label="",
		widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
	)
	password = forms.CharField(
		label='',
		widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
	)

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		from accounts.models import Account
		if Account.objects.filter(username=username).exists():
			account = Account.objects.get(username=username)
			if not account.check_password(raw_password=password):
				raise forms.ValidationError("Password didn't match.")
		else:
			raise forms.ValidationError("Username couldn't found.")
		return super(AccountLogin, self).clean(*args, **kwargs)


class AccountRegistration(forms.Form):
	name = forms.CharField(
		max_length = 128, label="", validators=[validateName],
		widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name', 'id': 'name'}),
		help_text="example: John Doe"
	)
	password = forms.CharField(
		label='', validators=[validatePassword],
		widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'id': 'password'}),
		help_text='example: hiji&@#biji28^#'
	)



class PasswordChange(forms.Form):
	old_password = forms.CharField(
		label="",
		widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Current password'}),
	)
	new_password = forms.CharField(
		label='',
		widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New password'}),
	)
	re_password  = forms.CharField(
		label='',
		widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}),
	)
	def __init__(self, userObj, *args, **kwargs):
		self.userObj = userObj
		super(PasswordChange, self).__init__(*args, **kwargs)

	def clean(self, *args, **kwargs):
		old_password = self.cleaned_data.get('old_password')
		new_password = self.cleaned_data.get('new_password')
		re_password  = self.cleaned_data.get('re_password')
		if not self.userObj.check_password(raw_password=old_password):
			raise forms.ValidationError("Incorrect current password.")
		if new_password != re_password:
			raise forms.ValidationError("New and confirm password didn't match.")
		if len(new_password) < 6 or len(re_password) < 6:
			raise forms.ValidationError("Password is too small.")
		if new_password == old_password:
			raise forms.ValidationError("The password you are trying to change is already your current password.")
		return super(PasswordChange, self).clean(*args, **kwargs)

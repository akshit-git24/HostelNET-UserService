from django.shortcuts import render
import random
import string
# Create your views here.
def generate_uni_id(role):
    role_lower = role.lower()
    if role_lower == "university":
       return 'UNI' + ''.join(random.choices(string.digits, k=6))
    elif role_lower == "student":
       return 'STD' + ''.join(random.choices(string.digits, k=12))
    elif role_lower == "hostel":
       return 'HST' + ''.join(random.choices(string.digits, k=10))

from django.shortcuts import render, redirect
from .models import Image, Like
from django.db.models.aggregates import Sum
from django.db.models import Count
from django.db.models import F
from django.contrib.auth.models import User
from collections import Counter
import itertools

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
def index(request):
    '''
    return template and dict of image url and number of people who liked it
    '''
    images = Image.objects.all()
    likes = Like.objects.all()

    like = Like.objects.all().values('image__image') #dict of image=>url and user=>id
    images = [ item.get('image__image') for item in like]
    image_with_count = Counter(images)

    image_with_like_num_dict = {}
    image_with_like_num_list = []
    for key in dict(image_with_count):
        image_with_like_num_dict['image']=key
        image_with_like_num_dict['num']=image_with_count.get(key)
        image_with_like_num_list.append(image_with_like_num_dict)
        image_with_like_num_dict = {}
    print(image_with_like_num_list)

    dictfilt = lambda x, y: dict( [ (i,x[i]) for i in x if i in set(y) ] ) #pick spacific key in this context (image_image)
    
    user_count = User.objects.all().count()
    print(image_with_like_num_list)
    context = {
        'user_count':user_count,
        'images':image_with_like_num_list,
    }
    return render(request, 'like_action/index.html', context )

# list_of_images = []
# for item in like.iterator():
#     dict_of_images = dictfilt(item, ('image__image',) ) #key:value of what you want
#     list_of_images.append(dict_of_images)
# print(list_of_images)


# urls = [ url for item in like for url in dict_of_images.values()]#list of image url 
# urls_with_count = Counter(urls)#list of image url and counter them

# image_with_like_num_dict = {}
# image_with_like_num_list = []
# for key in dict(urls_with_count):
#     image_with_like_num_dict['image'] = key
#     image_with_like_num_dict['num'] = urls_with_count.get(key)
#     image_with_like_num_list.append(image_with_like_num_dict)

# print(image_with_like_num_list)



def update(request, pk):
    if request.method == 'GET':
        image = Image.objects.filter(pk=pk).first()
        context = {
            'image':image,
        }
        return render(request, 'like_action/update.html',context )
    elif request.method == 'POST':
        image = Image.objects.filter(pk=pk)
        name = request.POST.get('name')
        description = request.POST.get('description')
        file = request.FILES.get('file')
        print(file)
        user = request.user

        image.update(name=name,description=description, user=user, image=file)
        
        return redirect('like:index')



def signup(request):
    user_count = User.objects.all().count()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('like:signup')
    else:
        form = UserCreationForm()
    return render(request, 'like_action/signup.html', {'form': form, 'user_count':user_count})

def counter(request):
    users = User.objects.count()
    return render(request, 'like_action/all_user.html',{'users':users})
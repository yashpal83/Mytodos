from django.shortcuts import redirect, render, HttpResponse
from todo.models import Todo, Contact
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def home(request):         
    if request.method == "POST":
        title = request.POST['title']
        desc = request.POST['desc']
        user = request.user
        today = datetime.now()
        dt = today.strftime("%d-%b-%Y / %H:%M:%S") 
        todo = Todo(title = title, desc = desc, datetime = dt, user = user)
        todo.save()
    
    if request.user.is_authenticated:
        user = request.user
        todos = Todo.objects.filter(user = user)
        content = {'todos': todos}
        return render(request, 'home.html', content)
      
    else:
        return render(request, 'home.html')
    


def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == "POST":
        
        name = request.POST['name']
        email = request.POST['email']
        today = datetime.now()
        dt = today.strftime("%d-%b-%Y / %H:%M:%S")
        city = request.POST['city']
        state = request.POST['state']
        desc = request.POST['desc']


        if len(name) < 3 or len(email) < 4 or len(city) < 4 or len(state) <= 3 or len(desc) < 4:
            messages.warning(request, "Please enter the details correctly.")

        else:

            contact = Contact(name = name, email = email, datetime = dt, city = city, state = state, desc = desc)        
            contact.save()
            messages.success(request, "Your message has been successully sent.")
            
            return redirect("/contact")
        
    return render(request, 'contact.html')  


def delete(request, num):
    todo = Todo.objects.get(num = num)
    todo.delete()
    
    return redirect("/")

def update(request, num):
    
    if request.method == "POST":
        title = request.POST['title']
        desc = request.POST['desc']
        today = datetime.now()
        dt = today.strftime("%d-%b-%Y / %H:%M:%S")

        todo = Todo.objects.get(num = num)
        todo.title = title
        todo.desc = desc
        todo.datetime = dt
        todo.save()
        
        return redirect("/")
    
    todo = Todo.objects.get(num = num)
    content = {'todo': todo}
    return render(request, 'update.html', content)
    
def search(request):
    word = request.GET['todosearch']

    if word == "":
        messages.warning(request, "Enter something in search box.")
        todos = []

    if len(word) > 20:
        messages.warning(request, "Please Search in limited words.")
        todos = []

    if request.user.is_authenticated:
        user = request.user
        todotitle = Todo.objects.filter(user = user, title__icontains = word)
        tododesc = Todo.objects.filter(user = user, desc__icontains = word)
        tododate = Todo.objects.filter(user = user, datetime__icontains = word)
        todos = todotitle.union(tododesc)
        todos = todos.union(tododate)
        content = {'todos':todos, 'word':word}
    
    else:
        content = {}
        
    return render(request, 'search.html', content)


def handlesignup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']


        if User.objects.filter(username = username).exists():
            messages.warning(request, "This username already exists, Please choose another username.")
            return redirect("/")

        if not username.isalnum():
            messages.warning(request, "Username should be alpha numeric (numbers and letters)")
            return redirect('/')
            
        if not username.islower():
            messages.warning(request, "Username should be in lowercase.")
            return redirect("/")
        
        
        if len(username) > 10:
            messages.warning(request, "Username should be less than 10 characters.")
            return redirect("/")

        if password1 != password2:
            messages.warning(request, "Passsword did not match.")
            return redirect("/")

        user = User.objects.create_user(username, email, password1)
        user.first_name = fname
        user.last_name = lname
        user.save()
        messages.success(request, "Your account has been successfully created.")
        return redirect("/")
    
    
    else:
        return HttpResponse("404: Error")




def handlelogin(request):
    if request.method == "POST":
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(request, username = loginusername, password = loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, "You are successfully Logged In.")
            return redirect("/")
        else:
            messages.warning(request, "Bad Credentials, Please try again.")
            return redirect("/")
    
    else:
        return HttpResponse("404 : Error")

def handlelogout(request):
    logout(request)
    messages.success(request, "You are successfully Logged Out.")
    return redirect("/")

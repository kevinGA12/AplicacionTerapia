from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import Sessions, Categories, Posts, Threads, Profiles, Resources
from .forms import therapyForm, LoginForm, NewThreadForm, NewPostForm, ProfileForm, ResourceForm


# Create your views here.

def log_in(request):
    form = LoginForm(request.POST or None)
    context = {'message': None, 'form': form}
    if request.POST and form.is_valid():
        user = authenticate(**form.cleaned_data)
        if user is not None:
            if user.is_active:
                login(request, user)

                profile, created = Profiles.objects.get_or_create(
                    user=user,
                    defaults={'username': user.username, 'user_id': user.id, 'age': 0, 'therapycount': 0, 'wellbeing': 0, 'currentmood': '', 'stresslevel': 0, 'anxietylevel': 0}
                )
                
                return redirect('therapy:home')
            else:
                context['message'] = 'El usuario ha sido desactivado'
        else:
            context['message'] = 'Usuario o contraseña incorrecta'
    return render(request, 'therapy/login.html', context)


# decorador para restringir el acceso a solo usuarios autenticados
@login_required
def log_out(request):
    logout(request)
    return redirect('therapy:log-in')


@login_required
def session_list(request):
    therapy = Sessions.objects.all()
    return render(request, 'therapy/index.html', {'therapy': therapy})


@login_required
def session_detail(request, pk):
    try:
        # recuperamos el objeto mediante la
        # API de abstracción de base de datos
        # que ofrece Django
        m = Sessions.objects.get(pk=pk)
    except Sessions.DoesNotExist:
        raise Http404("Esta sesion no está agendada")

    # version con shortcuts de django, equivalente al codigo anterior
    # m = get_object_or_404(therapy, pk=pk)
    return render(request, 'therapy/detail.html', {'session': m})

@login_required
def session_create(request):
    if request.method == 'POST':
        form = therapyForm(request.POST, request.FILES)
        if form.is_valid():
            new_session = form.save(commit=False)
            new_session.user_id = request.user.id
            new_session.name = request.user.username
            new_session.save()
            form.save_m2m()
            return redirect('therapy:home')
    else:
        form = therapyForm()
    return render(request, 'therapy/form.html', {'form': form})


@login_required
def session_update(request, **kwargs):
    # recuperamos el objeto a actualizar
    session = Sessions.objects.get(pk=kwargs.get('pk'))
    # inicializamos el formulario con el objeto recuperado
    form = therapyForm(
        request.POST or None,
        instance=session
    )
    if request.POST and form.is_valid():
        form.save()
        return redirect('therapy:home')
    return render(request, 'therapy/form.html', {'form': form})


@login_required
def session_delete(request, **kwargs):
    session = Sessions.objects.get(pk=kwargs.get('pk'))
    session.delete()
    return redirect('therapy:home')

@login_required
def thread_reply(request, pk):
    thread = get_object_or_404(Threads, pk=pk)
    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.thread = thread  
            post.user = request.user  
            post.save()
            return redirect('therapy:thread-detail', pk=thread.pk)
    else:
        form = NewPostForm()
    return render(request, 'therapy/therapy/thread_reply.html', {'form': form, 'thread': thread})

@login_required
def thread_update(request, pk):
    thread = get_object_or_404(Threads, pk=pk)

    if request.user.id != thread.user_id:
        return HttpResponseForbidden("You are not allowed to edit this thread.")
    if request.method == 'POST':
        form = NewThreadForm(request.POST, request.FILES, instance=thread)
        if form.is_valid():
            form.save()
            return redirect('therapy:thread-detail', pk=thread.pk)  
    else:
        form = NewThreadForm(instance=thread)
    return render(request, 'therapy/therapy/thread_edit.html', {'form': form})

@login_required
def thread_delete(request, **kwargs):
    thread_id = kwargs.get('pk')
    thread = Threads.objects.get(pk=thread_id)

    if request.user.id != thread.user_id:
        return HttpResponseForbidden("You are not allowed to delete this thread.")

    Posts.objects.filter(thread_id=thread_id).delete()

    thread.delete()
    return redirect('therapy:therapy-forums')

@login_required
def therapy_request(request):
    therapies = Sessions.objects.all()
    return render(request, 'therapy/therapy/therapy_request.html', {'therapies': therapies})

@login_required
def therapy_forums(request):
    threads = Threads.objects.all()
    return render(request, 'therapy/therapy/therapy_forums.html', {'threads': threads})

@login_required
def therapy_resources(request):
    resources = Resources.objects.all()
    return render(request, 'therapy/therapy/therapy_resources.html', {'resources': resources})

@login_required
def resource_create(request):
    form = ResourceForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            new_resource = form.save(commit=False)
            new_resource.user_id = request.user.id
            new_resource.save()
            return redirect('therapy:therapy-resources')
    return render(request, 'therapy/therapy/resource_create.html', {'form': form})

@login_required
def resource_edit(request, pk):
    resource = get_object_or_404(Resources, pk=pk)
    if request.user.id != resource.user_id:
        return HttpResponseForbidden("You are not allowed to edit this resource.")
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES, instance=resource)
        if form.is_valid():
            form.save()
            return redirect('therapy:therapy-resources')
    else:
        form = ResourceForm(instance=resource)
    return render(request, 'therapy/therapy/resource_edit.html', {'form': form, 'resource': resource})

@login_required
def resource_delete(request, **kwargs):
    resource_id = kwargs.get('pk')
    resource = Resources.objects.get(pk=resource_id)
    if request.user.id != resource.user_id:
        return HttpResponseForbidden("You are not allowed to delete this resource.")
    resource.delete()
    return redirect('therapy:therapy-resources')

@login_required
def thread_detail_view(request, pk):
    thread = get_object_or_404(Threads, pk=pk)  
    replies = Posts.objects.filter(thread=thread)  
    return render(request, 'therapy/therapy/thread_detail.html', {'thread': thread, 'replies': replies})

@login_required
def thread_create(request):

    form = NewThreadForm(request.POST or None, request.FILES or None)
    
    if request.method == 'POST':

        if form.is_valid():
            new_thread = form.save(commit=False)
            new_thread.user_id = request.user.id
            new_thread.name = request.user.username
            new_thread.save()

            return redirect('therapy:therapy-forums')  

    return render(request, 'therapy/therapy/thread_create.html', {'form': form})

@login_required
def therapy_followup(request, pk):
    profile = get_object_or_404(Profiles, pk=pk)
    return render(request, 'therapy/therapy/therapy_followup.html', {'profile': profile})

# Editar perfil
@login_required
def profile_edit(request, pk):
    profile = get_object_or_404(Profiles, pk=pk)
    if request.user.id != profile.user_id:
        return HttpResponseForbidden("You are not allowed to edit this thread.")
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('therapy:therapy-followup', pk=pk)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'therapy/therapy/profile_edit.html', {'form': form, 'profile': profile})
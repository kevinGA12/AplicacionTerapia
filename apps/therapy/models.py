from django.db import models
from django.urls import reverse_lazy
from django.conf import settings

class BaseName(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre')
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

class Profiles(BaseName):
    username = models.CharField(max_length=150, verbose_name='Nombre')
    age = models.IntegerField(verbose_name='Edad')
    therapycount = models.IntegerField(verbose_name='Numero de Terapias')
    wellbeing = models.IntegerField(verbose_name='Bienestar')
    currentmood = models.CharField(max_length=150, verbose_name='Estado de Animo')
    stresslevel = models.IntegerField(verbose_name='Nivel de Estres')
    anxietylevel = models.IntegerField(verbose_name='Nivel de Ansiedad')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Usuario')

    class Meta:
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuarios'

    def get_profile_url(self):
        return reverse_lazy('therapy:therapy-followup', kwargs={'pk': self.pk})
    
    def get_edit_url(self):
        return reverse_lazy('therapy:profile-edit', kwargs={'pk': self.pk})

class Categories(BaseName):
    class Meta:
        verbose_name = 'Categoria de Terapia'
        verbose_name_plural = 'Categorias de Terapias'

class Doctors(BaseName):
    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctores'

class Sessions(BaseName):
    session_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=256, verbose_name='Descripcion')
    date_created = models.DateTimeField(auto_now_add=True)
    user_id = models.IntegerField()
    found = models.BooleanField(default=False)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, verbose_name='Categoria')
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE, verbose_name='Doctor')
    therapy_date = models.DateField(max_length=256, verbose_name='Fecha de Terapia')
    therapy_time = models.TimeField(auto_now=False, auto_now_add=False, verbose_name='Hora de Terapia')

    class Meta:
        verbose_name = 'Terapia'
        verbose_name_plural = 'Terapias'

    def get_edit_url(self):
        return reverse_lazy('therapy:therapy-edit', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse_lazy('therapy:therapy-delete', kwargs={'pk': self.pk})

    def get_detail_url(self):
        return reverse_lazy('therapy:therapy-detail', kwargs={'pk': self.pk})
    
class Threads(BaseName):
    thread_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150, verbose_name='Titulo')
    initial_post = models.TextField(max_length=1000, verbose_name='Mensaje Inicial')
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Usuario')

    class Meta:
        verbose_name = 'Hilo del Foro'
        verbose_name_plural = 'Hilos del Foro'

    def get_reply_url(self):
        return reverse_lazy('therapy:thread-reply', kwargs={'pk': self.pk})

    def get_edit_url(self):
        return reverse_lazy('therapy:thread-edit', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse_lazy('therapy:thread-delete', kwargs={'pk': self.pk})

    def get_detail_url(self):
        return reverse_lazy('therapy:thread-detail', kwargs={'pk': self.pk})

class Posts(BaseName):
    thread = models.ForeignKey(Threads, on_delete=models.CASCADE, related_name='posts', verbose_name='Hilo')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Usuario')
    message = models.TextField(verbose_name='Mensaje')
    date_posted = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Publicación')

    class Meta:
        verbose_name = 'Publicación del Foro'
        verbose_name_plural = 'Publicaciones del Foro'
        ordering = ['date_posted']

class Resources(BaseName):
    title = models.CharField(max_length=150, verbose_name='Titulo')
    text = models.TextField(max_length=1000, verbose_name='Texto')
    icon = models.ImageField(upload_to='therapy', verbose_name='Icono')
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, verbose_name='Categoria')
    date_posted = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Publicación')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Usuario')

    class Meta:
        verbose_name = 'Recurso'
        verbose_name_plural = 'Recursos'
        ordering = ['date_posted']
    
    def get_edit_url(self):
        return reverse_lazy('therapy:resource-edit', kwargs={'pk': self.pk})
    
    def get_delete_url(self):
        return reverse_lazy('therapy:resource-delete', kwargs={'pk': self.pk})
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.forms import formset_factory
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponseRedirect
from django.db import connection
import logging
from .models import Property, PropertyPhoto
from .forms import PropertyForm, PropertyPhotoForm, ContactRequestForm
from apps.contact.models import ContactRequest

# Configurar logger
logger = logging.getLogger(__name__)

class ProfileRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return (
            self.request.user.is_authenticated
            and self.request.user.profile_type in ["arrendatario", "arrendador"]
        )

    def handle_no_permission(self):
        messages.error(
            self.request,
            "No tienes permiso para acceder a esta página. Solo arrendadores y arrendatarios pueden ver la lista de propiedades.",
        )
        return redirect("home")

class PropertyListView(LoginRequiredMixin, ProfileRequiredMixin, ListView):
    model = Property
    template_name = "properties/list.html"
    context_object_name = "properties"

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Property.objects.all()
        if user.profile_type == "arrendador":
            return Property.objects.filter(owner=user, is_active=True)
        return Property.objects.filter(is_active=True)

class PropertyDetailView(LoginRequiredMixin, ProfileRequiredMixin, DetailView):
    model = Property
    template_name = "properties/property_detail.html"
    context_object_name = "property"

    def get_context_data(self, **kwargs):
        # Forzar recarga del objeto desde la base de datos para obtener los valores más recientes
        self.object.refresh_from_db()
        context = super().get_context_data(**kwargs)
        if self.request.user.profile_type == "arrendatario":
            context["contact_form"] = ContactRequestForm()
        context["photos"] = self.object.related_photos.all()  # Añadimos las fotos para Lightbox
        context["GOOGLE_MAPS_API_KEY"] = getattr(settings, 'GOOGLE_MAPS_API_KEY', '')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if request.user.profile_type != "arrendatario":
            messages.error(request, "Solo los arrendatarios pueden enviar solicitudes de contacto.")
            return redirect("property_detail", pk=self.object.pk)

        form = ContactRequestForm(request.POST)
        if form.is_valid():
            contact_request = form.save(commit=False)
            contact_request.tenant = request.user
            contact_request.property = self.object
            contact_request.owner = self.object.owner
            contact_request.save()
            messages.success(request, "Solicitud de contacto enviada correctamente.")
            return redirect("property_detail", pk=self.object.pk)
        else:
            messages.error(request, "Por favor corrige los errores del formulario.")
            context = self.get_context_data()
            context["contact_form"] = form
            return self.render_to_response(context)

class PropertyCreateView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (user.is_superuser or user.profile_type == "arrendador")

    def get(self, request):
        property_form = PropertyForm()
        PhotoFormSet = formset_factory(PropertyPhotoForm, extra=3, can_delete=False)
        photo_formset = PhotoFormSet()
        return render(
            request,
            "properties/property_form.html",
            {
                "property_form": property_form,
                "photo_formset": photo_formset,
            },
        )

    def post(self, request):
        property_form = PropertyForm(request.POST, request.FILES)
        PhotoFormSet = formset_factory(PropertyPhotoForm, extra=3, can_delete=False)
        photo_formset = PhotoFormSet(request.POST, request.FILES)

        if property_form.is_valid():
            property_obj = property_form.save(commit=False)
            property_obj.owner = request.user
            property_obj.is_active = True
            # Validar que latitude y longitude estén presentes
            if not property_obj.latitude or not property_obj.longitude:
                messages.error(request, "Debes seleccionar y confirmar una ubicación en el mapa.")
                return render(
                    request,
                    "properties/property_form.html",
                    {
                        "property_form": property_form,
                    },
                )
            property_obj.save()

            # Procesar fotos múltiples, principal y orden
            photos = request.FILES.getlist('photos')
            main_index = int(request.POST.get('main_photo_index', 0)) if request.POST.get('main_photo_index') else 0
            for idx, photo in enumerate(photos):
                is_main = (idx == main_index)
                PropertyPhoto.objects.create(
                    property=property_obj,
                    image=photo,
                    is_main=is_main,
                    order=idx
                )
            # Actualiza el campo main_photo en Property
            if photos:
                property_obj.main_photo = photos[main_index]
                property_obj.save()

            messages.success(request, "Propiedad creada exitosamente.")
            return redirect("property_list")

        # Manejo de errores
        for field, errors in property_form.errors.items():
            for error in errors:
                messages.error(request, f"{property_form.fields[field].label}: {error}")

        for i, form in enumerate(photo_formset):
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Foto {i + 1} - {form.fields[field].label}: {error}")

        return render(
            request,
            "properties/property_form.html",
            {
                "property_form": property_form,
                "photo_formset": photo_formset,
            },
        )

class PropertyUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        user = self.request.user
        property_obj = get_object_or_404(Property, pk=self.kwargs.get("pk"))
        return user.is_authenticated and (user.is_superuser or user == property_obj.owner)

    def get(self, request, pk):
        property_obj = get_object_or_404(Property, pk=pk)
        if not (request.user.is_superuser or request.user == property_obj.owner):
            messages.error(request, "No tienes permiso para editar esta propiedad.")
            return redirect("property_list")

        property_form = PropertyForm(instance=property_obj)
        PhotoFormSet = formset_factory(PropertyPhotoForm, extra=0, can_delete=True)
        photo_formset = PhotoFormSet(initial=[{'property': property_obj}] * property_obj.related_photos.count())
        for form, photo in zip(photo_formset.forms, property_obj.related_photos.all()):
            form.instance = photo

        return render(
            request,
            "properties/property_form.html",
            {
                "property_form": property_form,
                "photo_formset": photo_formset,
                "is_update": True,
                "property": property_obj,
            },
        )

    def post(self, request, pk):
        property_obj = get_object_or_404(Property, pk=pk)
        if not (request.user.is_superuser or request.user == property_obj.owner):
            messages.error(request, "No tienes permiso para editar esta propiedad.")
            return redirect("property_list")

        property_form = PropertyForm(request.POST, request.FILES, instance=property_obj)
        PhotoFormSet = formset_factory(PropertyPhotoForm, extra=0, can_delete=True)
        photo_formset = PhotoFormSet(request.POST, request.FILES, initial=[{'property': property_obj}] * property_obj.related_photos.count())

        if property_form.is_valid():
            property_obj = property_form.save(commit=False)
            # Validar que latitude y longitude estén presentes
            if not property_obj.latitude or not property_obj.longitude:
                messages.error(request, "Debes seleccionar y confirmar una ubicación en el mapa.")
                return render(
                    request,
                    "properties/property_form.html",
                    {
                        "property_form": property_form,
                        "is_update": True,
                        "property": property_obj,
                    },
                )
            property_obj.save()

            # Eliminar fotos antiguas
            property_obj.related_photos.all().delete()
            # Procesar fotos múltiples, principal y orden
            photos = request.FILES.getlist('photos')
            main_index = int(request.POST.get('main_photo_index', 0)) if request.POST.get('main_photo_index') else 0
            for idx, photo in enumerate(photos):
                is_main = (idx == main_index)
                PropertyPhoto.objects.create(
                    property=property_obj,
                    image=photo,
                    is_main=is_main,
                    order=idx
                )
            # Actualiza el campo main_photo en Property
            if photos:
                property_obj.main_photo = photos[main_index]
                property_obj.save()

            messages.success(request, "Propiedad actualizada exitosamente.")
            return redirect("property_list")

        messages.error(request, "Hubo errores al actualizar la propiedad.")
        return render(
            request,
            "properties/property_form.html",
            {
                "property_form": property_form,
                "photo_formset": photo_formset,
                "is_update": True,
                "property": property_obj,
            },
        )

class PropertyDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        user = self.request.user
        property_obj = get_object_or_404(Property, pk=self.kwargs.get("pk"))
        return user.is_authenticated and (user.is_superuser or user == property_obj.owner)
    
    def post(self, request, pk):
        try:
            # Obtener la propiedad directamente
            property_obj = Property.objects.get(pk=pk)
            
            # Verificar permisos
            if not (request.user.is_superuser or request.user == property_obj.owner):
                messages.error(request, "No tienes permiso para eliminar esta propiedad.")
                return redirect("property_list")
            
            # Guardar el título antes de eliminar
            property_title = property_obj.title
            
            # Eliminar todas las referencias a la propiedad en otras tablas
            with connection.cursor() as cursor:
                # Eliminar fotos relacionadas
                cursor.execute("DELETE FROM properties_propertyphoto WHERE property_id = %s", [pk])
                
                # Eliminar solicitudes de contacto relacionadas
                cursor.execute("DELETE FROM contact_contactrequest WHERE property_id = %s", [pk])
                
                # Intentar eliminar otras posibles referencias
                try:
                    cursor.execute("DELETE FROM contracts_contract WHERE property_id = %s", [pk])
                except:
                    pass  # Ignorar si la tabla no existe
                
                try:
                    cursor.execute("DELETE FROM payments_payment WHERE property_id = %s", [pk])
                except:
                    pass  # Ignorar si la tabla no existe
                
                try:
                    cursor.execute("DELETE FROM ratings_rating WHERE property_id = %s", [pk])
                except:
                    pass  # Ignorar si la tabla no existe
                
                # Finalmente eliminar la propiedad
                cursor.execute("DELETE FROM properties_property WHERE id = %s", [pk])
            
            # Mensaje de éxito
            messages.success(request, f"La propiedad '{property_title}' ha sido eliminada con éxito.")
            return redirect("property_list")
        except Exception as e:
            # Registrar el error para depuración
            logger.error(f"Error al eliminar propiedad {pk}: {str(e)}")
            # Mensaje de error genérico
            messages.error(request, "No se pudo eliminar la propiedad. Por favor, inténtelo de nuevo.")
            return redirect("property_list")
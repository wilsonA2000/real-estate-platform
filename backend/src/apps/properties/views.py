from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.forms import formset_factory
from .models import Property
from .forms import PropertyForm, PropertyPhotoForm


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


class PropertyCreateView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        user = self.request.user
        if user.is_superuser:
            return True
        return user.is_authenticated and user.profile_type == "arrendador"

    def get(self, request):
        property_form = PropertyForm()
        PhotoFormSet = formset_factory(PropertyPhotoForm, extra=3)
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
        PhotoFormSet = formset_factory(PropertyPhotoForm, extra=3)
        photo_formset = PhotoFormSet(request.POST, request.FILES)

        if property_form.is_valid() and photo_formset.is_valid():
            property_obj = property_form.save(commit=False)
            property_obj.owner = request.user
            property_obj.is_active = True
            property_obj.save()

            for form in photo_formset:
                image = form.cleaned_data.get("image")
                if image:
                    photo = form.save(commit=False)
                    photo.property = property_obj
                    photo.save()

            messages.success(request, "Propiedad creada exitosamente.")
            return redirect("property_list")

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
        if user.is_superuser:
            return True
        return (
            user.is_authenticated
            and user.profile_type == "arrendador"
            and user == property_obj.owner
        )

    def get(self, request, pk):
        property_obj = get_object_or_404(Property, pk=pk)
        property_form = PropertyForm(instance=property_obj)
        PhotoFormSet = formset_factory(PropertyPhotoForm, extra=3)
        photo_formset = PhotoFormSet()
        return render(
            request,
            "properties/property_edit.html",
            {
                "property_form": property_form,
                "photo_formset": photo_formset,
                "property": property_obj,
            },
        )

    def post(self, request, pk):
        property_obj = get_object_or_404(Property, pk=pk)
        property_form = PropertyForm(request.POST, request.FILES, instance=property_obj)
        PhotoFormSet = formset_factory(PropertyPhotoForm, extra=3)
        photo_formset = PhotoFormSet(request.POST, request.FILES)

        if property_form.is_valid() and photo_formset.is_valid():
            property_obj = property_form.save()

            for form in photo_formset:
                image = form.cleaned_data.get("image")
                if image:
                    photo = form.save(commit=False)
                    photo.property = property_obj
                    photo.save()

            messages.success(request, "Propiedad actualizada exitosamente.")
            return redirect("property_detail", pk=property_obj.pk)

        for field, errors in property_form.errors.items():
            for error in errors:
                messages.error(request, f"{property_form.fields[field].label}: {error}")

        for i, form in enumerate(photo_formset):
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Foto {i + 1} - {form.fields[field].label}: {error}")

        return render(
            request,
            "properties/property_edit.html",
            {
                "property_form": property_form,
                "photo_formset": photo_formset,
                "property": property_obj,
            },
        )
from django.shortcuts import redirect, render
from .models import Profile, Collection, Medicine
from .forms import (
    RegisterUserForm,
    ProfileForm,
    UserForm,
    MedicineForm,
    CollectionForm,
    UserLoginForm,
)
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


@login_required
def index(request):
    return render(request, "base/index.html")


def Login(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
        form = UserLoginForm()

    context = {"form": form}
    return render(request, "registration/login.html", context)


def register(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
        form = RegisterUserForm()

    context = {"form": form}
    return render(request, "registration/register.html", context)


@login_required
def profile(request):
    user = request.user
    _profile = Profile.objects.get(user=user)
    context = {"user": user, "profile": _profile}
    return render(request, "base/profile.html", context)


@login_required
def edit_profile(request):
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(
            request.POST, request.FILES, instance=request.user.profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile is updated successfully")
            return redirect("profile")
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    return render(
        request,
        "base/edit_profile.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


@staff_member_required
def create_collection(request, pk=None):
    if pk is not None:
        medicine = Medicine.objects.get(pk=pk)
        if request.method == "POST":
            form = CollectionForm(request.POST, initial_medition=medicine)
            if Collection.objects.filter(
                medition=medicine,
                userID=form.data["userID"],
                date=form.data["date"],
            ).exists():
                messages.error(
                    request,
                    "Collection for this medicine, user and date already exists!",
                )
                return redirect("index")
            else:
                form.save()
                messages.success(request, "Collection added successfully!")
                return redirect("index")
        else:
            form = CollectionForm(initial_medition=medicine)
        context = {"form": form, "medicine": medicine}
    else:
        if request.POST:
            form = CollectionForm(request.POST)
            if form.is_valid():
                if Collection.objects.filter(
                    medition=form.cleaned_data["medition"],
                    userID=form.cleaned_data["userID"],
                    date=form.cleaned_data["date"],
                ).exists():
                    messages.error(
                        request,
                        "Collection for this medicine, user and date already exists!",
                    )
                    return redirect("index")
                else:
                    form.save()
                    messages.success(request, "Collection added successfully!")
                    return redirect("index")
        else:
            form = CollectionForm()
        context = {"form": form}

    return render(request, "base/create_collection.html", context)


@staff_member_required
def collections_for_admin(request):
    collections = Collection.objects.all()
    collectionscontext = {"collections": collections}
    action = request.GET.get("action")
    if request.method == "POST":
        if action == "delete":
            collection = Collection.objects.get(pk=request.POST.get("collection_id"))
            collection.delete(collection)
        if action == "approve":
            unapproved_collection

    return render(request, "base/collections_for_admin.html", collectionscontext)


@login_required
def collections_for_user(request):
    collections = Collection.objects.filter(userID=request.user)
    collectionscontext = {"collections": collections}
    action = request.GET.get("action")
    if request.method == "POST":
        if action == "approve":
            unapproved_collection
    return render(request, "base/collections_for_user.html", collectionscontext)


@staff_member_required
def delete_collection(request, pk):
    collection = Collection.objects.get(pk=pk)
    collection.delete()
    messages.success(request, "Collection deleted successfully!")
    return redirect("collections_for_admin")


@staff_member_required
def unapproved_collection(request):
    collections = Collection.objects.filter(collectedApproved=False)
    collectionscontext = {"collections": collections}
    return render(request, "base/unapproved_collections.html", collectionscontext)


@staff_member_required
def approve_collection(request, pk):
    collection = Collection.objects.get(pk=pk)
    if collection.collected is False:
        messages.error(request, "Collection not collected yet!")
        return redirect("collections_for_admin")
    else:
        collection.collectedApproved = True
        collection.collectedApprovedBy = request.user
        collection.save()
        messages.success(request, "Collection approved successfully!")
        return redirect("collections_for_admin")


@login_required
def approve_collected(request, pk):
    collection = Collection.objects.get(pk=pk)
    collection.collected = True
    collection.save()
    messages.success(request, "Collection approved successfully!")
    return redirect("collections_for_user")


@staff_member_required
def new_medicine(request):
    if request.method == "POST":
        form = MedicineForm(request.POST)
        action = request.POST.get("action")
        if form.is_valid():
            medicine = form.save()
            if action == "submit":
                return redirect(
                    "new_medicine_confirm", pk=medicine.pk
                )  # Redirect to new_medicine_confirm view
    else:
        form = MedicineForm()
    return render(request, "base/new_medicine.html", {"form": form})


@staff_member_required
def new_medicine_confirm(request, pk):
    medicine = Medicine.objects.get(pk=pk)
    context = {"medicine": medicine}
    action = request.POST.get("action")
    if request.method == "POST":
        if action == "confirm":
            messages.success(request, "Medicine added successfully")
            return redirect("new_medicine")
        elif action == "cancel":
            messages.warning(request, "Cancelled adding medicine")
            medicine.delete()
            return redirect("index")
    return render(request, "base/new_medicine_confirm.html", context)


@staff_member_required
def medicine(request):
    medicines = Medicine.objects.all()
    context = {"medicines": medicines}
    action = request.POST.get("action")
    if request.method == "POST":
        if action == "delete":
            medicine = Medicine.objects.get(pk=request.POST.get("medicine_id"))
            medicine_delete(request, medicine.pk)
        elif action == "edit":
            medicine = Medicine.objects.get(pk=request.POST.get("medicine_id"))
            return redirect("edit_medicine", pk=medicine.pk)
        elif action == "collection":
            medicine_id = request.POST.get("medicine_id")
            return redirect("create_collection_with_medicine", pk=medicine_id)
    return render(request, "base/medicine.html", context)


@staff_member_required
def edit_medicine(request, pk):
    medicine = Medicine.objects.get(pk=pk)
    if request.method == "POST":
        form = MedicineForm(request.POST, instance=medicine)
        action = request.POST.get("action")
        if form.is_valid():
            medicine = form.save()
            if action == "save":
                messages.success(request, "Medicine updated successfully")
                return redirect("medicine")
    else:
        form = MedicineForm(instance=medicine)
    return render(
        request, "base/edit_medicine.html", {"form": form, "medicine": medicine}
    )


@staff_member_required
def medicine_delete(request, pk):
    medicine = Medicine.objects.get(pk=pk)
    medicine.delete()
    messages.warning(request, "Medicine deleted successfully")
    return redirect("medicine")


@login_required
def medicine_profile(request, pk):
    amount_collected_by_user = 0
    total_amount_collected = 0
    medicine = Medicine.objects.get(pk=pk)
    collections = Collection.objects.filter(medition=medicine)
    for collection in collections:
        if collection.collected and collection.userID == request.user:
            amount_collected_by_user += 1
        if collection.collected:
            total_amount_collected += 1
    context = {
        "medicine": medicine,
        "amount_collected_by_user": amount_collected_by_user,
        "total_amount_collected": total_amount_collected,
    }
    return render(request, "base/medicine_profile.html", context)


@staff_member_required
def admin_profile(request, pk):
    # This is the profile of a user which only an admin can see, it shows the amount of collections the user has done and the amount of collections that have been approved
    open_collections = Collection.objects.filter(userID=pk, collected=False)
    completed_collections = Collection.objects.filter(userID=pk, collected=True)
    approved_collected = Collection.objects.filter(userID=pk, collectedApproved=True)
    context = {
        "open_collections": open_collections,
        "completed_collections": completed_collections,
        "approved_collected": approved_collected,
        "username": open_collections[0].userID.username,
    }
    return render(request, "base/admin_profile.html", context)

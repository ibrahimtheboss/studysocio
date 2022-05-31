from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render

# Create your views here.
from apps.complaint.forms import ComplaintForm
from apps.complaint.models import Complaint, Feedback


@login_required
def complaints(request):
    view_Complaint = Complaint.objects.filter(created_by=request.user)
    feedbacks = Feedback.objects.filter(complaint__created_by=request.user)

    context = {
    'view_Complaint': view_Complaint,
        'feedbacks':feedbacks,

    }
    return render(request, 'complaint/complaint.html',context )

@login_required
def make_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                members = Complaint.objects.create(
                    title=form.cleaned_data["title"],
                    Description=form.cleaned_data["Description"],
                    created_by=User.objects.get(pk=request.user.id),
                )

                members.save()
                messages.success(request, 'successfully Sent Complaint/ Request.')
                return render(request, 'complaint/make_complaint.html',
                              {'form': form,
                               })

            except IntegrityError:
                messages.warning(request, 'error')

        else:
            return render(request, 'complaint/make_complaint.html',
                          {'form': form,
                           })
    else:
        form = ComplaintForm()

    context = {
        'form': form,
        }
    return render(request, 'complaint/make_complaint.html', context)
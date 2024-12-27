from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.core.serializers import serialize
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.views.decorators.http import require_http_methods
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

from jobapp.forms import *
from jobapp.models import *
from jobapp.permission import *
User = get_user_model()


def home_view(request):

    published_jobs = Job.objects.filter(is_published=True).order_by('-timestamp')
    jobs = published_jobs.filter(is_closed=False)
    total_candidates = User.objects.filter(role='employee').count()
    total_companies = User.objects.filter(role='employer').count()
    paginator = Paginator(jobs, 3)
    page_number = request.GET.get('page',None)
    page_obj = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        job_lists = list(jobs.values())
        return JsonResponse({
            'job_lists': job_lists
        })

    context = {
        'total_candidates': total_candidates,
        'total_companies': total_companies,
        'total_jobs': len(jobs),
        'total_completed_jobs':len(published_jobs.filter(is_closed=True)),
        'page_obj': page_obj
    }
    return render(request, 'jobapp/index.html', context)

@cache_page(60 * 15)
def job_list_View(request):
    job_list = Job.objects.filter(is_published=True,is_closed=False).order_by('-timestamp')
    paginator = Paginator(job_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj}
    return render(request, 'jobapp/job-list.html', context)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def create_job_View(request):
    form = JobForm(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)
    categories = Category.objects.all()

    if request.method == 'POST':

        if form.is_valid():

            instance = form.save(commit=False)
            instance.user = user
            instance.save()
            # for save tags
            form.save_m2m()
            messages.success(
                    request, 'You are successfully posted your job! Please wait for review.')
            return redirect(reverse("jobapp:single-job", kwargs={'id': instance.id}))

    context = {
        'form': form,
        'categories': categories
    }
    return render(request, 'jobapp/post-job.html', context)


def single_job_view(request, id):
    if cache.get(id):
        job = cache.get(id)
    else:
        job = get_object_or_404(Job, id=id)
        cache.set(id,job , 60 * 15)
    related_job_list = job.tags.similar_objects()

    paginator = Paginator(related_job_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'job': job,
        'page_obj': page_obj,
        'total': len(related_job_list)

    }
    return render(request, 'jobapp/job-single.html', context)


def search_result_view(request):
    """
    Handle job search with multiple filters
    """
    job_list = Job.objects.filter(is_published=True, is_closed=False).order_by('-timestamp')
    
    # Keywords/Title Search
    if 'job_title' in request.GET:
        job_title = request.GET.get('job_title', '').strip()
        if job_title:
            job_list = job_list.filter(
                Q(title__icontains=job_title) |
                Q(company_name__icontains=job_title)
            )
    
    # Location Search
    if 'location' in request.GET:
        location = request.GET.get('location', '').strip()
        if location:
            job_list = job_list.filter(location__icontains=location)
    
    # Job Type Filter
    if 'job_type' in request.GET:
        job_type = request.GET.get('job_type', '').strip()
        if job_type:
            job_list = job_list.filter(job_type=job_type)
    
    # Category Filter
    if 'category' in request.GET:
        category = request.GET.get('category')
        if category:
            job_list = job_list.filter(category_id=category)

    paginator = Paginator(job_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total_jobs': len(job_list),
        'search_title': request.GET.get('job_title', ''),
        'search_location': request.GET.get('location', ''),
        'search_type': request.GET.get('job_type', ''),
        'categories': Category.objects.all()
    }
    return render(request, 'jobapp/search.html', context)



# apply job
@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def apply_job_view(request, id):
    form = JobApplyForm(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)
    job = get_object_or_404(Job, id=id)

    if job.is_closed:
        messages.error(request, 'This job is closed!')
        return redirect('jobapp:single-job', id=id)
        
    if Applicant.objects.filter(user=user, job=job).exists():
        messages.error(request, 'You already applied for this job')
        return redirect('jobapp:single-job', id=id)

    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            instance.save()

            try:
                # Send email notification
                mail_subject = f'Job Application Confirmation - {job.title}'
                message = render_to_string('emails/job_application.html', {
                    'user': user,
                    'job': job,
                })
                email = EmailMessage(
                    mail_subject,
                    message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[user.email]
                )
                email.content_subtype = "html"
                email.send(fail_silently=False)
                messages.success(request, 'Application submitted and confirmation email sent!')
            except Exception as e:
                messages.warning(request, f'Application submitted but email failed: {e}')

            return redirect('jobapp:single-job', id=id)

    context = {'form': form, 'job': job}
    return render(request, 'jobapp/job-apply.html', context)

# dashboard
@login_required(login_url=reverse_lazy('account:login'))
def dashboard_view(request):
    jobs = []
    savedjobs = []
    appliedjobs = []
    total_applicants = {}
    if request.user.role == 'employer':

        jobs = Job.objects.filter(user=request.user.id)
        for job in jobs:
            count = Applicant.objects.filter(job=job.id).count()
            total_applicants[job.id] = count

    if request.user.role == 'employee':
        savedjobs = BookmarkJob.objects.filter(user=request.user.id)
        appliedjobs = Applicant.objects.filter(user=request.user.id)
    context = {

        'jobs': jobs,
        'savedjobs': savedjobs,
        'appliedjobs':appliedjobs,
        'total_applicants': total_applicants
    }

    return render(request, 'jobapp/dashboard.html', context)


@login_required
def delete_job_view(request, id):
    try:
        job = Job.objects.get(id=id, user=request.user)
        job.delete()
        return JsonResponse({
            'status': True,
            'message': 'Job successfully deleted!'
        })
    except Job.DoesNotExist:
        return JsonResponse({
            'status': False,
            'message': 'Job not found!'
        }, status=404)



# make job complete
@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def make_complete_job_view(request, id):
    try:
        job = Job.objects.get(id=id, user=request.user)
        job.is_closed = True
        job.save()
        return JsonResponse({
            'status': True,
            'message': 'Job successfully marked as closed!'
        })
    except Job.DoesNotExist:
        return JsonResponse({
            'status': False,
            'message': 'Job not found!'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': False,
            'message': str(e)
        }, status=500)


# all applicants
@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def all_applicants_view(request, id):
    job = get_object_or_404(Job, id=id, user=request.user)
    all_applicants = Applicant.objects.filter(job=job)

    context = {
        'job': job,
        'all_applicants': all_applicants
    }

    return render(request, 'jobapp/all-applicants.html', context)


# delete bookmark
@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def delete_bookmark_view(request, id):

    job = get_object_or_404(BookmarkJob, id=id, user=request.user.id)

    if job:

        job.delete()
        messages.success(request, 'Saved Job was successfully deleted!')

    return redirect('jobapp:dashboard')




# applicant details
@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def applicant_details_view(request, id):

    applicant = get_object_or_404(User, id=id)

    context = {'applicant': applicant}

    return render(request, 'jobapp/applicant-details.html', context)


# job bookmark
@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def job_bookmark_view(request, id):

    form = JobBookmarkForm(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)
    applicant = BookmarkJob.objects.filter(user=request.user.id, job=id)

    if not applicant:
        if request.method == 'POST':
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user
                instance.save()
                messages.success(
                    request, 'You have successfully save this job!')
                return redirect(reverse("jobapp:single-job", kwargs={'id': id}))
        else:
            return redirect(reverse("jobapp:single-job", kwargs={'id': id}))

    else:
        messages.error(request, 'You already saved this Job!')
        return redirect(reverse("jobapp:single-job", kwargs={'id': id}))


# job edit
@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def job_edit_view(request, id=id):
    job = get_object_or_404(Job, id=id, user=request.user.id)
    categories = Category.objects.all()
    form = JobEditForm(request.POST or None, instance=job)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        # for save tags
        # form.save_m2m()
        messages.success(request, 'Your Job Post Was Successfully Updated!')
        return redirect(reverse("jobapp:single-job", kwargs={'id': instance.id}))
    context = {
        'form': form,
        'categories': categories
    }

    return render(request, 'jobapp/job-edit.html', context)

@login_required
@require_http_methods(["DELETE"])
def delete_job(request, id):
    try:
        job = Job.objects.get(id=id, user=request.user)
        job.delete()
        return JsonResponse({
            'status': True,
            'message': 'Job successfully deleted!'
        })
    except Job.DoesNotExist:
        return JsonResponse({
            'status': False,
            'message': 'Job not found!'
        }, status=404)

@login_required
@user_is_employer
def send_job_offer(request, job_id, applicant_id):
    job = get_object_or_404(Job, id=job_id, user=request.user)
    applicant = get_object_or_404(User, id=applicant_id)
    
    # Send offer email
    mail_subject = f'Job Offer - {job.title}'
    message = render_to_string('emails/job_offer.html', {
        'user': applicant,
        'job': job,
        'employer': request.user,
    })
    
    email = EmailMessage(
        subject=mail_subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[applicant.email]
    )
    # Set the content type to HTML
    email.content_subtype = "html"
    email.send()
    
    messages.success(request, f'Job offer sent to {applicant.get_full_name()}')
    return redirect('jobapp:applicants', id=job_id)

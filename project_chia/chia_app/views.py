"""Views: /app"""

from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage

from .models import Record, Category
from .forms import RecordForm


# Create your views here.
@login_required
def hello(request):
    """test function"""
    return render(request,'app/example_hello.html',{})

@login_required
def frontpage(request):
    """frontpage function"""
    record_form = RecordForm(initial={'balance_type': '支出'})
    records = Record.objects.filter()
    income_list = [record.cash for record in records if record.balance_type == '收入']
    outcome_list = [record.cash for record in records if record.balance_type == '支出']
    income = sum(income_list) if len(income_list)!=0 else 0
    outcome = sum(outcome_list) if len(outcome_list)!=0 else 0
    net = income - outcome
    return render(request,'app/index.html', locals())

@login_required
def settings(request):
    """settings function"""
    categories = Category.objects.filter()
    print(categories)
    return render(request,'app/settings.html', locals())

@login_required
def add_category(request):
    """addCategory function"""
    if request.method == 'POST':
        posted_data = request.POST
        category = posted_data['add_category_name']
        Category.objects.get_or_create(category=category)
    return redirect('/app/settings')

@login_required
def delete_category(category):
    """delete_category function"""
    Category.objects.filter(category=category).delete()
    return redirect('/app/settings')

@login_required
def add_record(request):
    """add_record function"""
    if request.method == 'POST':
        form = RecordForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('/app')

@login_required
def delete_record(request):
    """delete_record function"""
    if request.method == 'POST':
        record_id = request.POST['delete_val']
        Record.objects.filter(id=record_id).delete()
    return redirect('/app')

###upload
def upload(request):
    """upload function"""
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        # url = fs.url(name)
        context['url'] = fs.url(name)
    return render(request, 'app/upload.html', context)

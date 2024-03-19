from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
from .models import CSP

# Create your views here.
@login_required(login_url='login')
def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
        
    return render (request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('/')

def home(request):
    return render(request,"index.html")


def aboutus(request):
    return render(request,"about.html")


def search(request):
    return render(request,"search.html")


def search_view(request):
    if 'q' in request.GET:
        query = request.GET['q']
        results = CSP.objects.filter(company_name__icontains=query)
        return render(request, 'search.html', {'results': results, 'query': query})
    return render(request, 'search.html')

def search_stockiest(request):
    query = request.GET.get('q')
    st = request.GET.get('stock')

    if query:
        results = CSP.objects.filter(stockiest_name__icontains=query)
    elif st:
        results = CSP.objects.filter(stockiest_name__icontains=st)
    else:
        results = None

    context = {'results': results, 'query': query, 'stock': st}
    return render(request, 'search.html', context)

from .models import CSP  # Import your model

def search_product(request):
    query = request.GET.get('q')
    pd = request.GET.get('product')
    pcontain = None  # Initialize pcontain to None

    if query:
        results = CSP.objects.filter(company_name__icontains=query)
    elif pd:
        results = CSP.objects.filter(product_name__icontains=pd)
    else:
        results = None

    # Check if a specific CSP record is found, and if so, extract pcontain
    if results and results.exists():
        # Assuming you want to use the pcontain value from the first result
        pcontain = results.first().pcontain

    context = {'results': results, 'query': query, 'product': pd, 'pcontain': pcontain}
    return render(request, 'search.html', context)



def service(request):
    return render(request,"service.html")

def add(request):
    if request.method=='POST':
        print("Added")

        # retrive the infromation from form
        n1 = request.POST.get('s_name')
        n2 = request.POST.get('c_name')
        n3 = request.POST.get('s_address')
        n4 = request.POST.get('s_contact')
        n5 = request.POST.get('noc')
        n6 = request.POST.get('dl1')
        n7 = request.POST.get('dl2')
        n8 = request.POST.get('E_date')

        # create an object for models to show and save
        s = CSP()
        s.stock_name=n1
        s.comp_name=n2
        s.stock_address=n3
        s.stock_phone=n4
        s.noc=n5
        s.dl1=n6
        s.dl2=n7
        s.Expiry_date=n8

        s.save()
        return redirect('search')
    return render(request,'add_details.html',{})


def show(request):
    return render(request,"show_details.html")


# Save record of shows.html
def save_details(request):
    if request.method == 'POST':
        selected_stock = request.POST.get('stock')
        selected_company = request.POST.get('company')

        # Check if both company and stock are selected and not empty
        if selected_company and selected_stock:
            # Check if the combination already exists in the database
            if CSP.objects.filter(stockiest_name=selected_stock, company_name=selected_company).exists():
                messages.error(request, 'Company and Stockiest name already exists')
            else:
                # Create a new record in your model and save it to the database
                new_record = CSP(stockiest_name=selected_stock, company_name=selected_company)
                new_record.save()
                messages.success(request, 'Details saved successfully')
        else:
            # Show an error message if either company or stock is empty
            messages.error(request, 'Please select both Company and Stockiest before saving.')

    return redirect('show')


# Delete record of shows.html

def delete_details(request):
    if request.method == 'POST':
        selected_stock = request.POST.get('stock')
        selected_company = request.POST.get('company')
        
        # Check if both stock and company are provided
        if selected_stock and selected_company:
            try:
                # Use the company_name and stockiest_name to identify and delete the record
                datadelete = CSP.objects.get(company_name=selected_company, stockiest_name=selected_stock)
                datadelete.delete()
                return JsonResponse({'message': 'Record deleted successfully.'})
            except CSP.DoesNotExist:
                return JsonResponse({'message': 'Record not found.'}, status=404)
        else:
            return JsonResponse({'message': 'Both Stock and Company are required.'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method.'}, status=405)



def contact(request):
    return render(request,"contact.html")


from django.contrib import messages
import pandas as pd

# Final Code All working
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']

        if file.name.lower().endswith('.csv') or file.name.lower().endswith('.xlsx'):
            try:
                if file.name.lower().endswith('.csv'):
                    df = pd.read_csv(file)
                else:
                    df = pd.read_excel(file, engine='openpyxl')

                # Define a mapping of expected column names to actual column names
                column_mapping = {
                    'company name': 'company_name',
                    'stockiest name': 'stockiest_name',
                    'product name': 'product_name',
                    'product contain': 'pcontain',
                    'mobile number': 'mobile',
                    'telephone number': 'telephone',
                }

                # Make the column names in the DataFrame case-insensitive
                df.columns = df.columns.str.lower()

                # Map the column names to match your database columns
                df = df.rename(columns=column_mapping)

                for index, row in df.iterrows():
                    CSP.objects.create(
                        company_name=row['company_name'],
                        stockiest_name=row['stockiest_name'],
                        product_name=row['product_name'],
                        pcontain=row['pcontain'],
                        mobile=row['mobile'],
                        telephone=row['telephone']
                    )

                # Add a success message
                messages.success(request, 'File uploaded successfully.')
            except Exception as e:
                # Add an error message
                messages.error(request, f'An error occurred: {str(e)}')
        else:
            # Add an error message for invalid file format
            messages.error(request, 'Invalid file format. Only CSV and XLSX files are allowed.')
        return redirect('upload')
    return render(request, 'File.html')

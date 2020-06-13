from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core import exceptions
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Employee as EmployeeModel
from .models import Customer as CustomerModel
from .models import Mandant as MandantModel
from .models import Product as ProductModel
from .models import Unit
from .permissions import BelongsToClient
from .forms import *
from .exceptions import UploadException
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import permissions
from rest_framework.permissions import *
from .serializers import *
from django.views.decorators.csrf import csrf_exempt
import json
import requests
import csv
import io
import os
import datetime

# Create your views here.
def test(request):
    return render(request, 'meas/test.html')

@login_required(login_url='/login/')
def index(request):
    return render(request, 'meas/index.html')

@login_required(login_url='/login')
def scheduler(request):
    return render(request, 'meas/index.html')

@login_required(login_url='/login/')
def employeesview(request):
    r = EmployeeModel.objects.filter(Mandant=request.user.Mandant, Employees_deleted= False)
    return render(request, 'meas/employees.html', {'context': r})

@login_required(login_url='/login/')
def employeeeditview(request):
    form = EmployeeEditForm()
    return render(request, 'meas/employeeedit.html', {'form': form})

@login_required(login_url='/login/')
def customersview(request):
    return render(request, 'meas/customers.html')

@login_required(login_url='/login/')
def productsview(request):
    if request.method == 'GET':
        form = UploadForm()
        return render(request, 'meas/products.html', {'form': form})
    if request.method == 'POST':
        form = UploadForm(request.POST,request.FILES)
        if form.is_valid():
            fp = os.path.join(settings.MEDIA_ROOT, 'uploads\products\\')
            fn = datetime.datetime.now().strftime('%Y-%m-%d') + '_' + get_random_string(15) + '.json'
            ffn = fp + fn
            try:
                f = handle_csv_upload_products(request, request.FILES['upload_file'])
                with open(ffn,'w+', encoding='utf-8') as jfile:
                    myFile = File(jfile)
                    json.dump(f, myFile, ensure_ascii=False, indent=4)
                return HttpResponseRedirect('/produkte/?success=true&file=' + fn )
            except UploadException as e:
                print(e)
                return HttpResponse(status= 400)

def handle_csv_upload_products(request, csv_file):
    if not request.user.Mandant:
        raise UploadException("Not authenticated")
    if not csv_file.name.endswith(('.csv', '.CSV')):
        raise UploadException("Wrong Datafile")
    
    try:
        data_set = csv_file.read().decode('utf-8')
    except:
        try:
            data_set = csv_file.read().decode('ISO-8859-1')
        except:
            raise UploadException("No utf-8 coded file")
    io_string = io.StringIO(data_set)
    next(io_string)
    j = 2 #Initial Line, for error detection purpose
    e = []
    overlap = None
    content = []
    reader = csv.DictReader(io_string, fieldnames=('Product_number', 'Product_name', 'Product_desc', 'Product_supplier', 'Product_supplier_code','Product_unit','Product_pppu_net', 'Product_sppu_net','Product_vf','Product_vu'),delimiter=";")
    for row in reader:
        content.append(dict(row))
    for i in content:
        if not i['Product_number'] or not i['Product_unit'] or not i['Product_pppu_net'] or not i['Product_sppu_net'] or not i['Product_vf']:
            e.append(
                {
                    'error_line': j-1,
                    'error_line_excel': j,
                    'error_description': 'Pflichtfeld(er) ist/sind leer',
                    'try': 'Artikelnummer, Einheit, Einkaufspreis netto, Verkaufspreis netto und Gültig von müssen gesetzt sein'
                }
            )
        else:
            try:
                unit_id = Unit.objects.get(Unit_symbol=i['Product_unit'])
            except Unit.DoesNotExist:
                e.append(
                    {
                        'error_line': j-1,
                        'error_line_excel': j,
                        'error_description': 'Einheit kann nicht gefunden werden',
                        'try': 'Bitte verwenden Sie die Einheitssymbole, wie sie in den Stammdaten vorkommen'
                    }
                )
                j += 1
                continue
            ae = ProductModel.objects.filter(
                Mandant=request.user.Mandant,
                Product_deleted= False,
                Product_number=i['Product_number'])
            if ae:
                for entry in ae:
                    try:
                        start_b = csv_str_to_date(i['Product_vf'])
                        if i['Product_vu']:
                            end_b = csv_str_to_date(i['Product_vu'])
                        else:
                            end_b = None
                    except Exception as ex:
                        e.append(
                            {
                                'error_line': j-1,
                                'error_line_excel': j,
                                'error_description': str(ex),
                                'try': ''
                            }
                        )
                        continue
                    start_a = entry.Product_vf
                    start_a = start_a.replace(tzinfo=None)
                    if entry.Product_vu:
                        end_a = entry.Product_vu
                        end_a = end_a.replace(tzinfo=None)
                    else: 
                        end_a = None
                    overlap = check_overlap(start_a, end_a,start_b, end_b)
                    if overlap == 0:
                        e.append(
                            {
                                'error_line': j-1,
                                'error_line_excel': j,
                                'error_description': 'Zeitkonflikt',
                                'try': 'Es sind bereits Einträge vorhanden, die zu dieser Zeit Gültigekeit besitzen'
                            }
                        )
                        break
                    if overlap == 2:
                        update = ProductModel.objects.get(pk=entry.pk)
                        update.Product_vu = start_b
                        update.save()
                if overlap == 1 or overlap == 2:
                    try:
                        create = ProductModel.objects.update_or_create(
                            Mandant=request.user.Mandant,
                            Product_number=i['Product_number'],
                            Product_name= i['Product_name'],
                            Product_desc= i['Product_desc'],
                            Product_supplier= i['Product_supplier'],
                            Product_supplier_code= i['Product_supplier_code'],
                            Product_unit= unit_id,
                            Product_pppu_net= csv_str_to_float(i['Product_pppu_net']),
                            Product_sppu_net= csv_str_to_float(i['Product_sppu_net']),
                            Product_vf= start_b,
                            Product_vu= end_b
                        )
                    except Exception as ex:
                        e.append(
                            {
                                'error_line': j-1,
                                'error_line_excel': j,
                                'error_description': str(ex),
                                'try': ''
                            }
                        )
            else:
                try:
                    start = csv_str_to_date(i['Product_vf'])
                    end = None
                    if i['Product_vu']:
                        end = csv_str_to_date(i['Product_vu'])
                    create = ProductModel.objects.update_or_create(
                        Mandant=request.user.Mandant,
                        Product_number=i['Product_number'],
                        Product_name= i['Product_name'],
                        Product_desc= i['Product_desc'],
                        Product_supplier= i['Product_supplier'],
                        Product_supplier_code= i['Product_supplier_code'],
                        Product_unit= unit_id,
                        Product_pppu_net= csv_str_to_float(i['Product_pppu_net']),
                        Product_sppu_net= csv_str_to_float(i['Product_sppu_net']),
                        Product_vf= start,
                        Product_vu= end
                    )
                except Exception as ex:
                    e.append(
                        {
                            'error_line': j-1,
                            'error_line_excel': j,
                            'error_description': str(ex),
                            'try': ''
                        }
                    )
        j += 1
    return e

def check_overlap(start_a, end_a, start_b, end_b):
    if end_a and end_b:
        if start_a <= end_b and start_b <= end_a:
            return 0
        if start_b <= end_a and start_a <= end_b:
            return 0
        if start_a <= end_b and end_a >= start_b:
            return 0
        if start_b <= end_a and end_b >= start_a:
            return 0
    if end_a and not end_b:
        if start_b <= end_a:
            return 0
    if not end_a and start_b >= start_a:
        return 2
    return 1

def csv_str_to_float(a):
    a = a.replace('.','')
    a = a.replace(',','.')
    a = a.replace('€','')
    a = a.replace('$','')
    return float(a) 

def csv_str_to_date(a):
    date_patterns = ["%d-%m-%Y", "%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y", "%Y/%m/%d"]
    for pattern in date_patterns:
        try:
            return datetime.datetime.strptime(a, pattern)
        except:
            pass

def loginview(request):
    if request.method =='POST':
        post_body = request.body.decode('utf-8')
        body = json.loads(post_body)
        customer_number= body['CustomerNumber']
        user_name= body['UserName']
        password = body['Password']
        try:
            user = Meas_User.objects.get(username=user_name)
            mandant = user.Mandant
            if(customer_number!=mandant.Mandant_accn):
                raise exceptions.ValidationError()
            user = authenticate(username=user_name, password=password)
            if user is not None:
                login(request, user)
                return HttpResponse(status = 200)
            else:
                return HttpResponse(status = 403)
        except Meas_User.DoesNotExist:
            return HttpResponse(status = 403)
        except exceptions.ValidationError:
            return HttpResponse(status = 403)
    return render(request, 'meas/registration/login.html')

def logoutview(request):
    logout(request)
    return render(request, 'meas/registration/login.html')

class EmployeeList(APIView):
    permission_classes = [IsAuthenticated,BelongsToClient]
    serializer_class = EmployeeSerializer
    
    def get(self, request, format=None):
        employees = EmployeeModel.objects.filter(Mandant=request.user.Mandant, Employees_deleted= False)
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

class CustomerList(APIView):
    permission_classes = [IsAuthenticated,BelongsToClient]
    serializer_class= CustomerSerializer

    def get(self, request, format=None):
        customer = CustomerModel.objects.filter(Mandant=request.user.Mandant, Customer_deleted= False)
        serializer = CustomerSerializer(customer, many=True)
        rtn = {
            'data': serializer.data
        }
        return Response(rtn)

class Employee(APIView):
    permission_classes = [IsAuthenticated,BelongsToClient]
    serializer_class = EmployeeSerializer

    def get(self, request, pk, format=None):
        try:
            employee = EmployeeModel.objects.filter(Employees_deleted= False).get(pk=pk)
        except EmployeeModel.DoesNotExist:
            return HttpResponse(status = 404)
        self.check_object_permissions(request, employee)
        serializer = EmployeeSerializer(employee, many=False)
        return Response(serializer.data)

    def post(self, request, format=None):
        try:
            mandant = request.user.Mandant
            mandant = mandant.Mandant_id
        except:
            return HttpResponse(status=403)
        request.data.update({'Mandant': mandant})
        serializer = EmployeeSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        try:
            mandant = request.user.Mandant
            mandant = mandant.Mandant_id
        except:
            return HttpResponse(status=403)
        request.data.update({'Mandant': mandant})
        try:
            employee = EmployeeModel.objects.filter(Employees_deleted= False).get(pk=pk)
        except EmployeeModel.DoesNotExist:
            return HttpResponse(status = 404)
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        print(serializer.errors)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            employee = EmployeeModel.objects.filter(Employees_deleted= False).get(pk=pk)
        except EmployeeModel.DoesNotExist:
            return HttpResponse(status = 404)
        self.check_object_permissions(request, employee)
        employee.Employees_deleted = True
        employee.save()
        return Response(status=status.HTTP_202_ACCEPTED)

class ProductList(APIView):
    permission_classes = [IsAuthenticated,BelongsToClient]
    serializer_class= ProductListSerializer

    def get(self, request, format=None):
        prod = ProductModel.objects.filter(Mandant=request.user.Mandant, Product_deleted= False)
        serializer = ProductListSerializer(prod, many=True)
        rtn = {
            'data': serializer.data
        }
        return Response(rtn)

class Product(APIView):
    permission_classes = [IsAuthenticated,BelongsToClient]
    serializer_class = ProductSerializer

    def get(self, request, pk, format=None):
        try:
            prod = ProductModel.objects.filter(Product_deleted= False).get(pk=pk)
        except ProductModel.DoesNotExist:
            return HttpResponse(status = 404)
        self.check_object_permissions(request, prod)
        serializer = ProductSerializer(prod, many=False)
        return Response(serializer.data)

    def post(self, request, format=None):
        try:
            mandant = request.user.Mandant
            mandant = mandant.Mandant_id
        except:
            return HttpResponse(status=403)
        request.data.update({'Mandant': mandant})
        serializer = ProductSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        try:
            mandant = request.user.Mandant
            mandant = mandant.Mandant_id
        except:
            return HttpResponse(status=403)
        request.data.update({'Mandant': mandant})
        try:
            prod = ProductModel.objects.filter(Product_deleted= False).get(pk=pk)
        except ProductModel.DoesNotExist:
            return HttpResponse(status = 404)
        serializer = ProductSerializer(prod, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        print(serializer.errors)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            prod = ProductModel.objects.filter(Product_deleted= False).get(pk=pk)
        except ProductModel.DoesNotExist:
            return HttpResponse(status = 404)
        self.check_object_permissions(request, prod)
        prod.Product_deleted = True
        prod.save()
        return Response(status=status.HTTP_202_ACCEPTED)
    
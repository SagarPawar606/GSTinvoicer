from django.shortcuts import redirect, render, HttpResponse
from .forms import (UserRegistrationForm, 
                    OrganizationProfileForm, 
                    RecipientDetailsForm,
                    InvoiceDetialsForm,
                    ExtraChargesForm,
                    ItemsFormset, MailForm)
from .models import OrganizationlDetials
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from num2words import num2words
from django.core.mail import send_mail

# Create your views here.
def index(request):
    return render(request, 'base/index.html')

def register_user(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            organization_name = form.cleaned_data['organization_name']
            user = User.objects.get(username=username)
            org_obj = OrganizationlDetials.objects.create(user=user, org_name=organization_name)
            org_obj.save()
            messages.success(request, f'Successfully created account for {username}')

            #log in user & redirect to homepage
            new_user = authenticate(username=username, password=form.cleaned_data['password1'])
            login(request, new_user)
            return redirect('index')
    else:
        form = UserRegistrationForm()
    return render(request, 'base/registration.html', {'form':form, 'title':'User Registration'})



@login_required
def orgnization_profile(request):
    if request.method == 'POST':
        form = OrganizationProfileForm(request.POST, instance=request.user.organizationldetials)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been saved successfully !')
            return redirect('index')
    else:
        form = OrganizationProfileForm(instance=request.user.organizationldetials)
    
    return render(request, 'base/profile.html', {'form':form, 'title':'Profile'})


@login_required
def invoice(request):
    if request.method == 'POST':
        rcpt_form = RecipientDetailsForm(request.POST)
        inv_detail_form = InvoiceDetialsForm(request.POST)
        item_formset = ItemsFormset(request.POST)
        extra_form = ExtraChargesForm(request.POST)

        '''There will be three dictionary to store invoice related data
            invoice_dict - will store recipient data, invoice detials(invoice no, delivery date...)
            items_dict - will store each item's data
            pricing_dict - will store final pricing related data
        '''
        invoice_dict = {}
        items_dict = {}
        pricing_dict = {}

        if rcpt_form.is_valid() and inv_detail_form.is_valid() and extra_form.is_valid() and item_formset.is_valid():
            # recipient details
            for key, value in rcpt_form.cleaned_data.items():
                invoice_dict[key] = value
            
            # invoice detials
            for key, value in inv_detail_form.cleaned_data.items():
                invoice_dict[key] = value
        
        # if item_formset.is_valid() and extra_form.is_valid():
            before_tax_total = 0
            after_tax_total = 0
            total_tax_amount = 0
            
            def calculate_gst(price, cgst, sgst):
                cgst_value = (price/100) * cgst
                sgst_value = (price/100) * sgst
                return [price + cgst_value + sgst_value, cgst_value, sgst_value]

            for i, form in enumerate(item_formset, start=1):
                if form.is_valid():
                    items_dict[str(i)] = {}
                    item = items_dict[str(i)]

                    #item details
                    for key, value in form.cleaned_data.items():
                        item[key] = value

                    price = form.cleaned_data['price']
                    quantity = form.cleaned_data['quantity']
                    cgst = form.cleaned_data['cgst']
                    sgst = form.cleaned_data['sgst']
                    gst_exclusive_price = price * quantity
                    tax_amount = calculate_gst(gst_exclusive_price, cgst, sgst)
                    item['gst_inclusive_price'] = tax_amount[0]
                    item['cgst_amnt'] = tax_amount[1]
                    item['sgst_amnt'] = tax_amount[2]
                    item['gst_exclusive_price'] = gst_exclusive_price
                    before_tax_total = before_tax_total + gst_exclusive_price
                    after_tax_total = after_tax_total + tax_amount[0]
                    total_tax_amount = total_tax_amount + tax_amount[1] + tax_amount[2]

            discount = extra_form.cleaned_data['discount']
            shipping = extra_form.cleaned_data['shipping']
            if discount is None:
                discount = 0
            if shipping is None:
                shipping = 0
            pricing_dict['discount'] = discount
            pricing_dict['shipping'] = shipping

            discounted_total = after_tax_total - discount
            grand_total = round(discounted_total + shipping)
            
            pricing_dict['before_tax_total'] = before_tax_total
            pricing_dict['after_tax_total'] = after_tax_total
            pricing_dict['total_tax_amount'] = total_tax_amount
            pricing_dict['discounted_total'] = discounted_total
            pricing_dict['grand_total'] = grand_total
            total_in_words = num2words(grand_total)
            pricing_dict['total_in_words'] = total_in_words.title()

            pdf_context_data = {
                'invoice_detail':invoice_dict,
                'items':items_dict,
                'pricing':pricing_dict,
            }

            return render(request, 'base/pdf_invoice.html', pdf_context_data)
    else:
        rcpt_form = RecipientDetailsForm()
        inv_detail_form = InvoiceDetialsForm()
        item_formset = ItemsFormset()
        extra_form = ExtraChargesForm()
        
        context = {'rcpt_form' : rcpt_form, 
                    'inv_det_form' : inv_detail_form, 
                    'item_formset':item_formset,
                    'extra_form': extra_form,   
                    'title':'Invoice Form' 
                    }
        return render(request, 'base/invoice-form.html', context)


def sendmail(request):
    if request.method == 'POST':
        form = MailForm(request.POST)
        if form.is_valid():
            mail_from = form.cleaned_data['email_from']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            try:
                send_mail(
                    subject = f'[GSTinvoicer] - {subject}',
                    message = f'From : {mail_from} \n {message}',
                    from_email = mail_from,
                    recipient_list = ['sagarpawar606@gmail.com',],
                    fail_silently = False,
                )
                messages.success(request, 'Mail sent successfully !')
            except Exception as e:
                messages.error(request, 'Something went wrong ! Try again later')
                print(f'[MAIL_ERROR] : {e}')
    else:
        form = MailForm()
    return render(request, 'base/mail.html', {'form':form, 'title':'Send Message'})
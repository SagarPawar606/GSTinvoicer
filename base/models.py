from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class OrganizationlDetials(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    org_name = models.CharField(max_length=255, verbose_name='Organization Name', blank=True, null=True)
    gstin = models.CharField(max_length=15, blank=True, null=True, unique=True)
    address = models.TextField(verbose_name='Address', null=True, blank=True)
    contact_no = models.CharField(max_length=100, verbose_name='Contact Number', null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    upi = models.CharField(max_length=100, verbose_name='UPI No', null=True, blank=True)
    bank_name = models.CharField(max_length=255, verbose_name='Bank Name', blank=True, null=True)
    branch_name = models.CharField(max_length=255, verbose_name='Branch Name', blank=True, null=True)
    account_no = models.CharField(max_length=50, verbose_name='Account No', null=True, blank=True)
    ifsc_code = models.CharField(max_length=50, verbose_name='IFSC Code', null=True, blank=True)


    def __str__(self) -> str:
        return self.user.username + ' Profile'
    
    class Meta:
        verbose_name_plural = "Organizations"


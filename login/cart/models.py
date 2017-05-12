# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class AccountEmailaddress(models.Model):
    email = models.CharField(unique=True, max_length=254)
    verified = models.IntegerField()
    primary = models.IntegerField()
    user = models.ForeignKey('AuthUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_emailaddress'


class AccountEmailconfirmation(models.Model):
    created = models.DateTimeField()
    sent = models.DateTimeField(blank=True, null=True)
    key = models.CharField(unique=True, max_length=64)
    email_address = models.ForeignKey(AccountEmailaddress, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_emailconfirmation'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class BikeDatabase(models.Model):
    bike_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=15)
    vendor = models.ForeignKey('Vend', models.DO_NOTHING, db_column='vendor')
    status = models.IntegerField()
    price = models.IntegerField()
    image = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'bike_database'


class BikeReview(models.Model):
    bike_name = models.CharField(max_length=15)
    customer_name = models.CharField(max_length=15)
    stars = models.IntegerField()
    review = models.CharField(max_length=100)
    date = models.DateField()

    class Meta:
        managed = False
        db_table = 'bike_review'


class BikeStatus(models.Model):
    bike_id = models.ForeignKey(BikeDatabase, models.DO_NOTHING, db_column='bike id')  # Field renamed to remove unsuitable characters.
    name = models.CharField(max_length=15)
    status = models.IntegerField()
    pickup_date = models.DateField()
    drop_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'bike_status'


class Booked(models.Model):
    image = models.CharField(max_length=50)
    bike = models.ForeignKey(BikeDatabase, models.DO_NOTHING, blank=True, null=True)
    bike_name = models.CharField(max_length=15)
    customer_name = models.CharField(max_length=15)
    customer = models.ForeignKey(AuthUser, models.DO_NOTHING)
    customer_num = models.CharField(max_length=15)
    location = models.CharField(max_length=30)
    vendor = models.ForeignKey('Vend', models.DO_NOTHING, db_column='vendor')
    start_date = models.DateField()
    end_date = models.DateField()
    date_of_booking = models.DateField()
    bike_stars = models.IntegerField(db_column='Bike_stars', blank=True, null=True)  # Field name made lowercase.
    bike_review = models.CharField(db_column='Bike_review', max_length=100, blank=True, null=True)  # Field name made lowercase.
    vendor_stars = models.IntegerField(db_column='Vendor_stars', blank=True, null=True)  # Field name made lowercase.
    vendor_review = models.CharField(db_column='Vendor_review', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ridobiko_stars = models.IntegerField(blank=True, null=True)
    ridobiko_review = models.CharField(max_length=100, blank=True, null=True)
    email = models.IntegerField(blank=True, null=True)
    book_time = models.TimeField()

    class Meta:
        managed = False
        db_table = 'booked'


class Cart(models.Model):
    bike_name = models.CharField(db_column='Bike_Name', max_length=15)  # Field name made lowercase.
    vendor = models.ForeignKey('Seller', models.DO_NOTHING, db_column='Vendor')  # Field name made lowercase.
    image = models.CharField(db_column='Image', max_length=15)  # Field name made lowercase.
    price = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cart'


class Cart2(models.Model):
    bike_name = models.CharField(db_column='Bike_Name', max_length=50)  # Field name made lowercase.
    vendor = models.CharField(db_column='Vendor', max_length=50)  # Field name made lowercase.
    image = models.CharField(db_column='Image', max_length=50)  # Field name made lowercase.
    price = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cart2'


class Coupons(models.Model):
    number = models.CharField(max_length=10)
    discount = models.IntegerField()
    start = models.DateField()
    end = models.DateField()

    class Meta:
        managed = False
        db_table = 'coupons'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DjangoSite(models.Model):
    domain = models.CharField(unique=True, max_length=100)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'django_site'


class LogUserprofile(models.Model):
    number = models.CharField(max_length=10)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'log_userprofile'


class RidobikoReview(models.Model):
    customer_name = models.CharField(max_length=15)
    stars = models.IntegerField()
    review = models.CharField(max_length=100)
    date = models.DateField()

    class Meta:
        managed = False
        db_table = 'ridobiko_review'


class Seller(models.Model):
    vendor = models.ForeignKey('Vend', models.DO_NOTHING, db_column='Vendor', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'seller'


class SocialaccountSocialaccount(models.Model):
    provider = models.CharField(max_length=30)
    uid = models.CharField(max_length=191)
    last_login = models.DateTimeField()
    date_joined = models.DateTimeField()
    extra_data = models.TextField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'socialaccount_socialaccount'
        unique_together = (('provider', 'uid'),)


class SocialaccountSocialapp(models.Model):
    provider = models.CharField(max_length=30)
    name = models.CharField(max_length=40)
    client_id = models.CharField(max_length=191)
    secret = models.CharField(max_length=191)
    key = models.CharField(max_length=191)

    class Meta:
        managed = False
        db_table = 'socialaccount_socialapp'


class SocialaccountSocialappSites(models.Model):
    socialapp = models.ForeignKey(SocialaccountSocialapp, models.DO_NOTHING)
    site = models.ForeignKey(DjangoSite, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'socialaccount_socialapp_sites'
        unique_together = (('socialapp', 'site'),)


class SocialaccountSocialtoken(models.Model):
    token = models.TextField()
    token_secret = models.TextField()
    expires_at = models.DateTimeField(blank=True, null=True)
    account = models.ForeignKey(SocialaccountSocialaccount, models.DO_NOTHING)
    app = models.ForeignKey(SocialaccountSocialapp, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'socialaccount_socialtoken'
        unique_together = (('app', 'account'),)


class UserCart(models.Model):
    usename = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='usename')
    bike_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user_cart'


class Vend(models.Model):
    vendor = models.CharField(primary_key=True, max_length=15)
    city = models.CharField(max_length=15)
    landmark = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'vend'


class VendorReview(models.Model):
    vendor = models.CharField(max_length=15)
    customer_name = models.CharField(max_length=15)
    stars = models.IntegerField()
    review = models.CharField(max_length=100)
    date = models.DateField()

    class Meta:
        managed = False
        db_table = 'vendor_review'

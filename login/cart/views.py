from django.shortcuts import render,HttpResponse
from log.models import *
from django.db.models import Count
from django.db.models import Q
from .forms import login_user,bio,registartion_user
from django.contrib.auth import (
    login,
    logout,

)
from operator import itemgetter
from django.db.models import Avg
from django.contrib.auth.models import User
from cart.models import Cart,BikeDatabase,BikeStatus,Vend,Booked
from django.contrib.auth.decorators import login_required
import datetime
from django.core.mail import EmailMessage
from cart.models import BikeReview,VendorReview,RidobikoReview,Coupons




def search_page(request):
    items= Cart.objects.all()
    val = request.GET.get('value')
    bikes=Cart.objects.values_list('bike_name', flat=True).distinct()
    name=request.GET.get('brand')

    if name==None:
        fil_bike=items
    else:
        fil_bike=Cart.objects.filter(bike_name=name).distinct()
        q = Cart.objects.filter(bike_name=name).values('vendor').annotate(tot=Count('bike_name'))


    if request.method == 'GET' and val!=None:
        val= request.GET.get('value')
        k =int(val)
        k = k- (k%1000)
        items=Cart.objects.filter(price__lte=k)
        return render(request,"workspace/homepage_v1/searchPage.html",{"fil_bike":items,"bikes":bikes})

    return render(request,"workspace/homepage_v1/searchPage.html",{"items":items,"fil_bike":fil_bike,"bikes":bikes})

def index_page(request):
    total=Vend.objects.all().values_list('city')
    places=total.distinct()
    list=[]
    for i in places:
        list.append(i[0].encode('utf-8'))
    date=datetime.date.today()
    try:
        le=len(request.session['final'])
    except:
        le="0"

    return render(request,"index.html",{"list":list,"date":date,"le":le})


def cart_page(request):

    place=request.GET.get('location')
    print place

    start_date=str(request.GET.get('date1'))
    start_time=request.GET.get('time1')
    end_date=str(request.GET.get('date2'))
    end_time=request.GET.get('time2')
    request.session['place']=place
    request.session['start_date']=start_date
    request.session['end_date'] =end_date
    bikenot=Booked.objects.filter(~(Q(end_date__lte=start_date)|Q(start_date__gte=end_date))).values_list('bike_id',flat=True)
    total = Vend.objects.all().values_list('city',flat=True).distinct()
    list=[]
    for i in bikenot:
        k=int(i)
        list.append(k)

    base = BikeDatabase.objects.filter((Q(status=1) | (~Q(bike_id__in=list))) & Q(vendor__city=place)).values_list('name','vendor','image','vendor__city','price','vendor__landmark')
    bike2=base.values_list('name','image').distinct()

    n=len(bike2)
    bike=[]
    brands=base.values_list('name',flat=True).distinct()
    landmark=base.values_list('vendor__landmark',flat=True).distinct()


    k=0
    for i in bike2:
        lm=base.filter(name=i[0]).values_list('name','vendor','price','image').annotate(Count('name')).distinct()


        for j in lm:
            id = base.filter(name=j[0], vendor=j[1]).values_list('bike_id')
            k= tuple(id[0])
            mm=j
            nnn=mm+k
            print nnn
            bike.append(nnn)



    for o in bike:
        print o
    p=False
    try:
        request.session['final']
    except:
        p=True
    if(p==False):
        ch = request.session['final']
    else:
        ch=[]
    le = 0
    if (ch):
        le = len(request.session['final'])
    print ch

    return render(request,"shop.html",{"bike":bike,"brands":brands,"landmark":landmark,"list":total,"len":le})

def fil_page(request):
    val=request.GET.get('hero',None)
    reverse=False
    if val=='1':
        reverse=False
    elif val=='2':
        reverse =True
    else:
        reverse = False
    chk=[]
    check = request.GET.getlist('brand',None)
    land=request.GET.getlist('land',None)
    chk.append(val);

    price=request.GET.get('price',None)
    min=0
    max=0

    if(price):
        if(price == '1'):
            min=500
            max=1000

        if (price == '2'):
            min=1000
            max=2000
        if (price == '3'):
            min=2000
            max=3000
        if (price == '4'):
            min=3000
            max=4000
        if (price == '5'):
            min=4000
            max=5000
        if (price == '6'):
            min=5000
            max=6000
        if (price == '7'):
            min=6000
            max=10000
        if (price == '8'):
            min=10000
            max=1000000



    if(check and check[0] == 'on'):
        check=None
    if (land and land[0] == 'on'):
        land = None
    chk.append(check)
    chk.append(land)
    chk.append(price)
    place = request.session.get('place')
    start_date = request.session.get('start_date')
    end_date = request.session.get('end_date')
    bikenot = Booked.objects.filter(~(Q(end_date__lte=start_date) | Q(start_date__gte=end_date))).values_list(
        'bike_id', flat=True)


    list = []
    for i in bikenot:
        k = int(i)
        list.append(k)

    base = BikeDatabase.objects.filter((Q(status=1) | (~Q(bike_id__in=list))) & Q(vendor__city=place)).values_list('name','vendor',
                                                                                                                   'image',                                                                                                       'vendor__city',
                                                                                                               'price',
                                                                                                                   'vendor__landmark')

    base2 = base

    if check:
        base=base.filter(Q(name__in=check))
    if land:
        base=base.filter(Q(vendor__landmark__in=land))
    if price:
        base=base.filter(Q(price__gte=min) & Q(price__lt=max))
        print max , min

    landmark = base2.values_list('vendor__landmark', flat=True).distinct()
    bike2 = base.values_list('name', 'image').distinct()
    l= bike2.values_list('name','vendor').order_by('-price').distinct()
    brands=base2.values_list('name',flat=True).distinct()
    total = Vend.objects.all().values_list('city', flat=True).distinct()
    n = len(bike2)
    bike = []
    k = 0
    for i in bike2:
        lm = base.filter(name=i[0]).values_list('name', 'vendor', 'price', 'image').annotate(Count('name')).distinct()

        for j in lm:
            id = base.filter(name=j[0], vendor=j[1]).values_list('bike_id')
            k = tuple(id[0])
            mm = j
            nnn = mm + k
            bike.append(nnn)

    bike.sort(key=lambda x: x[2],reverse=reverse)

    p = False
    try:
        request.session['final']
    except:
        p = True
    if (p == False):
        ch = request.session['final']
    else:
        ch = []

    le=0
    if(ch and (p == False)):
        le=len(request.session['final'])

    return render(request, "shop.html", {"bike": bike,"check":chk, "brands": brands, "landmark": landmark, "list": total,"val":val,"len":le,})


def add_page(request):


    t=True



    name=request.GET.getlist('name')
    vendor=request.GET.getlist('vendor')
    k=name+vendor

    quantity=['1']
    print k+quantity

    if(name==None):
        return HttpResponse(len(request.session['mylist'])-1)


    try:

        request.session['mylist']

    except:
        t=False
        request.session['mylist']=[]
        if(len(k+quantity)>1):
            request.session['mylist'].append(k+quantity)
            request.session.modified = True
        return HttpResponse(len(request.session['mylist'])-1)
    if t==True:
        lm=k+quantity
        if lm in request.session['mylist']:
             return HttpResponse(len(request.session['mylist']) - 1)

        else:
            request.session['mylist'].append(k+quantity)
            request.session.modified=True
            return HttpResponse(len(request.session['mylist'])-1)





def buy_page(request):


    place = request.session.get('place')
    start_date = request.session.get('start_date')
    end_date = request.session.get('end_date')
    if (end_date== None):
        return render(request, "cart.html")
    bikenot = Booked.objects.filter(~(Q(end_date__lte=start_date) | Q(start_date__gte=end_date))).values_list(
        'bike_id', flat=True)

    list = []
    for i in bikenot:
        k = int(i)
        list.append(k)
    base = BikeDatabase.objects.filter((Q(status=1) | (~Q(bike_id__in=list))) & Q(vendor__city=place) ).values_list('name','vendor',
                                                                                                  'image','vendor__city','price', 'vendor__landmark')



    rem = request.GET.get('rem')

    name=request.GET.getlist('name')
    vendor=request.GET.getlist('ven')
    info=request.GET.get('info')
    if(info):
        for i in request.session['mylist']:
            if(len(i)>1):
                if(i[0]==name[0] and i[1]==vendor[0]):
                    return HttpResponse(i[2])


    k=[]
    k=name+vendor
    quantity=request.GET.get('quantity')

    try:
        request.session['quantity']
    except:
        request.session['quantity']=[]

    if quantity:
        for i in request.session['mylist']:
            if(len(i)>1):
                if(i[0]==name[0] and i[1]==vendor[0]):
                   i[2]=quantity
                   request.session.modified=True



    if rem=='1':
        for i in request.session['mylist']:
            if (len(i) > 1):
                if (i[0] == name[0] and i[1] == vendor[0]):
                    request.session['mylist'].remove(i)
                    request.session.modified = True
                    return HttpResponse("success")



    list2 = request.session.get('mylist')

    final=[]
    try:
        for c in list2:
            if(len(c)>1):
                l= [c[2]]

                base2 = base.filter(name=c[0],vendor=c[1]).values_list('name','vendor','price','image').annotate(Count('name')).distinct()

                final.append(base2)
    except:

        return render(request, "cart.html")









    kkk=request.session['mylist']
    lii=[]
    for i in kkk:
        if(len(i)>1):

            lii.append(i)

    request.session['final']=lii

    ch = request.session['final']

    le = 0
    if (ch):
        le = len(request.session['final'])
    return render(request,"cart.html",{"last":final,"len":le})

@login_required(login_url='/login/')
def rate_page(request):

    place = request.session.get('place')
    start_date = request.session.get('start_date')
    end_date = request.session.get('end_date')
    if (end_date == None):
        return render(request, "cart.html")
    bikenot = Booked.objects.filter(~(Q(end_date__lte=start_date) | Q(start_date__gte=end_date))).values_list(
        'bike_id', flat=True)

    list = []
    for i in bikenot:
        k = int(i)
        list.append(k)
    base = BikeDatabase.objects.filter((Q(status=1) | (~Q(bike_id__in=list))) & Q(vendor__city=place)).values_list(
        'name', 'vendor',
        'image', 'vendor__city', 'price', 'vendor__landmark')



    k=request.GET.get('proceed',None)
    name=request.GET.get('bike',None)
    stars=request.GET.get('stars',None)
    review=request.GET.get('review',None)
    vendor=request.GET.get('vendor',None)
    rido=request.GET.get('rido',None)
    date=datetime.date.today()
    username=request.user.username
    if (name and stars and review):
        rev=BikeReview.objects.create(bike_name=name,customer_name=username,stars=stars,review=review,date=date)
    if(vendor and stars and review):
        rev=VendorReview.objects.create(vendor=vendor,customer_name=username,stars=stars,review=review,date=date)
    if(rido and stars and review):
        rev=RidobikoReview.objects.create(customer_name=username,stars=stars,review=review,date=date)
    
    p=True
    try:
        list=request.session['final']


    except:
        list={}
        p=False
    tot_ven = []
    tot_bikes = []
    tot_loop = []

    if (p and k):
        for i in list:
            #print i[0]
            #print "SDf"

            b_name=i[0]
            b_ven=i[1]
            quant=int(i[2])
            print "a"
            id=base.filter(name=b_name,vendor=b_ven).values_list('bike_id',flat=True)
            k=0

            for v in range(0,quant) :
                print "DFf"
                b_id=id[v]
                print id[v]
                cus_name=request.user.username
                cus_id=request.user.id
                loc=request.session['place']
                start_date=request.session['start_date']
                end_date=request.session['end_date']
                book_date=datetime.date.today()
                book_time = datetime.datetime.now().strftime("%H:%M")



                if(cus_name == None):
                    cus_name=request.user.username
                email=request.user.email




                v=Vend.objects.get(vendor=b_ven)

                entry=Booked.objects.create(bike_id=b_id,bike_name=b_name,customer_name=cus_name,customer_id=cus_id,customer_num=9456522297,location=loc,vendor=v,start_date=start_date,end_date=end_date,date_of_booking=book_date,image='pic-5.jpg',book_time=book_time )
                b_new_id=BikeDatabase.objects.get(bike_id=b_id)
                bike_new=BikeStatus.objects.create(bike_id=b_new_id,name=b_name,status=2,pickup_date=start_date,drop_date=end_date)

                b_new_id.status=2
                b_new_id.save()




    total=Booked.objects.filter(customer_name=request.user.username).values_list('book_time',flat=True).distinct()

    for j in total:
        tot=Booked.objects.filter(Q(book_time=j)).values_list('location','start_date','end_date').distinct()
        tot_loop.append(tot)
        ven = Booked.objects.filter(Q(book_time=j)).values_list('vendor', 'vendor__landmark').distinct()
        tot_ven.append(ven)
        bike = Booked.objects.filter(Q(book_time=j)).values_list('bike_name', 'image')
        tot_bikes.append(bike)
    p = zip(tot_bikes, tot_ven)
    t = zip(tot_loop, p)
    n=len(total)
    list2=[[] * n for x in xrange(n)]
    for x in range(0,len(tot_ven)):
        for y in range(0,len(tot_ven[x])):
            list2[x].append(tot_bikes[x][y]+tot_ven[x][y])
        for z in range(len(tot_ven[x]),len(tot_bikes[x])):
                list2[x].append(tot_bikes[x][z])

    final_list=zip(tot_loop,list2)




    return  render(request,"rate.html",{"list":final_list,"p":p})

@login_required(login_url='/login/')
def history_page(request):
    del request.session['mylist']
    request.session.modified = True
    del request.session['final']
    request.session.modified = True
    print "fsasfs"
    tot_ven = []
    tot_bikes = []
    tot_loop = []
    cancel=request.GET.get('cancel',None)



    total = Booked.objects.filter(customer_name=request.user.username).values_list('book_time', flat=True).distinct()

    if(cancel):
        lm = int(cancel)
        emp=Booked.objects.filter(Q(book_time=total[lm-1]))
        emp.delete()
        de=emp.values_list('bike_id',flat=True)


    for j in total:
        tot = Booked.objects.filter(Q(book_time=j)).values_list('location', 'start_date', 'end_date').distinct()
        tot_loop.append(tot)
        bike = Booked.objects.filter(Q(book_time=j)).values_list('bike_name', 'image','vendor','bike_id__price').annotate(Count('bike_name')).distinct()
        tot_bikes.append(bike)

    n = len(total)
    list2 = [[] * n for x in xrange(n)]

    final_list = zip(tot_loop, tot_bikes)


    return render(request,"bookingHis.html",{'list':final_list})

def detail_page(request):
    id=request.GET.get('id')
    left=request.GET.get('left')
    bike=BikeDatabase.objects.filter(bike_id=id).values_list('name','bike_id','vendor','price','image')
    review=VendorReview.objects.filter(vendor=bike[0][2]).values_list('customer_name','stars','review','date').distinct()
    avg = VendorReview.objects.filter(vendor=bike[0][2]).values_list('customer_name', 'stars', 'review',
                                                                        'date').distinct().aggregate(Avg('stars'))

    k= int(avg['stars__avg'])
    try:
        le=len(request.session['final'])
    except:
        le="0"
    return render(request,"detail.html",{'list':bike,'left':left,'review':review,"le":le,'k':k})

def dis_page(request):
    date = datetime.date.today()
    coup=Coupons.objects.filter(Q(start__lte=date) & Q(end__gte=date)).values_list('number','discount')
    cop= request.GET.get('coup')
    for i in coup:
        if(cop==i[0]):
            return HttpResponse(i[1])
        else:
            return HttpResponse("0")
    return HttpResponse("0")






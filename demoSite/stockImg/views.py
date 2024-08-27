from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
import razorpay

def hello(request):
    return HttpResponse("Hello World")

def demo(request):
    return render(request,"index.html")

def demoList(request):
    myList=[
        {"sname":'amaan',"roll_no":101},
        {"sname":'mayur',"roll_no":102},
        {"sname":'harsh',"roll_no":103}
    ]
    return render(request,"display.html",{"myList":myList})

def loadlogin(request):
     return render(request,"login.html")

def login(request):
    uname=request.POST.get("txtUname")
    pwd=request.POST.get("txtPwd")

    luser=user.objects.filter(username=uname,password=pwd).first()

    if(luser):
         request.session["uid"]=luser.userid
         request.session["uname"]=luser.username

         return redirect('./home')
    else:
        temp={"msg":"Invalid Username or Password"}
        return render(request,"login.html",temp)

def register(request):
    uname=request.POST.get("txtUname")
    pwd=request.POST.get("txtPwd")
    mail=request.POST.get("txtEmail")
    ph_no=request.POST.get("txtPh_No")
    image=request.FILES.get("img")
    biodata=request.POST.get("txtBio")
    gen=request.POST.get("gender")
    d_o_b=request.POST.get("txtDate")

    ct=ucity.objects.filter(cityid=request.POST.get("txtCity")).first()
    
    print(ct)
    us=user(username=uname,
            password=pwd,
            email=mail,
            phone_number=ph_no,
            cityid=ct,
            profile_pic=image,
            bio=biodata,
            gender=gen,
            dob=d_o_b
            )
    us.save()
    return redirect('./loadLogin')

def home(request):
    return render(request,"newsfeed.html")


def loadUploadImage(request):
    return render(request,"uploadImage.html")

def uploadImg(request):
     userinfo=user.objects.filter(userid=request.session["uid"]).first()
     upImg=img(userid=userinfo,
               url=request.FILES.get("fup"),
               price=request.POST.get("txtPrice"),
               description=request.POST.get("txtDesc")
               )
     upImg.save()    
     return redirect("./profile")

def profile(request):
    if(request.GET.get("uid")):
        useri=user.objects.filter(userid=request.GET.get("uid")).first()
    else:
        useri=user.objects.filter(userid=request.session["uid"]).first()

    temp={
         "userInfo":useri,
         "images":img.objects.filter(userid=useri).values()
          }
    return render(request,"profile.html",temp)

def about(request):
    if(request.GET.get("uid")):
        useri=user.objects.filter(userid=request.GET.get("uid")).first()
    else:
        useri=user.objects.filter(userid=request.session["uid"]).first()

    temp={
         "userInfo":useri,
          }
    return render(request,'about.html',temp)

def photos(request):
    if(request.GET.get("uid")):
        useri=user.objects.filter(userid=request.GET.get("uid")).first()
    else:
        useri=user.objects.filter(userid=request.session["uid"]).first()

    temp={
        "userInfo":useri,
        "image":img.objects.filter(userid=useri).values()
    }
    return render(request,"photos.html",temp)

def albums(request):
    if(request.GET.get("uid")):
        useri=user.objects.filter(userid=request.GET.get("uid")).first()
    else:
        useri=user.objects.filter(userid=request.session["uid"]).first()

    temp={
        "userInfo":useri,
        "album":album.objects.filter(userid=useri)
    }
    return render(request,"albums.html",temp)

def loadUploadAlbum(request):
    return render(request,"addAlbum.html")

def uploadAlbum(request):
    userinfo=user.objects.filter(userid=request.session["uid"]).first()
    upAlbum=album(userid=userinfo,
                  thumbnail=request.FILES.get("fup"),
                  title=request.POST.get("txtTitle"),
                  description=request.POST.get("txtDesc")
                  )
    upAlbum.save()
    return redirect("./albums")

def followers(request):
    return render(request,"followers.html")

def following(request):
    return render(request,"following.html")

def imageInfo(request):
    pid=request.GET.get("pid")
    imageInfo=img.objects.filter(imageid=pid).first()
    comments=comment.objects.filter(imageid=pid)
    
    likes=like.objects.filter(imageid=img.objects.filter(imageid=pid).first())
    saves=save.objects.filter(imageid=img.objects.filter(imageid=pid).first())
    
    
    userInfo=user.objects.filter(userid=request.session["uid"]).first()
    haveBought=len(order.objects.filter(imageid=imageInfo,userid=userInfo))
    pid=request.GET.get("pid")

    myLikes=like.objects.filter(userid=userInfo,
                imageid=img.objects.filter(imageid=pid).first()
                )
    
    mySaves=save.objects.filter(userid=userInfo,
                imageid=img.objects.filter(imageid=pid).first()
                )
    from django.conf import settings
    client=razorpay.Client(auth=(settings.KEY,settings.SECRET))
    payment=client.order.create({"amount":imageInfo.price*100,"currency":"INR","payment_capture":1})
    temp={
        "imageInfo":imageInfo,
        "comms":comments,
        "likes":likes,
        "saves":saves,
        "hasLike":len(myLikes),
        "hasSave":len(mySaves),
        "payment":payment,
        "tb":haveBought
    }
    return render(request,"imageInfo.html",temp)

def addCommnet(request):
    pid=request.GET.get("pid")

    c=comment(userid=user.objects.filter(userid=request.session['uid']).first(),
              imageid=img.objects.filter(imageid=pid).first(),
              comment=request.POST.get("txtComment")
              )
    c.save()
    return redirect("../imageInfo/?pid="+pid)

def albumPhoto(request):
    tid=request.GET.get("tid")
    albumInfo=album.objects.filter(albumid=tid).first()
    photos=img.objects.filter(imageid__in=(albumimage.objects.filter(albumid=albumInfo).only("imageid")))
    temp={
        "albumInfo":albumInfo,
        "photos":photos,
        "totImg":len(photos)
    }
    return render(request,"album_photo.html",temp)

def uploadAlbumImage(request):

    userinfo=user.objects.filter(userid=request.session["uid"]).first()
    upImg=img(userid=userinfo,
               url=request.FILES.get("fup"),
               price=request.POST.get("txtPrice"),
               description=request.POST.get("txtDesc")
               )
    upImg.save()    

    tid=request.GET.get("tid")
    ai=albumimage(
        albumid=album.objects.filter(albumid=tid).first(),
        imageurl=img.objects.latest("imageid")
    )
    ai.save()
    return redirect("../albumPhoto/?tid="+tid)

def insertLike(request):
    userInfo=user.objects.filter(userid=request.session["uid"]).first()
    pid=request.GET.get("pid")
    imgs=img.objects.filter(imageid=pid).first()

    likeadd=like(userid=userInfo,
                imageid=imgs
                )
    likeadd.save()
    return redirect("../imageInfo/?pid="+pid)

def deleteLike(request):
    userInfo=user.objects.filter(userid=request.session["uid"]).first()
    pid=request.GET.get("pid")
    imgs=img.objects.filter(imageid=pid).first()
    likedel=like.objects.filter(userid=userInfo,
                imageid=imgs
                ).first()
    likedel.delete()
    return redirect("../imageInfo/?pid="+pid)

def insertSave(request):
    userInfo=user.objects.filter(userid=request.session["uid"]).first()
    pid=request.GET.get("pid")
    imgs=img.objects.filter(imageid=pid).first()
    addSave=save(userid=userInfo,
                imageid=imgs
                )
    addSave.save()
    return redirect("../imageInfo/?pid="+pid)

def deleteSave(request):
    userInfo=user.objects.filter(userid=request.session["uid"]).first()
    pid=request.GET.get("pid")
    imgs=img.objects.filter(imageid=pid).first()
    delSave=save.objects.filter(userid=userInfo,
                    imageid=imgs
                    ).first()
    delSave.delete()
    return redirect("../imageInfo/?pid="+pid)

def savedPhoto(request):
    userInfo=user.objects.filter(userid=request.session["uid"]).first()
    usaveimg=save.objects.filter(userid=userInfo)

    saveImgs=[]
    for x in usaveimg:
        saveImgs.append(x.imageid.imageid)

    photos=img.objects.filter(imageid__in=saveImgs)
    temp={
        "photos":photos,
        "totImg":len(photos)
    }
    return render(request,"savedPhoto.html",temp)

def otherUser(request):
    useri=user.objects.filter(userid=request.GET.get("uid")).first()
    temp={
         "userInfo":useri,
         "images":img.objects.filter(userid=useri).values()
          }
    return render(request,"otheruserprofile.html",temp)

def searchImage(request):
    userInfo=user.objects.filter(userid=request.session["uid"]).first()
    temp={
        "userInfo":userInfo,
        "image":img.objects.filter(userid=userInfo).values()
    }
    return render(request,"searchImage.html",temp)

def base(request):
    return render(request,"base.html")

def allPhoto(request):
    imageInfo=img.objects.all()
    temp={
        "imageInfo":imageInfo
    }
    return render(request,"allPhoto.html",temp)

def likedPhoto(request):
    userInfo=user.objects.filter(userid=request.session["uid"]).first()
    ulikeimg=like.objects.filter(userid=userInfo)

    likeImgs=[]
    for x in ulikeimg:
        likeImgs.append(x.imageid.imageid)

    photos=img.objects.filter(imageid__in=likeImgs)
    temp={
        "photos":photos,
        "totImg":len(photos)
    }
    return render(request,"likedPhoto.html",temp)

def payment_success(request):
    iid=request.GET.get("iid")
    rpid=request.GET.get("rpid")
    roid=request.GET.get("roid")
    rs=request.GET.get("rs")

    im=img.objects.filter(imageid=iid).first()
    order(
        imageid=im,
        userid=user.objects.filter(userid=request.session['uid']).first(),   
        price=im.price,
        razorpay_payment_id=rpid,
        razorpay_order_id=roid,
        razorpay_signature=rs,
    ).save()

    return render(request,"success.html")


def download(request):
    id=request.GET.get("id")
    i=img.objects.filter(imageid=id).first()
    #file_name = i.title
    path_to_file = "http://127.0.0.1:8000/media/"
    response = HttpResponse(mimetype='application/force-download')
    response['Content-Disposition'] = 'attachment;%s'%(i.url)
    response['X-Sendfile'] =path_to_file
    return response

def orders(request):
    o=order.objects.filter(userid=user.objects.filter(userid=request.session['uid']).first())
    temp={
        "orders":o
    }
    return render(request,"orders.html",temp)

def header(request):
    userInfo=user.objects.filter(userid=request.session["uid"]).first()
    temp={
        "userInfo":userInfo
    }
    return render(request,"header.html",temp)

def logout(request):
	# del request.session['uid']
	# del request.session['uid']
	# del request.session['uid']
	return redirect("./loadLogin")
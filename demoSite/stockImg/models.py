from django.db import models

class country(models.Model):
    countryid=models.AutoField(primary_key=True)
    countryname=models.TextField(max_length=20)

    def __str__(self):
        return self.countryname

class state(models.Model):
    stateid=models.AutoField(primary_key=True)
    statename=models.TextField(max_length=20)
    countryid=models.ForeignKey(country,on_delete=models.CASCADE)

    def __str__(self):
        return self.statename
    
class ucity(models.Model):
    cityid=models.AutoField(primary_key=True)
    cityname=models.TextField(max_length=20)
    stateid=models.ForeignKey(state,on_delete=models.CASCADE)

    def __str__(self):
        return self.cityname
    
class user(models.Model):
    userid=models.AutoField(primary_key=True)
    username=models.TextField(max_length=30)
    password=models.TextField(max_length=15)
    email=models.TextField(max_length=50)
    phone_number=models.TextField(max_length=15)
    cityid=models.ForeignKey(ucity,on_delete=models.CASCADE)
    profile_pic=models.ImageField(upload_to='media/images',default="default.jpg")
    bio=models.TextField(max_length=150)
    register_date_time=models.DateTimeField(auto_now=True)
    gender=models.TextField(max_length=15,null=True)
    dob=models.DateField(null=True)

    def __str__(self):
        return self.username

class catagory(models.Model):
    catagoryid=models.AutoField(primary_key=True)
    catagoryname=models.TextField(max_length=20)

    def __str__(self):
        return self.catagoryname
    
class img(models.Model):
    imageid=models.AutoField(primary_key=True)
    title=models.TextField(max_length=100,default="--Not Defined--")
    url=models.ImageField(upload_to='media/images')
    is_approved=models.BooleanField(default=False)
    status=models.IntegerField(default=0)
    userid=models.ForeignKey(user,on_delete=models.CASCADE)
    description=models.TextField(max_length=1000)
    price=models.IntegerField(default=0)
    catagoryid=models.ForeignKey(catagory,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.userid.username+"/"+str(self.imageid)

class like(models.Model):
    likeid=models.AutoField(primary_key=True)
    userid=models.ForeignKey(user,on_delete=models.CASCADE)
    imageid=models.ForeignKey(img,on_delete=models.CASCADE)

    def __str__(self):
        return "like/"+self.imageid.title+"/"+(self.userid.username)
    
class comment(models.Model):
    commentid=models.AutoField(primary_key=True)
    userid=models.ForeignKey(user,on_delete=models.CASCADE)
    imageid=models.ForeignKey(img,on_delete=models.CASCADE)
    comment=models.TextField(max_length=100)
    date_time=models.DateTimeField(auto_now=True)

    def __str__(self):
        return "comment/"+self.imageid.title+"/"+(self.userid.username)
    
class save(models.Model):
    saveid=models.AutoField(primary_key=True)
    userid=models.ForeignKey(user,on_delete=models.CASCADE)
    imageid=models.ForeignKey(img,on_delete=models.CASCADE)

    def __str__(self):
        return self.userid.username
    
class album(models.Model):
    albumid=models.AutoField(primary_key=True)
    userid=models.ForeignKey(user,on_delete=models.CASCADE)
    title=models.TextField(max_length=50)
    status=models.IntegerField(default=0)
    description=models.TextField(max_length=300)
    thumbnail=models.ImageField(upload_to="media/images",default="default.jpg")

    def __str__(self):
        return self.title
    
class albumimage(models.Model):
    albumimageid=models.AutoField(primary_key=True)
    albumid=models.ForeignKey(album,on_delete=models.CASCADE)
    imageurl=models.ForeignKey(img,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.albumid)
    

class tags(models.Model):
    tagid=models.AutoField(primary_key=True)
    tag=models.TextField(max_length=50)
    catagoryid=models.ForeignKey(catagory,on_delete=models.CASCADE)

    def __str__(self):
        return self.tag
    
class order(models.Model):
    orderid=models.AutoField(primary_key=True)
    imageid=models.ForeignKey(img,null=True,on_delete=models.CASCADE)
    userid=models.ForeignKey(user,null=True,on_delete=models.CASCADE)
    OrderDateTime=models.DateTimeField(auto_now=True)
    price=models.IntegerField(default=0)
    razorpay_payment_id=models.CharField(max_length=200,null=True)
    razorpay_order_id=models.CharField(max_length=200,null=True)
    razorpay_signature=models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.orderid
    
# class follow(models.Model):
#     followid=models.AutoField(primary_key=True)
#     followerid=models.ForeignKey(user,on_delete=models.CASCADE)
#     userid=models.ForeignKey(user,on_delete=models.CASCADE)

#     def __str__(self):
#         return self.userid
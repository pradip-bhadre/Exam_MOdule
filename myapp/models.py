from django.db import models

# Create your models here.
class Person(models.Model):
     pid = models.IntegerField(primary_key=True)
     name=models.CharField(max_length=50)
     age=models.IntegerField(null=False)
     gender=models.CharField(max_length=10)
     def __str__(self):
           return "{},{},{},{}".format(self.pid,self.name,self.age,self.gender)
     class Meta:
          db_table="Person"

class Question(models.Model):

     qno = models.IntegerField(primary_key=True)
     qtext=models.CharField(max_length=50)
     qanswer=models.CharField(max_length=50)
     op1=models.CharField(max_length=50)
     op2=models.CharField(max_length=50)
     subject=models.CharField(max_length=50)
     def __str__(self):
           return "{},{},{},{},{},{}".format(self.qno,self.qtext,self.qanswer,self.op1,self.op2,self.subject)
      
     class Meta:
            db_table="Question"

class Users(models.Model):
     uname=models.CharField(max_length=40)
     upass=models.CharField(max_length=40)

     def __str__(self):
          return "{},{}".format(self.uname,self.upass)

     class Meta:
          db_table="users"
     
class Userdata(models.Model):
     username=models.CharField(max_length=20,primary_key=True)
     password=models.CharField(max_length=20)
     mobno = models.IntegerField()
     
     
     #__str__() function gives us object data .

     def __str__(self):
          return "{},{},{}".format(self.username,self.password,self.mobno)

     class Meta:
          db_table="userdata"

class User(models.Model):
     name=models.CharField(max_length=20,primary_key=True)
     password=models.CharField(max_length=50)
     mobno = models.IntegerField()
     email=models.CharField(max_length=50)
     imagepath=models.CharField(max_length=50)
          
     #__str__() function gives us object data .

     def __str__(self):
          return "{},{},{},{},{}".format(self.name,self.password,self.mobno,self.email,self.imagepath)

     class Meta:
          db_table="user"
     

class Score(models.Model):
     name=models.CharField(max_length=45,primary_key=True)
     subject=models.CharField(max_length=5)
     score = models.IntegerField()

     class Meta:
          db_table="score"


class Student(models.Model):
     rno = models.IntegerField(primary_key=True)
     name=models.CharField(max_length=45)
     marks=models.IntegerField()

     class Meta:
          db_table="student"





from myapp.functions.uploadfileex import fileupload

from myapp.forms import StudentForm
from email import message
from functools import partial
from django.db.models import Max,Min,Sum,Avg,Count
import traceback
from django.shortcuts import render
import json
# Create your views here.  
from django.http import HttpResponse
from myapp.models import Person, Question, Score, Student, User,Users,Userdata

from rest_framework.decorators import api_view

from rest_framework.response import Response

from myapp.serializers import StudentSerializer, UserdataSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views import View
from rest_framework_simplejwt.authentication import JWTAuthentication

class ClassBaseView(View):
    def get(self,request):
        return HttpResponse("<h1>It is get method</h1>")

    def post(self,request):
        return HttpResponse("<h1>It is post method</h1>")

@api_view(['GET','POST'])  
def hello_world(request):
    return Response({"rno":1,"name":"suresh","marks":90})

@api_view(['GET'])
def getUser2(request,username):
    usersfromdb=Userdata.objects.get(username=username)
    print(usersfromdb)
    serilizer=UserdataSerializer(usersfromdb) 
    print('type of serilizer is ' , type(serilizer))
    # serilizalier converts object into python dictionary
    print('type of data is ' , type(serilizer.data))
    return Response(serilizer.data) # Response converts dictionary to json
    #response["Access-Control-Allow-Origin"]="http://localhost:4200"

@api_view(['GET'])
#@authentication_classes([TokenAuthentication])
#@authentication_classes([JWTAuthentication])
#@permission_classes([IsAuthenticated])
def getallusers2(request):
    #print(request.user)
    #print(request.auth)
    usersfromdb=Userdata.objects.all()
    print(usersfromdb)
    serilizer=UserdataSerializer(usersfromdb,many=True)
    return Response(serilizer.data)
    #response["Access-Control-Allow-Origin"]="http://localhost:4200"

@api_view(['POST'])
def addUser2(request):
    serilizer=UserdataSerializer(data=request.data)
    if serilizer.is_valid():
        serilizer.save()
        #serilizer.data is python dictionary . It is converted into 
        # JSON String and sent to client
    return Response(serilizer.data) 
   
#{"username":"suresh","password":"mahesh","mobno":9877}
@api_view(['PUT'])
def updateUser2(request):
    userFromClient=request.data
    usersfromdb=Userdata.objects.get(username=userFromClient["username"])
    serilizer=UserdataSerializer(usersfromdb,data=userFromClient,partial=False)
    if serilizer.is_valid():
        serilizer.save()
    return Response("Record Updated")    

@api_view(['DELETE'])
def deleteUser2(request,username):
    Userdata.objects.filter(username=username).delete()
    response=Response("record deleted")
    return response 
#path("getUser/<username>",views.getUser),
#localhost:8000/getUser/pranit
@api_view(['GET'])
def getUser(request,username):
    usersfromdb=Userdata.objects.get(username=username)
    # userfromdb=>[username=pranit password=python mobno=2334444]
    response=Response({"username":usersfromdb.username,"password":usersfromdb.password,"mobno":usersfromdb.mobno})
    #response["Access-Control-Allow-Origin"]="http://localhost:4200"
    return response

@api_view(['GET'])
def getallUsers(request):
    allusersfromdb=Userdata.objects.all()
    print("generated query is " ,allusersfromdb.query)
    listofusers=[]
    for usersfromdb in allusersfromdb:
        listofusers.append({"username":usersfromdb.username,"password":usersfromdb.password,"mobno":usersfromdb.mobno})
    
    #using each user object , we have created Dictionary and then we added that dictionary in list
    response=Response(listofusers)
    #response["Access-Control-Allow-Origin"]="http://localhost:4200"
    return response

@api_view(['POST'])
def addUser(request):
    print(request.data)
    userFromClient=request.data # JSON String received from client will be converted into dictionary object . It is done by API internally .
    Userdata.objects.create(username=userFromClient["username"],password=userFromClient["password"],mobno=userFromClient["mobno"])
    response=Response({"username":Userdata.username,"password":Userdata.password,"mobno":Userdata.mobno})
    #response["Access-Control-Allow-Origin"]="http://localhost:4200"
    return response

@api_view(['DELETE'])
def deleteUser(request,username):
    Userdata.objects.filter(username=username).delete()
    response=Response("record deleted")
    #response["Access-Control-Allow-Origin"]="http://localhost:4200"
    return response 

@api_view(['PUT'])
def updateUser(request):
    userFromClient=request.data
    usersfromdb=Userdata.objects.get(username=userFromClient["username"])
    usersfromdb.mobno=userFromClient["mobno"]
    usersfromdb.password=userFromClient["password"]
    usersfromdb.save()
    print(usersfromdb)
    response=Response({"username":usersfromdb.username,"password":usersfromdb.password,"mobno":usersfromdb.mobno})
    #response["Access-Control-Allow-Origin"]="http://localhost:4200"
    #response["Access-Control-Allow-Headers"]="content-type"
    return response


def sendJsonList(request):
    data=[{'eno':1,'ename':'sachin','gender':'male'},{'eno':2,'ename':'satish','gender':'male'},{'eno':3,'ename':'seeta','gender':'female'},{'eno':4,'ename':'geeta','gender':'female'}]
    json_data=json.dumps(data) # dumps() converts python dictionary into JSON String
    print(json_data)
    response=HttpResponse(f'{json_data}',content_type='application/json')
    response["Access-Control-Allow-Origin"]="http://localhost:4200";
    return response

      
def hello(request):
    data={
        'rno':2,
        'marks':80
        }
    json_data=json.dumps(data) # dumps() converts python dictionary into JSON String
    print(json_data)
    response=HttpResponse(f'{json_data}',content_type='application/json')
    response["Access-Control-Allow-Origin"]="http://localhost:4200";
    return response


def getJSONData(request):
    print(request.body)
    data={'msg':'data received'};
    
    json_data=json.dumps(data) # dumps() converts python dictionary into JSON String
    print(json_data)
    response=HttpResponse(f'{json_data}',content_type='application/json')

    #json_data=json.loads(request.body.decode('utf-8'))
    #print(json_data)

    response["Access-Control-Allow-Origin"]="http://localhost:4200";
    response["Access-Control-Allow-Headers"]="content-type";
    return response;

def helloDjango(request):  
    return HttpResponse("<h2>Hello, Welcome to Django!</h2>")

def showregister(request):
    return render(request,"register.html")
    
def login1(request):

    uname=request.GET['uname'] # uname coming from browser uname=jbk
    upass=request.GET['upass'] # upass coming from browser upass=python

    usersfromdb=Users.objects.get(uname=uname)#users.objects.get(uname='jbk')
    print(usersfromdb)# usersfromdb is object of Users class .
    #it is having data from database
    
    if uname==usersfromdb.uname and upass==usersfromdb.upass:
        return render(request,'welcome1.html',{'username':uname})
    else:
        return render(request,'login1.html',{'message':'wrong password'})

def login(request):
    #for admin user
    
    uname=request.GET['uname'] # username coming from browser uname=jbk
    upass=request.GET['upass'] # password coming from browser upass=python
    subject=request.GET['subject']
    
    if uname=="admin" and upass=="admin123":
        return render(request,'questionsmanagement.html',{'message':"welcome admin"})

    usersfromdb=Userdata.objects.get(username=uname)#users.objects.get(username='jbk')
    print(usersfromdb)# usersfromdb is object of Userdata class .
    #it is having data from database

    # usersfromdb==>[username=anup,password=anup mobno=123] UserData object

    if uname==usersfromdb.username and upass==usersfromdb.password:
        request.session['username'] = uname
        request.session['password'] = upass
        #request.session['answers'] = []
        request.session['answers'] = {}
        request.session['score'] = 0
        request.session['qno'] = 0
        request.session['duration'] = 61
        questionnumber=4
        questions=Question.objects.filter(subject=subject)
        question=questions[0]
        return render(request,'welcome.html',{'question':question})	    
    else:
        return render(request,'login.html',{'res':'wrong creditals'})

def temp():
        pass
    #    question4=Question.objects.get(qno=questionnumber);
    #    print(type(question4))
    #    print(question4)
    #    question4.qtext='what is captial of tamilnadu'
    #    question4.qanswer='chennai'
    #    question4.op2='chennai'

    #    question4.save()

    #     save() call will ensure that updation done on object will be
    #     reflected in a database
       
    #     insert into question values(4,'what','a','a','b')
    #     Question.objects.create(qno=4,qtext='what',qanswer='a',op1='a',op2='a');

    #    Question.objects.filter(qno=2).delete()
    #    print("record deleted")
            

#localhost:8000
def homepage(request):
    return render(request,'login.html',{'message':"welcome to online exam Portal"})

def register(request):

    username=request.GET['username']
    password=request.GET['password']
    mobno=request.GET['mobno']
    
    try:

        Userdata.objects.create(username=username,password=password,mobno=mobno)
        
    except:

        return render(request,'register.html',{'message':'user is already present',"username":username,"password":password,"mobno":mobno})
    
    return render(request,'login.html',{'message':'registration successful'})

def login2(request):

    uname=request.GET['username'] # username coming from browser uname=jbk
    upass=request.GET['password'] # password coming from browser upass=python

    usersfromdb=Userdata.objects.get(username=uname)#users.objects.get(uname='jbk')
    print(usersfromdb)# usersfromdb is object of Userdata class .
    #it is having data from database
    
    if uname==usersfromdb.username and upass==usersfromdb.password:
        return render(request,'welcome2.html',{'username':uname})
    else:
        return render(request,'login2.html',{'message':'wrong password'})
#qno=2

def next(request):
        try:
            subject=request.GET['subject']
            questions = Question.objects.filter(subject=subject)
            request.session['qno'] = request.session['qno'] +1
            question=questions[request.session['qno']]
            qno=question.qno
            previousAnswer=""
            dictionary=request.session['answers']
            for key,value in dictionary.items():
                if(int(key)==qno):
                    previousAnswer=value[3]
                    break
            return render(request,'welcome.html',{'previousAnswer':previousAnswer,'question':question})
        except:
            print(subject)
            request.session['qno']=0
            question=questions[request.session['qno']]
            qno=question.qno
            previousAnswer=""
            dictionary=request.session['answers']
            for key,value in dictionary.items():
                if(int(key)==qno):
                    previousAnswer=value[3]
                    break
            
            return render(request,'welcome.html',{'previousAnswer':previousAnswer,'question':question})
#0 1 2
def previous(request):
        try:
            subject=request.GET['subject']
            questions = Question.objects.filter(subject=subject)
            
            request.session['qno'] = request.session['qno'] -1
            question=questions[request.session['qno']]
            qno=question.qno
            allentries=request.session['answers']#allentries {1:list,2:list,3:list}
            print(" no of questions attempted ",len(allentries))
            print(" Total no of questions  ",len(questions))

            previousAnswer=""
            for key,value in allentries.items():
                print('key is ',key)
                print('value is ',value)
                questionnumber=key
                print("questionnumber from dictionary ", questionnumber," qno from database ",qno)
                print(type(questionnumber))
                print(type(qno))
                print(questionnumber==qno)
                if int(questionnumber)==qno :
                    print("inside if")
                    previousAnswer=value[3]
                print('PreviousAnswer is ' , previousAnswer)
            return render(request,'welcome.html',{'previousAnswer':previousAnswer,'question':question})
        except:
            traceback.print_exc()
            request.session['qno']=len(questions)-1
            question=questions[request.session['qno']]
            qno=question.qno
            allentries=request.session['answers']#allentries {1:list,2:list,3:list}
            previousAnswer=""
            for key,value in allentries.items():
                print('key is ',key)
                print('value is ',value)
                questionnumber=key
                print("questionnumber is ", questionnumber," qno from dictionary ",qno)
                print(type(questionnumber))
                print(type(qno))
                print(questionnumber==qno)
                if int(questionnumber)==qno :
                    print("inside if")
                    previousAnswer=value[3]
                print('PreviousAnswer is ' , previousAnswer)
            
            return render(request,'welcome.html',{'previousAnswer':previousAnswer,'question':question})

def storeresponse(request):
    
    print(f'Store')  
    
#    resultobj=Result(request.GET['qno'],request.GET['q'],request.GET['a'],request.GET['op'])
 #   print(resultobj)

    
    #listofquestions=request.session['answers']
    #listofquestions.append([request.GET['qno'],request.GET['q'],request.GET['a'],request.GET['op']])
    #request.session['answers']=listofquestions
    #print(f"Updated List is {request.session['answers']}")
    #return render(request,'welcome.html')

    listofquestions=request.session['answers']#{1:list,2:list,3:list} {1:list}
    listofquestions[request.GET['qno']]=list([request.GET['qno'],request.GET['qtext'],request.GET['originalAnswer'],request.GET['submittedAnswer']])
    request.session['answers']=listofquestions

    print(f"Updated Dictioary is {request.session['answers']}")
    return render(request,'welcome.html')

def score(request):
    return render(request,'score.html',{'score':3})

def calculatescore(request):
    try:
        responses=request.session['answers']
        listoflist=responses.values()#[list1,list2,list3]
        
        for list in listoflist:
            #Answer.objects.create(qno=list[0],qtext=list[1],);
            print(f'correct answer {list[2]}  and submitted answer is {list[3]}') 
            if list[2]==list[3]:
                    request.session['score']=request.session['score'] + 1


        finalscore=request.session['score']
        print(f'Your score is {finalscore}')
        username=request.session['username']
        password=request.session['password']        
        logout(request)
    except Exception as msg:
        traceback.print_exc()
        return render(request,'login.html')    
        
    return render(request,'score.html',{'score':finalscore,'responses':listoflist,'username':username,'password':password})    


def getRemainingTime(request):

       request.session['duration'] =   request.session['duration'] - 1
       return HttpResponse(request.session['duration'])


def logout(request):
        
    del request.session['username']
    del request.session['password']
    del request.session['answers']
    del request.session['score']
    del request.session['qno']
    del request.session['duration'] 

    #return render(request,'logout.html')
    return HttpResponse("<Strong>You are loggged out </Strong>")


def saveQuestions(request):
     print(request.GET)
     qno=request.GET['qno'] 
     qtext=request.GET['qtext'] 
     qanswer=request.GET['qanswer'] 
     op1=request.GET['op1']
     op2=request.GET['op2'] 
     subject=request.GET['subject']

     Question.objects.create(qno=qno,qtext=qtext,qanswer=qanswer,op1=op1,op2=op2,subject=subject)
     print("Question is saved in database")
     return render(request,"questionsmanagement.html",{"message":"Question added in database successfully."})

def viewQuestion(request):
    print(request.GET["qno"])
    print(request.GET["subject"])
    question=Question.objects.get(qno=request.GET["qno"],subject=request.GET["subject"])
    print(question)
   
    data={
        'qtext':question.qtext,
        'qanswer':question.qanswer,
        'op1':question.op1,
        'op2':question.op2
        }
    json_data=json.dumps(data) # dumps() converts python dictionary into JSON String
    print(json_data)
    response=HttpResponse(f'{json_data}',content_type='application/json')
    
    return response
                                #  1 | what is 2+2 ?               | 4       | 4    | 50    | maths--database
                                #  1 | what is 2+2 ?            | 4        | 4   | 50   |maths  -- browser
def updateQuestion(request):
        question4=Question.objects.filter(qno=request.GET["qno"],subject=request.GET["subject"])
        question4.update(qtext=request.GET["qtext"],qanswer=request.GET["qanswer"],op1=request.GET["op1"],op2=request.GET["op2"])
        print("Question is updated in database")
        return render(request,"questionsmanagement.html",{"message":"Question updated in database"})

def deleteQuestion(request):
      Question.objects.filter(qno=request.GET["qno"],subject=request.GET["subject"]).delete()
      return render(request,"questionsmanagement.html",{"message":"Question deleted"})

def checkUsername(request):
    print(request.GET["username"])
    message="username already present"
    try:
        userdata=User.objects.get(name=request.GET["username"])
        print(userdata)
    except:
        traceback.print_exc()
        message='username does not exist';

    data={
        'message':message
       
        }
    json_data=json.dumps(data) # dumps() converts python dictionary into JSON String
    print(json_data)
    response=HttpResponse(f'{json_data}',content_type='application/json')
    return response

def databaseop(request):
    # Person.objects.create(pid=3,name='indira',age=20,gender='female')
    # print("record added")
    # return HttpResponse("record added")

    #Person.objects.filter(pid=1).delete()
    #Person.objects.all().delete()
    #return HttpResponse("record deleted")

    #p1=Person.objects.get(pid=1)
    #p1.age=90
    #p1.name='lankesh'
    #p1.save()
    #return HttpResponse("record updated")

    #Person.objects.all().update(age=F('age')-15)
    #return HttpResponse("records updated")

    # person=Person.objects.all().aggregate(Max('age'))
    # print(person) #dictionary {'age_max':90}
    # print(person['age__max'])
    # return HttpResponse('record found')

    # person=Person.objects.all().aggregate(Min('age'))
    # print(person) #dictionary {'age_min':90}
    # print(person['age__min'])
    # return HttpResponse('record found')

    
    # person=Person.objects.all().aggregate(Sum('age'))
    # print(person) #dictionary {'age_sum':90}
    # print(person['age__sum'])
    # return HttpResponse('record found')

    # person=Person.objects.all().aggregate(Avg('age'))
    # print(person) #dictionary {'age_avg':90}
    # print(person['age__avg'])
    # return HttpResponse('record found')

    # counts=Person.objects.count()
    # print(counts)
    # return HttpResponse('count is {}'.format(counts))

    result=Person.objects.values('gender').annotate(count=Count('gender'))
    print(result)
    for obj in result:
        print(obj)
    return HttpResponse('success')
    
def visitGoogle(request):
        return render(request,"https://www.google.co.in")
        
# call=invoke=request
def saveUserData(request):
    
    print(type(request))
    name=request.POST['name']
    password=request.POST['password']
    mobno=request.POST['mobno']
    email=request.POST['email']
    photo=request.FILES['photo']
    imagepath='/upload/'+photo.name

    with open('myapp/static/upload/'+photo.name, 'wb+') as destination:  
                for data in photo.chunks():  
                    destination.write(data)
    
    User.objects.create(name=name,password=password,mobno=mobno,email=email,imagepath=imagepath)
   
    return render(request,'login.html',{'message':'registration successful.please login now','imagepath':imagepath})

def logins(request):

    uname=request.GET["uname"]
    upass=request.GET["upass"]
    subject=request.GET["subject"]
    
    if uname=="admin" and upass=="admin123":
        return render(request,'questionsmanagement.html',{'message':"welcome Teacher. Pls Add Questions in Question Bank"})

    try:
        userfromdb=User.objects.get(name=uname)
    except:
        return render(request,'login.html',{"message":"wrong username",'password':upass})

    if(userfromdb.password==upass):
        questions=Question.objects.filter(subject=subject)
        question=questions[0]
        
        request.session['imagepath']=userfromdb.imagepath

        request.session['qno'] = 0
        request.session['username']=uname
        request.session['subject']=subject
        request.session['answers']={}
        request.session['score']=0

        return render(request,'question.html',{'question':question})
    
    else:
        
        return render(request,'login.html',{"message":"wrong password",'name':uname})
#0 1 2
def nextQuestion(request):

            subject=request.session['subject']
            questions = Question.objects.filter(subject=subject)
            if(request.session['qno']<len(questions)-1):
                request.session['qno'] = request.session['qno'] +1
                question=questions[request.session['qno']]

                # To get previous answer from Dictionary

                qno=question.qno
                responses=request.session['answers'] # get dictionary

                previousAnswer=""

                for key,value in responses.items():
                    if(int(key)==qno):
                        previousAnswer=value[3]
                        break

            else:

                return render(request,'question.html',{'errormessage':"questions over","question":questions[len(questions)-1]})    
            
            return render(request,'question.html',{'question':question,'previousAnswer':previousAnswer,"totalquestions":len(questions),"attemptedquestions":len(request.session['answers']),"remainingquestions":(len(questions)-len(request.session['answers']))})

# 3 2  1 qno
# 2 1  0 index
def previousQuestion(request):
            subject=request.GET['subject']
            questions = Question.objects.filter(subject=subject)
            if(request.session['qno']>0):
                request.session['qno'] = request.session['qno'] -1
                question=questions[request.session['qno']]

                # To get previous answer from Dictionary

                qno=question.qno
                responses=request.session['answers'] # get dictionary

                previousAnswer=""

                for key,value in responses.items():
                    if(int(key)==qno):
                        previousAnswer=value[3]
                        break
                        
                return render(request,'question.html',{'question':question,'previousAnswer':previousAnswer})

            else:
                responses2=request.session['answers'] # get dictionary

                firstQuestion=questions[0]
                fqno=firstQuestion.qno
                preans=""
                
                # in operator is used to check presence of key in dictionary

                if(str(fqno) in responses2):
                    firstanswer=responses2[str(fqno)]
                    preans=firstanswer[3]
                else:
                    preans=""
                return render(request,'question.html',{'errormessage':"questions over","question":questions[0],'previousAnswer':preans})    

def storeanswer(request):
        
        responses=request.session['answers'] # get dictionary
        
        # update dictionary

        responses[request.GET["qno"]]=list([request.GET["qno"],request.GET["qtext"],request.GET["qanswer"],request.GET["op"]])

        print(responses)

        request.session['answers']=responses # update answer attribute

        return render(request,'question.html')

def answerschecking(request):
        
        try:
                responses=request.session['answers']
                allanswers=responses.values()
                
                for answer in allanswers:
                    if(answer[2]==answer[3]):
                        request.session['score']=request.session['score']+1

                del request.session['answers']       
        except:
            
            traceback.print_exc()

            return render(request,'login.html')
        
        #store score in database

        username=request.session['username']
        userscore=request.session['score']
        subject=request.session['subject']
        
        try:
        
            Score.objects.create(name=username,subject=subject,score=userscore)
        
        except:
            
            message="exam of {} is already given".format(subject)

            return render(request,'login.html',{"message":message})


        return render(request,'score.html',{'finalscore':request.session['score'],'allanswers':allanswers})

def result(request):
    return render(request,'score.html')

def endpage(request):
    del request.session['username']
    #print("username from session is ",request.session['username'])
    return render(request,"endpage.html")



def uploadFile(request):  

    if request.method == 'POST':  

        student = StudentForm(request.POST, request.FILES)  
        imagepath=""
        if student.is_valid():  
            print("inside if")
            f=request.FILES['file'] 
            fileupload(f)            
            imagepath='/upload/'+f.name
        return render(request,"imagedisplay.html",{'imagepath':imagepath})
    else:  

        student = StudentForm()  
        return render(request,"uploadex.html",{'form':student})

@api_view(['GET'])
def getStudent(request,rollnumber):
    
    studentfromdb=Student.objects.get(rno=rollnumber)

    # studentfromdb=>[rno=103  name=abhijit marks=95] Student class object

    #seriliazer=StudentSerializer(studentfromdb)

    response=Response({"rno":studentfromdb.rno,"name":studentfromdb.name,"marks":studentfromdb.marks})
    
    #{"rno":103,"name":"abhijit","marks":95}
    #response=Response(seriliazer.data)

    return response

#API can NOT convert Student object into JSON
#API can convert ONLY Dictionary into JSON


@api_view(['POST'])
def receiveStudent(request):
     
     datafromclient=request.data
     print(type(datafromclient))
     print(datafromclient)
     return Response(datafromclient)

@api_view(['POST'])
def saveStudent(request):
     
    datafromclient=request.data
    print(datafromclient) #{"rno":1,"name":"kiranAcademy","marks":90}

    #  rnofromclient=datafromclient["rno"]
    #  namefromclient=datafromclient["name"]
    #  marksfromclient=datafromclient["marks"]

    #  Student.objects.create(rno=rnofromclient,name=namefromclient,marks=marksfromclient)

    serializer=StudentSerializer(data=datafromclient)
    
    if(serializer.is_valid()):
        serializer.save()

    return Response("data stored in database")

@api_view(['PUT'])
def updateStudent(request):
     
    datafromclient=request.data
    
    print(datafromclient) #{"rno":105,"name":"rahul","marks":70}

    # there is already record of rno 105 and we want to update it

    studentfromdb=Student.objects.get(rno=datafromclient["rno"])

    serializer=StudentSerializer(studentfromdb,data=datafromclient,partial=False)
    
    if(serializer.is_valid()):
        serializer.save()

    
    return Response("data updated in database")


@api_view(['DELETE'])
def deleteStudent(request,rollnumber):
    
    Student.objects.get(rno=rollnumber).delete()

    return Response("data deleted in database")



@api_view(['GET'])
def getAllStudents(request):
    
    allstudentsfromdb=Student.objects.all()

    seriliazer=StudentSerializer(allstudentsfromdb,many=True)
    
    response=Response(seriliazer.data)

    return response

def addition(request):
     no1=request.GET['number1']
     no2=request.GET['number2']
     no3=int(no1)+int(no2)
     #return HttpResponse(no3)
     print('result is ',no3)
     return render(request,'addition.html',{'answer':no3,'no1':no1,'no2':no2})

def subtraction(request):
     no1=request.GET['number1']
     no2=request.GET['number2']
     no3=int(no1)-int(no2)
     #return HttpResponse(no3)
     return render(request,'addition.html',{'answer':no3,'no1':no1,'no2':no2})


def setSession(request):
     request.session['sname']="akshay"
     return HttpResponse("attribute added in session object")

def getSession(request):

     try:
        studentname=request.session['sname']
        return HttpResponse(studentname)
     except:
        return HttpResponse("session expired")

def removeSession(request):
     del request.session['sname']
     return HttpResponse("attribute removed")

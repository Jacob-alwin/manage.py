import random as r
import smtplib
from bs4 import BeautifulSoup
import requests
import pyrebase
from django.contrib import messages
from django.shortcuts import render, redirect
import time
from datetime import datetime, timezone
import pytz

# Create your views here.

config = {

    "apiKey": "AIzaSyCztfnYVUT49K8JVDRsL4z1oSxN8lu7V-E",
    "authDomain": "connected-try.firebaseapp.com",
    "databaseURL": "https://connected-try-default-rtdb.firebaseio.com",
    "projectId": "connected-try",
    "storageBucket": "connected-try.appspot.com",
    "messagingSenderId": "1004314390323",
    "appId": "1:1004314390323:web:51d248e16cdf9e15ac5846",
    "measurementId": "G-P0MFRMLT0E",

}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()


def index(request):
    global otp, email, phn, password, gender, uname, status, fullname

    if request.method == 'POST' and 'signin' in request.POST:

        email = request.POST.get("email")
        psw = request.POST.get("psw")
        try:
            auth.sign_in_with_email_and_password(email, psw)
            print("Sucees")

            ufind = db.child('Accounts').shallow().get().val()

            for i in ufind:
                ufinder = db.child('Accounts').child(i).child('e-mail').get().val()
                print(ufinder)
                print(email)
                if ufinder == email:
                    uname = db.child('Accounts').child(i).child('username').get().val()
                    request.session['yourname'] = uname
                    print(uname)
                else:
                    pass

            return redirect("home")
        except:
            print("password or username is wrong")

    if request.method == 'POST' and 'signup' in request.POST:
        print("hlomf")
        email = request.POST.get("email")
        uname = request.POST.get("uname")
        request.session['username'] = uname
        p = request.POST.get("phn")
        password = request.POST.get("psw")
        cpassword = request.POST.get("cpsw")

        phn = str(p)
        print(phn)

        if password == cpassword:
            Break = True

            # searching for existing phone number
            try:
                people = db.child("Accounts").get()
                for p in people.each():
                    x = p.val()
                    if x['phone'] == phn or x['e-mail'] == email or x['username'] == uname:
                        Break = False
                        print('innna')
            except:
                pass
            if Break == True:
                try:
                    # OTP Generator
                    x = r.randint(1000, 9999)
                    otp = str(x)
                    print(otp)

                    # Sending email
                    sender = "connectedsocialmedia40@gmail.com"
                    print(1)
                    reciver = email
                    print(2)
                    psw = "Connected5%%"
                    print(3)
                    msg = otp
                    print(4)

                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    print(5)
                    server.starttls()
                    print(6)
                    server.login(sender, psw)
                    print(7)
                    server.sendmail(sender, reciver, msg)
                    print(8)

                    print("waiting :)")

                    time.sleep(1200)



                except:
                    print("nah...")
            else:
                print("sorry already existing")

    if request.method == 'POST' and 'otp' in request.POST:

        print(otp)

        x1 = request.POST.get('x1')
        x2 = request.POST.get('x2')
        x3 = request.POST.get('x3')
        x4 = request.POST.get('x4')

        x = f"{x1}{x2}{x3}{x4}"

        if x == otp:

            print(email, phn, password)

            data = {
                "e-mail": email,
                "phone": phn,
                "password": password,
                "username": uname

            }

            auth.create_user_with_email_and_password(email, password)
            db.child("Accounts").child(uname).set(data)
            request.session['username'] = uname
            print(request.session['username'], '.......................')
            return redirect("details")
        else:
            print("oops")

    else:
        print("oomb myree")

    return render(request, 'index.html')


def details(request):
    print("glllll")
    uname = request.session['username']
    print("glllll")

    if request.method == 'POST' and 'create' in request.POST:
        r1 = request.POST['choice']
        print(r1)

        r2 = request.POST['choices']
        print(r1)

        def from_dob_to_age(born):
            today = datetime.today()
            return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

        dob = request.POST.get('date')
        dofb = datetime.strptime(dob, '%Y-%m-%d')
        print(dob)
        age = from_dob_to_age(dofb)
        print(age)

        fname = request.POST.get('fname')

        lname = request.POST.get('lname')

        country = request.POST.get('country')
        state = request.POST.get('state')

        fullname = f"{fname} {lname}"
        print('p-----------------------------------p')
        print(fullname)

        data = {

            'uname': uname,
            "age": age,
            "gender": r1,
            "dob": dob,
            "fullname": fullname,
            "fname": fname,
            "lname": lname,
            "status": r2,
            "country": country,
            "state": state,
        }

        tz = pytz.timezone('Asia/Kolkata')
        time_now = datetime.now(timezone.utc).astimezone(tz)
        millis = int(time.mktime(time_now.timetuple()))
        print(" mili " + str(millis))
        url = request.POST.get('url')
        print(url)

        photo = {
            "url": url,
            "time": millis
        }

        db.child("Accounts").child(uname).child("details").set(data)
        db.child('Accounts').child(uname).child('details').child('images').child('profilepic').child(millis).set(photo)
        request.session['yourname'] = uname

        return redirect("home")

    gender = ['Male', 'Female', 'Others']
    status = ['Single', 'Married', 'Not Defined']

    return render(request, "details.html", {'uname': uname, 'gender': gender, 'status': status})


def test(request):
    # people = db.child("Accounts").get()
    # for p in people.each():
    #
    #     x = p.key()
    #     print(x)
    #     z = db.child("Accounts").child(x).get()
    #
    #     for i in z.each():
    #         y = i.val()
    #         print(y)
    people = db.child("Accounts").get()

    for p in people.each():
        x = p.val()
        print(x['username'])

        albin = x['username']

        data = {'alb': albin}
        messages.info(request, data.get('alb'))

    return render(request, "test.html")


def create(request):
    return render(request, 'create.html')


def post_create(request):
    uname = request.session['uname']
    import time
    from datetime import datetime, timezone
    import pytz

    tz = pytz.timezone('Asia/Kolkata')
    time_now = datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime(time_now.timetuple()))
    print(" mili " + str(millis))
    work = request.POST.get('work')
    progress = request.POST.get('progress')
    url = request.POST.get('url')
    print(url)

    # idtoken = request.session['jame']
    # a = auth.get_account_info(idtoken)
    # a = a['Accounts']
    # a = a[0]
    # a = a['james']
    # print("info"+str(a))

    data = {
        "work": work,
        'progress': progress,
        'url': url
    }
    print(url)
    db.child('Accounts').child(uname).child('details').child('images').child('profilepic').child(millis).set(data)
    return render(request, 'test.html')


def home(request):
    import datetime
    try:

        username = request.session['yourname']
        uname = username
        with open("connected.txt", "a") as f:
            f.write("\n")
            f.write(username)
        del request.session['yourname']

    except:

        with open("connected.txt", "r") as f:
            username = f.readlines()
        uname = username[-1]

    print(uname, "456456453265123645325135")

    prot = db.child('Accounts').child(uname).child('details').child('images').child('profilepic').shallow().get().val()


    for i in prot:
        propic = db.child('Accounts').child(uname).child('details').child('images').child('profilepic').child(i).child(
            'url').get().val()
        print(propic)

    name = db.child('Accounts').child(uname).child('details').child('fullname').get().val()

    names = []

    alluser = db.child('Accounts').shallow().get().val()
    print(alluser)
    des = []
    urls = []
    date = []
    all_lis_time = []
    lis_time = []
    adp = []
    so = []
    story = []
    adps = []
    comb_lis = None
    for l in alluser:

        timestamps = db.child('Accounts').child(l).child('details').child('images').child(
            'photos').shallow().get().val()

        photos = True

        try:
            for i in timestamps:
                lis_time.append(i)
                all_lis_time.append(i)

            lis_time.sort(reverse=True)
            all_lis_time.sort(reverse=True)
            print(lis_time)


            print("--------------------------------------------")

        except:
            photos = False

    try:

        for j in lis_time:
            for l in alluser:
                timestamps = db.child('Accounts').child(l).child('details').child('images').child(
                    'photos').shallow().get().val()

                # dpstory = db.child('Accounts').child(l).child('details').child('images').child(
                #     'story').shallow().get().val()
                #
                # for x in dpstory:
                #     allpropics = db.child('Accounts').child(l).child('details').child('images').child(
                #         'story').child(x).child('url').get().val()
                #
                # adps.append(allpropics)
                # stories = db.child('Accounts').child(l).child('details').child('images').child(
                #     'story').shallow().get().val()
                #
                # for x in stories:
                #     storyowner = db.child('Accounts').child(l)
                #     adps.append(allpropics)
                #     storys = db.child('Accounts').child(l).child('details').child('images').child(
                #         'profilepic').child(x).child('url').get().val()
                #     so.append(storyowner)
                #     story.append(storys)

                photos = True
                lis_time = []


                for i in timestamps:
                    if(i == j):
                        allprot = db.child('Accounts').child(l).child('details').child('images').child(
                            'profilepic').shallow().get().val()

                        for x in allprot:
                            allpropic = db.child('Accounts').child(l).child('details').child('images').child(
                                'profilepic').child(x).child('url').get().val()

                        adp.append(allpropic)
                        descrip = db.child('Accounts').child(l).child('details').child('images').child('photos').child(i).child(
                            'description').get().val()
                        des.append(descrip)
                        pic = db.child('Accounts').child(l).child('details').child('images').child('photos').child(i).child(
                            'url').get().val()

                        urls.append(pic)
                        i = float(i)
                        dat = datetime.datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%Y')
                        date.append(dat)
                        allname = db.child('Accounts').child(l).child('details').child('fullname').get().val()
                        names.append(allname)

        print(date)
        print(des)
        print(names)
        print(adp)
        comb_lis = zip(date, des, urls, names, adp)
        # story_lis = zip(so, story, adps)

        # for k in comb_lis:
        #     print("---------------------------------------------------------")
        #     print(k)




    except:
        print("no Photos")
        pass


   # -------------------------- search function ---------------------------------------------

    if request.method == 'POST' and 'search' in request.POST:

        print("sadasdasdasd")
        search = request.POST.get('sea')
        print(search)
        request.session['seacrchname'] = search
        print("asdasdasda")
        return redirect('othersprofile')

    # -----------------------------------------------------------------------------------------

    if request.method == 'POST' and 'upload-post' in request.POST:
        import time
        from datetime import datetime, timezone
        import pytz
        tz = pytz.timezone('Asia/Kolkata')
        time_now = datetime.now(timezone.utc).astimezone(tz)
        millis = int(time.mktime(time_now.timetuple()))
        print(" mili " + str(millis))
        description = request.POST.get('description')
        url = request.POST.get('url')
        print(url)

        data = {
            'time': millis,
            'description': description,
            'url': url
        }

        print(url)
        db.child('Accounts').child(uname).child('details').child('images').child('photos').child(millis).set(data)
        return redirect('home')

    if request.method == 'POST' and 'upload-story' in request.POST:
        import time
        from datetime import datetime, timezone
        import pytz
        tz = pytz.timezone('Asia/Kolkata')
        time_now = datetime.now(timezone.utc).astimezone(tz)
        millis = int(time.mktime(time_now.timetuple()))
        print(" mili " + str(millis))
        url = request.POST.get('url')
        print(url)

        data = {
            'time': millis,
            'url': url
        }

        print(url)
        db.child('Accounts').child(uname).child('details').child('images').child('story').child(millis).set(data)
        return redirect('home')

    return render(request, 'home.html', {'name': name, 'list': comb_lis, 'dp': propic })


def profile(request):

    import datetime
    with open("connected.txt", "r") as f:
        username = f.readlines()
    uname = username[-1]

    prot = db.child('Accounts').child(uname).child('details').child('images').child('profilepic').shallow().get().val()
    for i in prot:
        propic = db.child('Accounts').child(uname).child('details').child('images').child('profilepic').child(i).child(
            'url').get().val()

    name = db.child('Accounts').child(uname).child('details').child('fullname').get().val()

    timestamps = db.child('Accounts').child(uname).child('details').child('images').child(
        'photos').shallow().get().val()

    lis_time = []

    for i in timestamps:
        lis_time.append(i)
    lis_time.sort(reverse=True)
    print(lis_time)

    des = []
    urls = []
    date = []

    for i in lis_time:
        descrip = db.child('Accounts').child(uname).child('details').child('images').child('photos').child(i).child(
            'description').get().val()
        des.append(descrip)

        pic = db.child('Accounts').child(uname).child('details').child('images').child('photos').child(i).child(
            'url').get().val()
        urls.append(pic)

        i = float(i)
        dat = datetime.datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%Y')
        date.append(dat)

    comb_lis = zip(lis_time, date, des, urls)


    alluser = db.child('Accounts').shallow().get().val()
    adp = []
    for l in alluser:

        allprot = db.child('Accounts').child(l).child('details').child('images').child(
            'profilepic').shallow().get().val()

        for x in allprot:
            allpropic = db.child('Accounts').child(l).child('details').child('images').child(
                'profilepic').child(x).child('url').get().val()
        adp.append(allpropic)

    friend = zip(adp, alluser)

    if request.method == 'POST' and 'logout' in request.POST:
        f = open('file.txt', 'r+')
        f.truncate(0)
        redirect("index")

        # -------------------------- search function ---------------------------------------------

    if request.method == 'POST' and 'search' in request.POST:
        print("sadasdasdasd")
        search = request.POST.get('sea')
        print(search)
        request.session['seacrchname'] = search
        print("asdasdasda")
        return redirect('othersprofile')

    # -----------------------------------------------------------------------------------------

    if request.method == 'POST' and 'upload-post' in request.POST:
        import time
        from datetime import datetime, timezone
        import pytz
        tz = pytz.timezone('Asia/Kolkata')
        time_now = datetime.now(timezone.utc).astimezone(tz)
        millis = int(time.mktime(time_now.timetuple()))
        print(" mili " + str(millis))
        description = request.POST.get('description')

        url = request.POST.get('url')
        print(url)

        data = {
            'time': millis,
            'description': description,
            'url': url
        }
        print(url)
        db.child('Accounts').child(uname).child('details').child('images').child('photos').child(millis).set(data)
        return render(request, 'profile.html', {'name': name, 'comb_lis': comb_lis})
    return render(request, 'profile.html', {'name': name, 'comb_lis': comb_lis, 'dp': propic, 'urls': urls, 'friend': friend})


def othersprofile(request):

    import datetime
    username = request.session['seacrchname']
    uname = username

    prot = db.child('Accounts').child(uname).child('details').child('images').child('profilepic').shallow().get().val()
    for i in prot:
        propic = db.child('Accounts').child(uname).child('details').child('images').child('profilepic').child(i).child(
            'url').get().val()

    name = db.child('Accounts').child(uname).child('details').child('fullname').get().val()

    timestamps = db.child('Accounts').child(uname).child('details').child('images').child(
        'photos').shallow().get().val()
    lis_time = []

    for i in timestamps:
        lis_time.append(i)
    lis_time.sort(reverse=True)
    print(lis_time)

    des = []
    urls = []
    date = []

    for i in lis_time:
        descrip = db.child('Accounts').child(uname).child('details').child('images').child('photos').child(i).child(
            'description').get().val()
        des.append(descrip)

        pic = db.child('Accounts').child(uname).child('details').child('images').child('photos').child(i).child(
            'url').get().val()
        urls.append(pic)

        i = float(i)
        dat = datetime.datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%Y')
        date.append(dat)

    comb_lis = zip(lis_time, date, des, urls)

    alluser = db.child('Accounts').shallow().get().val()
    adp = []
    for l in alluser:

        allprot = db.child('Accounts').child(l).child('details').child('images').child(
            'profilepic').shallow().get().val()

        for x in allprot:
            allpropic = db.child('Accounts').child(l).child('details').child('images').child(
                'profilepic').child(x).child('url').get().val()
        adp.append(allpropic)

    friend = zip(adp, alluser)

    if request.method == 'POST' and 'logout' in request.POST:
        f = open('file.txt', 'r+')
        f.truncate(0)
        redirect("index")

        # -------------------------- search function ---------------------------------------------

    if request.method == 'POST' and 'search' in request.POST:
        print("sadasdasdasd")
        search = request.POST.get('sea')
        print(search)
        request.session['seacrchname'] = search
        print("asdasdasda")
        return redirect('othersprofile')

    # -----------------------------------------------------------------------------------------

    if request.method == 'POST' and 'upload-post' in request.POST:
        import time
        from datetime import datetime, timezone
        import pytz
        tz = pytz.timezone('Asia/Kolkata')
        time_now = datetime.now(timezone.utc).astimezone(tz)
        millis = int(time.mktime(time_now.timetuple()))
        print(" mili " + str(millis))
        description = request.POST.get('description')

        url = request.POST.get('url')
        print(url)
        data = {
            'time': millis,
            'description': description,
            'url': url
        }
        print(url)
        db.child('Accounts').child(uname).child('details').child('images').child('photos').child(millis).set(data)
        return render(request, 'profile.html', {'name': name, 'comb_lis': comb_lis})
    return render(request, 'profile.html', {'name': name, 'comb_lis': comb_lis, 'dp': propic, 'urls': urls, 'friend': friend})


# def news(request, request=None):

def news(request):
    with open("connected.txt", "r") as f:
        username = f.readlines()
    uname = username[-1]

    prot = db.child('Accounts').child(uname).child('details').child('images').child('profilepic').shallow().get().val()

    for i in prot:
        propic = db.child('Accounts').child(uname).child('details').child('images').child('profilepic').child(i).child(
            'url').get().val()

    name = db.child('Accounts').child(uname).child('details').child('fullname').get().val()

    html_text = requests.get('https://www.deccanchronicle.com').text
    html_text2 = requests.get('https://timesofindia.indiatimes.com').text
    html_text3 = requests.get('https://www.deccanchronicle.com').text

    soup = BeautifulSoup(html_text, 'lxml')
    soup2 = BeautifulSoup(html_text2, 'lxml')
    soup3 = BeautifulSoup(html_text3, 'lxml')

    dec = []
    times = []
    for x in soup.find_all('div', class_="col-sm-12 noPadding stry-top-big-a" ):
        dec.append(x.h2.text)
    c = 0
    print('hgcfytdyrtd5tde67ysde65esd65yd6tststers')
    for x in soup2.find_all('a', class_="_3SqZy"):

        times.append(x.figcaption.text)
        c = c + 1
        if c > 4:
            break


    for x in soup.find_all('h3', class_= " home-page-feature-small-1858428" ):
        today = x.a.text
        print(today)
    text = soup.prettify()

    # -------------------------- search function ---------------------------------------------

    if request.method == 'POST' and 'search' in request.POST:
        print("sadasdasdasd")
        search = request.POST.get('sea')
        print(search)
        request.session['seacrchname'] = search
        print("asdasdasda")
        return redirect('othersprofile')

    # -----------------------------------------------------------------------------------------

    return render(request, 'news.html', {'text': text, 'name': name, 'dp': propic, 'dec': dec, 'times': times})


def notification(request):
    import datetime

    with open("connected.txt", "r") as f:
        username = f.readlines()
    uname = username[-1]

    prot = db.child('Accounts').child(uname).child('details').child('images').child('profilepic').shallow().get().val()
    for i in prot:
        propic = db.child('Accounts').child(uname).child('details').child('images').child('profilepic').child(i).child(
            'url').get().val()
    name = db.child('Accounts').child(uname).child('details').child('fullname').get().val()

    names = []

    alluser = db.child('Accounts').shallow().get().val()
    print(alluser)
    des = []
    notify = []
    date = []
    all_lis_time = []
    lis_time = []
    adp = []

    for l in alluser:
        timestamps = db.child('Accounts').child(l).child('details').child('images').child(
            'photos').shallow().get().val()
        photos = True
        try:
            for i in timestamps:
                lis_time.append(i)
                all_lis_time.append(i)

            lis_time.sort(reverse=True)
            all_lis_time.sort(reverse=True)
            print(lis_time)

            print("-----------------------------------")

        except:
            photos = False

    try:

        for j in lis_time:
            for l in alluser:
                timestamps = db.child('Accounts').child(l).child('details').child('images').child(
                    'photos').shallow().get().val()
                photos = True
                lis_time = []
                for i in timestamps:
                    if (i == j):

                        allprot = db.child('Accounts').child(l).child('details').child('images').child(
                            'profilepic').shallow().get().val()
                        for x in allprot:

                            allpropic = db.child('Accounts').child(l).child('details').child('images').child(
                                'profilepic').child(x).child('url').get().val()
                        adp.append(allpropic)

                        allname = db.child('Accounts').child(l).child('details').child('fullname').get().val()
                        names.append(allname)
                        notify.append(allname+" has Updated the connection")
                        descrip = db.child('Accounts').child(l).child('details').child('images').child('photos').child(
                            i).child('description').get().val()
                        des.append(descrip)
                        i = float(i)
                        dat = datetime.datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%Y')
                        date.append(dat)

        print(date)
        print(names)
        print(adp)
        print(notify)
        print(des)

        comb_lis = zip(date, des, names, adp, notify)
    except:
        print("no Photos")
        pass

    return render(request, 'notification.html', {'name': name, 'list': comb_lis, 'dp': propic})


def photo(request):
    with open("connected.txt", "r") as f:
        username = f.readlines()
    uname = username[-1]

    timestamps = db.child('Accounts').child(uname).child('details').child('images').child(
        'photos').shallow().get().val()
    lis_time = []

    for i in timestamps:
        lis_time.append(i)
    lis_time.sort(reverse=True)
    print(lis_time)

    des = []
    urls = []

    for i in lis_time:
        descrip = db.child('Accounts').child(uname).child('details').child('images').child('photos').child(i).child(
            'description').get().val()
        des.append(descrip)

        # -------------------------- search function ---------------------------------------------

        if request.method == 'POST' and 'search' in request.POST:
            print("sadasdasdasd")
            search = request.POST.get('sea')
            print(search)
            request.session['seacrchname'] = search
            print("asdasdasda")
            return redirect('othersprofile')

        # -----------------------------------------------------------------------------------------

        pic = db.child('Accounts').child(uname).child('details').child('images').child('photos').child(i).child(
            'url').get().val()
        urls.append(pic)

    comb_lis = zip(lis_time, des, urls)

    return render(request, 'photo.html', {'comb_lis': comb_lis})


def feedback(request):
    with open("connected.txt", "r") as f:
        username = f.readlines()
    uname = username[-1]

    # -------------------------- search function ---------------------------------------------

    if request.method == 'POST' and 'search' in request.POST:
        print("sadasdasdasd")
        search = request.POST.get('sea')
        print(search)
        request.session['seacrchname'] = search
        print("asdasdasda")
        return redirect('othersprofile')

    # -----------------------------------------------------------------------------------------

    prot = db.child('Accounts').child(uname).child('details').child('images').child('profilepic').shallow().get().val()
    name = db.child('Accounts').child(uname).child('details').child('fullname').get().val()
    for i in prot:
        propic = db.child('Accounts').child(uname).child('details').child('images').child('profilepic').child(i).child(
            'url').get().val()

    return render(request, 'feedback.html', {'name': name, 'dp': propic})


def friends(request):

    with open("connected.txt", "r") as f:
        username = f.readlines()
    uname = username[-1]

    prot = db.child('Accounts').child(uname).child('details').child('images').child('profilepic').shallow().get().val()
    name = db.child('Accounts').child(uname).child('details').child('fullname').get().val()
    for i in prot:
        propic = db.child('Accounts').child(uname).child('details').child('images').child('profilepic').child(i).child(
            'url').get().val()

        # -------------------------- search function ---------------------------------------------

    if request.method == 'POST' and 'search' in request.POST:
        print("sadasdasdasd")
        search = request.POST.get('sea')
        print(search)
        request.session['seacrchname'] = search
        print("asdasdasda")
        return redirect('othersprofile')

    # -----------------------------------------------------------------------------------------

    # ----------------------------- Others Details --------------------------------

    alluser = db.child('Accounts').shallow().get().val()
    print(alluser)
    des = []

    adp = []
    names = []

    for l in alluser:
        allprot = db.child('Accounts').child(l).child('details').child('images').child(
            'profilepic').shallow().get().val()

        for x in allprot:
            allpropic = db.child('Accounts').child(l).child('details').child('images').child(
                'profilepic').child(x).child('url').get().val()
        adp.append(allpropic)

        allname = db.child('Accounts').child(l).child('details').child('fullname').get().val()
        names.append(allname)

    comb_lis = zip(adp, names)
    return render(request, 'friends.html',  {'name': name, 'list': comb_lis, 'dp': propic})



# iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
# iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
#             iiiiiiii
#             iiiiiiii
#             iiiiiiii
#             iiiiiiii
#             iiiiiiii
#             iiiiiiii
#             iiiiiiii
#             iiiiiiii
# iiiiiiiiiiiiiiiiiiii
# iiiiiiiiiiiiiiiiiiii
#
#
# iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
# iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
# iiiiiiii                 iiiiiiii
# iiiiiiii                 iiiiiiii
# iiiiiiii                 iiiiiiii
# iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
# iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
# iiiiiiii                 iiiiiiii
# iiiiiiii                 iiiiiiii
# iiiiiiii                 iiiiiiii
# iiiiiiii                 iiiiiiii
# iiiiiiii                 iiiiiiii
#
# iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
# iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
# iiiiiiii                 iiiiiiii
# iiiiiiii                 iiiiiiii
# iiiiiiii                 iiiiiiii
# iiiiiiii
# iiiiiiii
# iiiiiiii
# iiiiiiii                 iiiiiiii
# iiiiiiii                 iiiiiiii
# iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
# iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
#
#
# iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
# iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
# iiiiiiii                iiiiiiii
# iiiiiiii                iiiiiiii
# iiiiiiii                iiiiiiii
# iiiiiiii                iiiiiiii
# iiiiiiii                iiiiiiii
# iiiiiiii                iiiiiiii
# iiiiiiii                iiiiiiii
# iiiiiiii                iiiiiiii
# iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
# iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
#
#
# iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
# iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
# iiiiiiii                iiiiiiii
# iiiiiiii                iiiiiiii
# iiiiiiii                iiiiiiii
# iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
# iiiiiiiiiiiiiiiiiiiiiiiiiiiiii
# iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
# iiiiiiii                iiiiiiii
# iiiiiiii                iiiiiiii
# iiiiiiii                iiiiiiii
# iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
# iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
#

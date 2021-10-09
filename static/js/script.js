var settingsmenu = document.querySelector(".settings-menu");
var notificationmenu = document.querySelector(".notification-menu");
var darkBtn = document.getElementById("dark-btn");


function settingsMenuToggle(){
    settingsmenu.classList.toggle("settings-menu-height");
}

function notificationMenuToggle(){
    notificationmenu.classList.toggle("notification-menu-height");
}

darkBtn.onclick = function(){
    darkBtn.classList.toggle("dark-btn-on");
    document.body.classList.toggle("dark-theme");

    if(localStorage.getItem("theme") == "light")
    {
        localStorage.setItem("theme","dark");
    }

    else{
        localStorage.setItem("theme","light");
    }
}



if(localStorage.getItem("theme") == "light"){
    darkBtn.classList.remove("dark-btn-on");
    document.body.classList.remove("dark-theme");
}
else if(localStorage.getItem("theme") == "dark"){
    darkBtn.classList.add("dark-btn-on");
    document.body.classList.add("dark-theme");
}
else{
    localStorage.setItem("theme","light");
}












class Feedback {
    constructor() {
        this.formEle = document.getElementById("form");
        this.emailEle = document.getElementById("email");
        this.designationEle = document.getElementById("designation");
        this.nameEle = document.getElementById("name");
        this.feedbackEle = document.getElementById("feedback");
        this.statusEle = document.getElementById("status");
        this.loading = document.getElementById("loading");
    }
    setStatus(content) {
        this.removeLoading();
        this.statusEle.classList.add("statusActive");
        this.statusEle.innerHTML = content;
    }
    removeStatus() {
        this.statusEle.classList.remove("statusActive");
        this.statusEle.innerHTML = ``;
    }
    addLoading() {
        this.loading.classList.add("loadingActive");
    }
    removeLoading() {
        this.loading.classList.remove("loadingActive");
    }
    isEmpty(value) {
        return (value.trim().length == 0) ? true : false;
    }
    invalidLength(value, len) {
        return (value.length > len) ? true : false;
    }
    validateEmail(email) {
        let re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(email);
    }

    initialize() {
        this.formEle.onsubmit = (e) => {
            e.preventDefault();
            this.removeStatus();
            this.addLoading();
            this.validate();
        }
    }

    validate() {
        let email = this.emailEle.value.trim();
        let designation = this.designationEle.value.trim();
        let feedback = this.feedbackEle.value.trim();
        let name = this.nameEle.value.trim();
        let hasErrors = false;
        let errors = `<h>ERROR</h>`;
        if (this.isEmpty(name)) {
            errors = `${errors} <p> Pleae Enter your name</p>`;
            hasErrors = true;
        }
        if (this.invalidLength(name, 59)) {
            errors = `${errors} <p>Name cant exceed 60 characters</p>`;
            hasErrors = true;
        }
        if (!this.validateEmail(email)) {
            errors = `${errors} <p> Is that a valid email ? ? </p>`;
            hasErrors = true;
        }
        if (this.isEmpty(email)) {
            errors = `${errors} <p> Email can not be empty </p>`;
            hasErrors = true;
        }
        if (this.invalidLength(email, 319)) {
            errors = `${errors} <p>Email can not exceed 320 characters</p>`;
            hasErrors = true;
        }

        if (this.isEmpty(designation)) {
            errors = `${errors} <p> Phone Number cant be empty </p>`;
            hasErrors = true;
        }
        if (this.invalidLength(designation, 59)) {
            errors = `${errors} <p>Please fit your designation within 60 characters</p>`;
            hasErrors = true;
        }

        if (this.isEmpty(feedback)) {
            errors = `${errors} <p>Feedback cant be empty</p>`;
            hasErrors = true;
        }
        if (this.invalidLength(feedback, 5999)) {
            errors = `${errors} <p>Thats a long feedback,sorry feedback can not exceed 6000 characters</p>`;
            hasErrors = true;
        }

        if (hasErrors) {
            this.setStatus(errors);
        } else {
            let data = {
                    data: {
                        email: email,
                        designation: designation,
                        name: name,
                        feedback: feedback
                    }
                }
                // this.sendData(JSON.stringify(data));
        }
    }

    sendData(jsonData) {
        const url = "./php/AddFeedback.php";
        let xhttp = new XMLHttpRequest();
        let that = this;
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                if (this.responseText) {
                    that.setStatus("Thank you ! We got your feedback, we look forward to more from you.");
                    that.formEle.reset();
                } else {
                    that.setStatus("Are you sure you entered valid data? Dont worry there might also be problem with our server. Why not give it another shot?");
                }
            }
        };
        xhttp.open("POST", url, true);
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhttp.send(`data=${jsonData}`);
    }

}
const fb = new Feedback();
fb.initialize();











$(function() {
$(".btn").click(function() {
$(".form-signin").toggleClass("form-signin-left");
$(".form-signup").toggleClass("form-signup-left");
$(".frame").toggleClass("frame-long");
$(".signin-active").toggleClass("signin-inactive");
$(".signup-inactive").toggleClass("signup-active");
$(".forgot").toggleClass("forgot-left");
$(this).removeClass("idle").addClass("active");
});
});


$(function() {
    $(".btn").click(function() {
    $(".signup-active").toggleClass("signup-inactive");
    $(".signup-inactive").toggleClass("signup-active");
    });
    });


    $(function() {
        $(".forgot").click(function() {
        $(".btn-animate").toggleClass("btn-animate-grow");
        $(".welcome").toggleClass("welcome-left");
        $(".cover-photo").toggleClass("cover-photo-down");
        $(".frame").toggleClass("frame-short");
        $(".profile-photo").toggleClass("profile-photo-down");
        $(".btn-goback").toggleClass("btn-goback-up");
        $(".forgot").toggleClass("forgot-fade");
        });
        });


        $(function() {
          $(".btn-click").click(function() {

          $(".cover-photo").toggleClass("cover-photo-down");
          $(".frame-long").toggleClass("frame-short");
          $(".forgot").toggleClass("forgot-fade");
          });
          });









$(function() {
$(".btn-signup").click(function() {
$(".nav").toggleClass("nav-up");
$(".form-signup-left").toggleClass("form-signup-down");
$(".success").toggleClass("success-left");
$(".frame").toggleClass("frame-short");
});
});

$(function() {
$(".btn-signin").click(function() {
$(".btn-animate").toggleClass("btn-animate-grow");
$(".welcome").toggleClass("welcome-left");
$(".cover-photo").toggleClass("cover-photo-down");
$(".frame").toggleClass("frame-short");
$(".profile-photo").toggleClass("profile-photo-down");
$(".btn-goback").toggleClass("btn-goback-up");
$(".forgot").toggleClass("forgot-fade");
});
});






function OTPInput() {
    const inputs = document.querySelectorAll('#otp > *[id]');
    for (let i = 0; i < inputs.length; i++) {
      inputs[i].addEventListener('keydown', function(event) {
        if (event.key === "Backspace") {
          inputs[i].value = '';
          if (i !== 0)
            inputs[i - 1].focus();
        } else {
          if (i === inputs.length - 1 && inputs[i].value !== '') {
            return true;
          } else if (event.keyCode > 47 && event.keyCode < 58) {
            inputs[i].value = event.key;
            if (i !== inputs.length - 1)
              inputs[i + 1].focus();
            event.preventDefault();
          } else if (event.keyCode > 64 && event.keyCode < 91) {
            inputs[i].value = String.fromCharCode(event.keyCode);
            if (i !== inputs.length - 1)
              inputs[i + 1].focus();
            event.preventDefault();
          }
        }
      });
    }
  }
  OTPInput();
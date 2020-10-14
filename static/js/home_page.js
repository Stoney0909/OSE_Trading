function popfunction() {
   document.getElementById("profile").style.display = "block";
   document.getElementById("welcome").style.display = "none";
   document.getElementById("change_password").style.display = "none";
}

function displayWelcome()
{
    document.getElementById("profile").style.display = "none";
    document.getElementById("welcome").style.display = "block";
    document.getElementById("change_password").style.display = "none";

}

function  change_password()
{
     document.getElementById("welcome").style.display = "none";
     document.getElementById("profile").style.display = "none";
     document.getElementById("change_password").style.display = "block";
}


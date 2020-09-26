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

function displayEditProfile()
{
    // Left div tag part
    document.getElementById("UserName_Info").style.display = "none";
    document.getElementById("UserName_edit").style.display = "block";
    document.getElementById("FirstName_Info").style.display = "none";
    document.getElementById("FirstName_edit").style.display = "block";
    document.getElementById("Gender_Info").style.display = "none";
    document.getElementById("Gender_edit").style.display = "block";
    document.getElementById("Phone_Info").style.display = "none";
    document.getElementById("Phone_edit").style.display = "block";

    // Right div tag part
    document.getElementById("Email_Info").style.display = "none";
    document.getElementById("Email_edit").style.display = "block";
    document.getElementById("LastName_Info").style.display = "none";
    document.getElementById("LastName_edit").style.display = "block";
    document.getElementById("Age_Info").style.display = "none";
    document.getElementById("Age_edit").style.display = "block";
    document.getElementById("Stock_Label").style.display = "none";
    document.getElementById("Stock_Info").style.display = "none";

     // Button display
    document.getElementById("Saveprofile").style.display = "block";
    document.getElementById("displayEdit_Button").style.display = "none";
}

function saveProfile()
{
    // Left div tag part
    document.getElementById("UserName_Info").style.display = "block";
    document.getElementById("UserName_edit").style.display = "none";
    document.getElementById("FirstName_Info").style.display = "block";
    document.getElementById("FirstName_edit").style.display = "none";
    document.getElementById("Gender_Info").style.display = "block";
    document.getElementById("Gender_edit").style.display = "none";
    document.getElementById("Phone_Info").style.display = "block";
    document.getElementById("Phone_edit").style.display = "none";

    // Right div tag part
    document.getElementById("Email_Info").style.display = "block";
    document.getElementById("Email_edit").style.display = "none";
    document.getElementById("LastName_Info").style.display = "block";
    document.getElementById("LastName_edit").style.display = "none";
    document.getElementById("Age_Info").style.display = "block";
    document.getElementById("Age_edit").style.display = "none";
    document.getElementById("Stock_Label").style.display = "block";
    document.getElementById("Stock_Info").style.display = "block";

    // Button display
     document.getElementById("Saveprofile").style.display = "none";
    document.getElementById("displayEdit_Button").style.display = "block";
}

function  change_password()
{
     document.getElementById("welcome").style.display = "none";
     document.getElementById("profile").style.display = "none";
     document.getElementById("change_password").style.display = "block";
}

 // function showPreviewOne(event)
 // {
 //      if(event.target.files.length > 0){
 //        let src = URL.createObjectURL(event.target.files[0]);
 //        let preview = document.getElementById("Image_Change");
 //        preview.src = src;
 //        preview.style.display = "block";
 //      }
 // }
function ChangeName(name) {
  //alert(name);
  document.getElementById('user_btn').innerHTML = "";
  document.getElementById('user_btn').innerHTML = name;
}

function LoadUsers() {

  uluser = document.getElementById('ul_user');

  $.ajax({
      type: "POST",
      url: "getuser",
      data: {},
      success: function (data) {
          uluser.innerHTML = "";

          $.each(data, function (index) {
              uli = document.createElement("LI");
              var a4 = document.createElement("A");
              a4.setAttribute("href", "javascript:ChangeName('"+data[index].uUsername+"')");
              a4.innerHTML = data[index].uUsername;
              uli.appendChild(a4);
              uluser.appendChild(uli);
          });


      }
  });

}

function CheckAdd(btnval, txtval, tagval) {

  if (btnval == "Select user" || txtval == "") {
    alert("Please fill both the name and text value for assign a task");
  } else {

    $.ajax({
        type: "POST",
        url: "addtask",
        data: {'uVal':btnval, 'uTxt':txtval, 'uTag':tagval},
        success: function (data) {


            $.each(data, function (index) {
                //If ok first clear form
                if (data[index].message == 'OK') {
                  document.getElementById('user_btn').innerHTML = "Select user";
                  document.getElementById('txt_btn').value = "";
                  document.getElementById('txt_btn').setAttribute("placeholder","Type message...");
                } else {
                  alert(data[index].message);
                }

            });


        }
    });
  }

}

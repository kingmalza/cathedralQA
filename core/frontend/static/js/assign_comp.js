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

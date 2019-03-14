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
          divchat = document.getElementById("chat-box");

            $.each(data, function (index) {
                //If ok first clear form
                if (data[index].message == 'OK') {
                  document.getElementById('user_btn').innerHTML = "Select user";
                  document.getElementById('txt_btn').value = "";
                  document.getElementById('txt_btn').setAttribute("placeholder","Type message...");

                  //Now add new data to the existing
                  dch1 = document.createElement("div");
                  dch1.setAttribute("class", "item");
                  dimg1 = document.createElement("img");
                  dimg1.setAttribute("class", "online");
                  dimg1.setAttribute("src", "/static/dist/img/user4-128x128.jpg");
                  dp1 = document.createElement("p");
                  dp1.setAttribute("class", "message");
                  dp1.innerHTML = data[index].anote;
                  dp1_1 = document.createElement("label");
                  dp1_1.setAttribute("class", "name");
                  dp1_1.innerHTML = data[index].uass+" -> "+data[index].ufor;
                  dp1_1_1 = document.createElement("small");
                  dp1_1_1.setAttribute("class", "text-muted pull-right");
                  dp1_1_1.innerHTML = data[index].dop;
                  dp1_1_1_1 = document.createElement("i");
                  dp1_1_1_1.setAttribute("class", "fa fa-clock-o");
                  //No clock icon
                  //dp1_1_1.appendChild(dp1_1_1_1);
                  dp1_1.appendChild(dp1_1_1);

                  dp1.appendChild(dp1_1);

                  dch1.appendChild(dimg1);
                  dch1.appendChild(dp1);
                  divchat.appendChild(dch1);

                } else {
                  alert(data[index].message);
                }

            });


        }
    });
  }

}

function GetElementInsideContainer(containerID, childID) {
    var elm = document.getElementById(childID);
    var parent = elm ? elm.parentNode : {};
    return (parent.id && parent.id === containerID) ? elm : {};
}


function startTab() {

    t_main = document.getElementById("h_tab");
    t_main.innerHTML = "";
    var tr1 = document.createElement("TR");
    var th11 = document.createElement("TH");
    th11.innerHTML = "ID";
    var th12 = document.createElement("TH");
    th12.innerHTML = "Order";
    var th13 = document.createElement("TH");
    th13.innerHTML = "Group";
    var th14 = document.createElement("TH");
    th14.innerHTML = "Description";
    var th15 = document.createElement("TH");
    th15.innerHTML = "Active";
    var th16 = document.createElement("TH");
    th16.innerHTML = "User";
    tr1.appendChild(th11);
    tr1.appendChild(th12);
    tr1.appendChild(th13);
    tr1.appendChild(th14);
    tr1.appendChild(th15);
    tr1.appendChild(th16);
    t_main.appendChild(tr1)


    $.ajax({
        type: "POST",
        url: "groupmain",
        data: {},
        success: function (data) {

            $.each(data, function (index) {

                var tr2 = document.createElement("TR");
                var th21 = document.createElement("TD");
                th21.innerHTML = data[index].t_ID;
                var th22 = document.createElement("TD");
                th22.innerHTML = data[index].t_ord;
                var th23 = document.createElement("TD");
                th23.innerHTML = data[index].t_grp;
                var th24 = document.createElement("TD");
                th24.innerHTML = data[index].t_temp;
                var th25 = document.createElement("TD");
                th25.innerHTML = data[index].t_active;
                var th26 = document.createElement("TD");
                th26.innerHTML = data[index].t_user;
                tr2.appendChild(th21);
                tr2.appendChild(th22);
                tr2.appendChild(th23);
                tr2.appendChild(th24);
                tr2.appendChild(th25);
                tr2.appendChild(th26);
                t_main.appendChild(tr2);
            });

            var rows = t_main.rows; // or table.getElementsByTagName("tr");
            for (var i = 0; i < rows.length; i++) {
                rows[i].onclick = (function () { // closure
                    return function () {
                        ckSub(this.cells[0].innerHTML)
                    }
                })(i);
            }

        }
    });
}

function ckSub(tId) {
    tg = document.getElementById("tab_group");
    tg.innerHTML = ""
    //Create menu
    var tr1 = document.createElement("TR");
    var th11 = document.createElement("TH");
    th11.innerHTML = "ID";
    var th12 = document.createElement("TH");
    th12.innerHTML = "User";
    var th13 = document.createElement("TH");
    th13.innerHTML = "Date";
    var th14 = document.createElement("TH");
    th14.innerHTML = "Status";
    var th15 = document.createElement("TH");
    th15.innerHTML = "Passed";
    var th16 = document.createElement("TH");
    th16.innerHTML = "Failed";

    tr1.appendChild(th11);
    tr1.appendChild(th12);
    tr1.appendChild(th13);
    tr1.appendChild(th14);
    tr1.appendChild(th15);
    tr1.appendChild(th16);

    tg.appendChild(tr1);


    $.ajax({
        type: "POST",
        url: "groupsub",
        data: {tSub: tId},
        success: function (data) {

            $.each(data, function (index) {

                var tr2 = document.createElement("TR");
                var th21 = document.createElement("TD");
                th21.innerHTML = data[index].t_ID;
                var th22 = document.createElement("TD");
                th22.innerHTML = data[index].t_user;
                var th23 = document.createElement("TD");
                th23.innerHTML = data[index].t_data;
                var th24 = document.createElement("TD");
                var th24_span = document.createElement("SPAN");
                th24_span.setAttribute('class', 'label label-warning');
                th24_span.innerHTML = data[index].t_status;
                th24.appendChild(th24_span);
                var th25 = document.createElement("TD");
                var th25_span = document.createElement("SPAN");
                th25_span.setAttribute('class', 'badge bg-green');
                th25_span.innerHTML = data[index].t_pass;
                th25.appendChild(th25_span)
                var th26 = document.createElement("TD");
                var th26_span = document.createElement("SPAN");
                th26_span.setAttribute('class', 'badge bg-red');
                th26_span.innerHTML = data[index].t_fail;
                th26.appendChild(th26_span);

                tr2.appendChild(th21);
                tr2.appendChild(th22);
                tr2.appendChild(th23);
                tr2.appendChild(th24);
                tr2.appendChild(th25);
                tr2.appendChild(th26);

                tg.appendChild(tr2);
            });

        }
    });
}





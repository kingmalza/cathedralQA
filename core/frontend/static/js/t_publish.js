function seltemp() {
    oCtemplates = document.getElementById("t_select");


    $.ajax({
        type: "POST",
        url: "ajax",
        data: {selType: "ST"},
        success: function (data) {
            //oCssSet.style.visibility = visible;

            $.each(data, function (index) {


                var opt = document.createElement("option");
                opt.value = data[index].selID;
                opt.innerHTML = data[index].selDescr;

                oCtemplates.appendChild(opt);

            });

        }
    });
}

function clicktemp(tID) {

    oDetTempl = document.getElementById("t_details");
    //Relative to details area after template selection
    oDetDescr = document.getElementById("det_descr");

    /*
    $.ajax({
        type: "POST",
        url: "ajax",
        data: {selType: "ST"},
        success: function (data) {
            //oDetTempl.style.visibility = visible;

            $.each(data, function (index) {


                var opt = document.createElement("option");
                opt.value = data[index].selID;
                opt.innerHTML = data[index].selDescr;

                oCssSet.appendChild(opt);

            });

        }
    });*/
}

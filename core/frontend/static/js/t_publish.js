function seltemp() {
    oCtemplates = document.getElementById("t_select");


    $.ajax({
        type: "POST",
        url: "test_type",
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
    oDetNotes = document.getElementById("det_notes");
    oDetDt = document.getElementById("det_dt");
    oDetType = document.getElementById("det_type");
    oDetID = document.getElementById("id_test");


    $.ajax({
        type: "POST",
        url: "test_single",
        data: {idTemp: tID},
        success: function (data) {
            oDetTempl.style.visibility = 'visible';

            $.each(data, function (index) {

                oDetDescr.innerHTML = "";
                oDetDescr.innerHTML = data[index].selDescr;
                oDetNotes.innerHTML = "";
                oDetNotes.innerHTML = data[index].OptionNote;
                //oDetDt.innerHTML = "";
                oDetDt.value = data[index].OptionDt;
                oDetType.value = "";
                oDetType.value = data[index].OptionTtype;
                oDetID.value = tID;

            });

        }
    });
}


function isempty() {
    var r_1;
    var r_2;
    var r_3;


    r_1 = document.getElementById("t_select");
    r_2 = document.getElementById("t_descr");
    r_cover = document.getElementById("t_cover");
    r_price = document.getElementById("t_price");
    r_3 = document.getElementById("t_terms");

    if((r_1.value == "Please select...") || (r_2.value == "") || (r_3.checked == false)) {
        alert("Please fill in all the form fields including the terms of use to proceed with the publication");
        return false;
    } else {

        //Start exporting template
        $.ajax({
        type: "POST",
        url: "export_templ",
        data: {idTempl: document.getElementById("id_test").value,
            tDescr: r_2.value,
            tCover: r_cover.value,
            tPrice: r_price.value},
        success: function (data) {
            $.each(data, function (index) {
                    if (data[index].Error){
                        alert(data[index].Error)
                    } else {
                        alert("Template publication Request sent correctly! You will receive a notification regarding it's publication status directly on your email address.")
                    }
                } );

            }
        });
    }

}



function activate() {

    var a_1;

    a_1 = document.getElementById("act_code");


    if(a_1.value == "") {
        alert("Please enter the activation number received by email");
        return false;
    } else {

        //Start exporting template
        $.ajax({
        type: "POST",
        url: "\\act_lic",
        data: {nLic: document.getElementById("act_code").value},
        success: function (data) {
            $.each(data, function (index) {
                    if (data[index].Error){
                        alert(data[index].Error)
                    } else {
                        alert("The activation of your Cathedral took place successfully! Reconnect to the home page to use the application")
                    }
                } );

            }
        });
    }

}
/*
if (!$) {
    // Need this line because Django also provided jQuery and namespaced as django.jQuery
    $ = django.jQuery;
}
try {
    $ = django.jQuery;
}
catch(err) {
  console.log('$ already done -> '+err.message);
}

console.log("Dentro e fuori in admin.js");
$(document).ready(function() {
  console.log("Dentro in admin.js");
    $("select[name='main_id']").change(function() {
        $("select['test_id']").val('');
    });
});*/


(function($) {
    $(document).ready(function() {
        $("select#id_main_id").change(function() {
            console.log($("select#id_key_id").val());
            //$("select#id_test_id").prop('selectedIndex',-1);
            if ($("select#id_test_id").val() && $("select#id_key_id").val() === "") {
                location.reload();
            } else if ($("select#id_test_id").val() && $("select#id_key_id").val()) {
                alert("You cannot change your template ID selection in assist mode; Wait for 60 seconds and then ADD a new Test Case.");
                window.open('/admin/backend/temp_test_keywords/', '_self')
            }

        });
    });
})(django.jQuery);
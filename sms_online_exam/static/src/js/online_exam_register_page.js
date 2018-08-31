function check_string_name(name, error_id, name_id, core) {
    var format = /[~!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/;
    index = 0;
    if (name.length == 0) {
        document.getElementById(error_id).innerHTML = core._t('* Must be required !');
        document.getElementById(name_id).value = '';
        index += 1
    } else if (format.test(name) == true) {
        document.getElementById(error_id).innerHTML = core._t('* May not contain any special characters !');
        document.getElementById(name_id).value = name;
        index += 1;
    } else {
        document.getElementById(error_id).innerHTML = '';
        document.getElementById(name_id).value = name;
    }
    return index
}

function check_id(str_id, error_id, core) {
    index = 0;
    if (parseInt(str_id) > 0) {
        document.getElementById(error_id).innerHTML = '';
    } else {
        document.getElementById(error_id).innerHTML = core._t('* Please select a option !');
        index += 1
    }
    return index
}

function check_validate() {
    var last_name = document.getElementById("lastName").value.trim().replace(/  +/g, ' ');
    var middle_name = document.getElementById("middleName").value.trim().replace(/  +/g, ' ');
    var first_name = document.getElementById("firstName").value.trim().replace(/  +/g, ' ');
    var birthday = document.getElementById("birthday").value;
    var identity_card = document.getElementById("identityCard").value;
    var exam = document.getElementById("examList").value;
    var unit = document.getElementById("unitList").value;
    var position = document.getElementById("positionList").value;
    var i = 0;

    odoo.define('sms_online_exam.online_exam_register_page', function(require) {
        "use strict";
        var core = require('web.core');
        i += check_string_name(last_name, 'errorLastName', 'lastName', core);
        i += check_string_name(first_name, 'errorFirstName', 'firstName', core);
        if (middle_name) {
            i += check_string_name(middle_name, 'errorMiddleName', 'middleName', core);
        }
        if (!birthday) {
            i += 1;
            document.getElementById('errorBirthday').innerHTML = core._t('* Must be required !');
        }
        i += check_string_name(identity_card, 'errorIdentityCard', 'identityCard', core);
        i += check_id(exam, 'errorExamList', core);
        i += check_id(unit, 'errorUnitList', core);
        i += check_id(position, 'errorPositionList', core);
    });
    if (i > 0) {
        return false;
    } else {
        return true;
    }
}
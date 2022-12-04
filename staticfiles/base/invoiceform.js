function updateElementIndex(el, prefix, ndx) {
    var id_regex = new RegExp('(' + prefix + '-\\d+)');
    var replacement = prefix + '-' + ndx;
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
}
function cloneMore(selector, prefix) {
    var newElement = $(selector).clone(true);
    var total = $('#id_' + prefix + '-TOTAL_FORMS').val();
    newElement.find(':input:not([type=button]):not([type=submit]):not([type=reset])').each(function() {
        var name = $(this).attr('name').replace('-' + (total-1) + '-', '-' + total + '-');
        var id = 'id_' + name;
        $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
    });
    newElement.find('label').each(function() {
        var forValue = $(this).attr('for');
        if (forValue) {
          forValue = forValue.replace('-' + (total-1) + '-', '-' + total + '-');
          $(this).attr({'for': forValue});
        }
    });
    
    total++;
    $('#id_' + prefix + '-TOTAL_FORMS').val(total);
    $(selector).after(newElement);
    var conditionRow = $('.form-row:last');
    conditionRow.find('.btn.add-form-row')
    .removeClass('btn-outline-info').addClass('btn btn-danger')
    .removeClass('add-form-row').addClass('remove-form-row')
    .removeAttr('style')
    .html('<span class="glyphicon glyphicon-minus" aria-hidden="true">Remove Item</span>')
    conditionRow.find('.item-counter')
    .html(total)

    return false;
}
function deleteForm(prefix, btn) {
    var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    if (total > 1){
        btn.closest('.form-row').remove();
        var forms = $('.form-row');
        $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
        for (var i=0, formCount=forms.length; i<formCount; i++) {
            $(forms.get(i)).find(':input').each(function() {
                updateElementIndex(this, prefix, i);
            });
        }
    }
    return false;
}
function copyaddress(IsChecked){
    var address = document.getElementById('id_b_address').value
    var shipping_addr = document.getElementById('id_s_address')

    if(address.trim().length==0){
        alert("Enter the Billing Address first");
        document.getElementById("id_addr_chk_box").checked = false;
    }
    else{
        if(IsChecked==true){
            shipping_addr.value = address
             shipping_addr.setAttribute('readonly','')
        }
         else{
             shipping_addr.removeAttribute('readonly','')
         }
    }
}

const max_form_count = 10
let form_count = 1
$(document).on('click', '.add-form-row', function(e){
    e.preventDefault();
    if(form_count < max_form_count){
    cloneMore('.form-row:last', 'form');
    form_count++
    return false;
    }
    else{
        alert("Sorry! only 10 items can be inserted at a time");
    }
});
$(document).on('click', '.remove-form-row', function(e){
    e.preventDefault();
    deleteForm('form', $(this));
    form_count--
    return false;
});
$(document).on('click','#id_addr_chk_box', function(e){
    var IsChecked = $('input[name="addr_chk_box"]:checked').length > 0;
    copyaddress(IsChecked);
})
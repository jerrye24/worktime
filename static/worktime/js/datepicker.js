$("#id_period").datepicker({
            dateFormat: 'ddmmyy',
            firstDay: 1,
            dayNamesMin: [ 'Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб'],
            monthNames: ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'],
            onSelect: function( selectedDate ) {
                if(!$(this).data().datepicker.first){
                    $(this).data().datepicker.inline = true;
                    $(this).data().datepicker.first = selectedDate;
                }else{
                    if(selectedDate > $(this).data().datepicker.first){
                        $(this).val($(this).data().datepicker.first+"-"+selectedDate);
                    }else{
                        $(this).val(selectedDate+"-"+$(this).data().datepicker.first);
                    }
                    $(this).data().datepicker.inline = false;
                }
            },
            onClose:function(){
                delete $(this).data().datepicker.first;
                $(this).data().datepicker.inline = false;
            }
        });

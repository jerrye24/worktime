function Clock() {
    var date = new Date();
    var hours = date.getHours();
    var minutes = date.getMinutes();
    var seconds = date.getSeconds();
    if (hours < 10) hours = '0' + hours;
    if (minutes < 10) minutes = '0' + minutes;
    if (seconds < 10) seconds = '0' + seconds;
    document.getElementById('clock').innerHTML = hours + ':' + minutes + ':' + seconds;
}
window.onload = function () {
    setInterval(Clock, 1000);
}

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


$(document).ready(function(){
        var a = window.location.pathname;
        var b = a.slice(a.length-9);
	$('#data_table').Tabledit({
		deleteButton: false,
		editButton: false,   		
		columns: {
		  identifier: [0, 'date'],                    
		  editable: [[36, 'power_calc'],[37,'power_real'],[39,'power_correct']]
		},
		hideIdentifier: false,
		url: 'live_edit.php?id='+b		
	});

 
});



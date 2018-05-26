$(document).ready(function () {
	var table = $('#table').DataTable({
		"searching": true,
		"bFilter": true,
		"bPaginate": true,
		"ordering": true,
		"Info": true,
		"autoWidth": false,
		"asStripeClasses": [],
		"order": [
			[0, null]
		],
		"pageLength": 3,
		"columnDefs": [
			{
				orderable: false,
				targets: 0
			},
			{
				orderable: false,
				targets: 1
			},
			{
				orderable: false,
				targets: 2
			}
		],
		initComplete: function(){
			var api = this.api();
			api.columns().indexes().flatten().each(function (i) {
				if (i > 3) { // delete the filter box in the first and second column
					var column = api.column(i);
					var $span = $('<span class="addselect">▾</span>').appendTo($(column.header()))

					var select = $('<select><option value="">All</option></select>')
						.appendTo($(column.header()))
						.on('change', function (evt) {
							evt.stopPropagation();
							var val = $.fn.dataTable.util.escapeRegex($(this).val());
							column.search(val ? '^' + val + '$' : '', true, false).draw();
						});

					column.data().unique().sort().each(function (d, j) {
						d = d.replace(/<[^>]+>/g, ""); // remove the html tag
						select.append('<option value="' + d + '">' + d + '</option>');
						$span.append(select);
					});
				}
			});
		}
	});
	table.on('order.dt search.dt',
		function() {
			table.column(0, {
				"search": 'applied',
				"order": 'applied'
			}).nodes().each(function(cell, i) {
				cell.innerHTML = i + 1;
			});
	}).draw();

});

//checkbox select all
$("#checkAll").on("click", function () {
	console.log("checkall...")
	if ($(this).prop("checked") === true) {
		$("input[name='checkList']").prop("checked", $(this).prop("checked"));
		$('#table tbody tr').addClass('selected');
	} else {
		$("input[name='checkList']").prop("checked", false);
		$('#table tbody tr').removeClass('selected');
	}
});

$("input[name='checkList']").on("click", function () {
	console.log("checkList...")
	id = $(this).attr('id').substring(5)
	if ($(this).prop("checked") === true) {
		$('#tr' + id).addClass('selected');
	} else {
		$('#tr' + id).removeClass('selected');
	}
});
 
$("#download").on("click", function () {
	$("#download-instruction-block").css("display", "unset");
	var urls = $(".selected td[class='url'] a");
	if(urls.length == 0){
		$("#downloadUrl").text("");
	}else{
		$("#downloadUrl").text("");
		for(var i = 0; i < urls.length; i++){
			var tmp = $("#downloadUrl").text();
			$("#downloadUrl").text(tmp + urls[i] + " ");
		}
	}
	$("#downloadUrl").focus();
})

function copyinput(){
	var input = $("#downloadUrl");
	input.select();
	document.execCommand("Copy");
}




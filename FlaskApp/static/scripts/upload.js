function agree() {

	if(valid() == false) {
		alert("Please complete the table below.")
		document.getElementById('file-btn').disabled = 'disabled';
		document.getElementById('confirm').checked = false;
	}
	else if(document.getElementById('confirm').checked) {
		document.getElementById('file-btn').disabled = false;
	}
	else {
		document.getElementById('file-btn').disabled = 'disabled';
	}
}

function validate_required(field, alerttxt) {
	with (field) {
		if (value == null || value == "") {
			alert(alerttxt);
			return false
		}
		else {return true}
	}
}

function valid() {
	console.log("!")
	console.log($("input[name=Tissue]").val())
	if ($("input[name=Tissue]").val() == "") {
		$("input[name=Tissue]").focus();
		return false
	}
	if ($("input[name=date]").val() == "") {
		$("input[name=date]").focus();
		return false
	}
	if ($("input[name=magnification]").val() == "") {
		$("input[name=magnification]").focus();
		return false
	}
	if ($("input[name=Artifacts]").val() == "") {
		$("input[name=Artifacts]").focus();
		return false
	}
	if ($("input[name=Stain]").val() == "") {
		$("input[name=Stain]").focus();
		return false
	}
	if ($("input[name=Comments]").val() == "") {
		$("input[name=Comments]").focus();
		return false
	}
	if ($("input[name=Scanner]").val() == "") {
		$("input[name=Scanner]").focus();
		return false
	}
	if ($("input[name=Preparation]").val() == "") {
		$("input[name=Preparation]").focus();
		return false
	}
	if ($("input[name=Specimen]").val() == "") {
		$("input[name=Specimen]").focus();
		return false
	}
	if ($("input[name=Email]").val() == "") {
		$("input[name=Email]").focus();
		return false
	}
}

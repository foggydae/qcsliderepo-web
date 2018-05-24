function agree() {
	if(document.getElementById('confirm').checked)
		document.getElementById('submit').disabled = false;
	else
		document.getElementById('submit').disabled = 'disabled';
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

function valid(thisform) {
	with (thisform) {
		if (validate_required(Tissue,"Tissue must be filled out!") == false) {
			Tissue.focus();
			return false
		}
		if (validate_required(date,"Date must be filled out!") == false) {
			date.focus();
			return false
		}
		if (validate_required(magnification,"Magnification must be filled out!") == false) {
			magnification.focus();
			return false
		}
		if (validate_required(Artifacts,"Artifacts must be filled out!") == false) {
			Artifacts.focus();
			return false
		}
		if (validate_required(Stain,"Stain must be filled out!") == false) {
			Stain.focus();
			return false
		}
		if (validate_required(Comments,"Comments must be filled out!") == false) {
			Comments.focus();
			return false
		}
		if (validate_required(Scanner,"Scanner must be filled out!") == false) {
			Scanner.focus();
			return false
		}
		if (validate_required(Preparation,"Preparation must be filled out!") == false) {
			Preparation.focus();
			return false
		}
		if (validate_required(Specimen,"Specimen must be filled out!") == false) {
			Specimen.focus();
			return false
		}
		if (validate_required(Email,"Email must be filled out!") == false) {
			Email.focus();
			return false
		}
	}
}

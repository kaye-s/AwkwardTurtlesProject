const phoneInput1 = document.getElementById('phone_number');
const phoneInput2 = document.getElementById('edit_phone_number');

try{
  phoneInput1.addEventListener('input', validated_phone);
  phoneInput2.addEventListener('input', validated_phone);
} catch(e){
  console.log(e)
}


function initializeAutocomplete (){
    const address1Input = document.getElementById("address1");
    const editAddress1Input = document.getElementById("edit_address1");
    
  
    const autocomplete = new google.maps.places.Autocomplete(address1Input, {
      componentRestrictions: { country: "us" }, 
    });

    const editAutoComplete =  new google.maps.places.Autocomplete(editAddress1Input, {
      componentRestrictions: { country: "us" }, 
    });


    autocomplete.addListener("place_changed", () => {
      const place = autocomplete.getPlace();

      if (!place.geometry) {
        console.log("No details available for the input: '" + place.name + "'");
        return;
      }

      console.log("Selected place:", place);
    });

    editAutoComplete.addListener("place_changed", () => {
      const place = autocomplete.getPlace();

      if (!place.geometry) {
        console.log("No details available for the input: '" + place.name + "'");
        return;
      }

      console.log("Selected place:", place);
    });
}

function validated_phone(e){
  let input = e.target.value;
  console.log("phone_input_debug");

  input = input.replace(/\D/g, '');

  if (input.length > 3 && input.length <= 6) {
      input = `${input.slice(0, 3)}-${input.slice(3)}`;
  } else if (input.length > 6) {
      input = `${input.slice(0, 3)}-${input.slice(3, 6)}-${input.slice(6, 10)}`;
  }
  e.target.value = input;
}


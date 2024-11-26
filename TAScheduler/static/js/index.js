document.getElementById("logout_btn").addEventListener("click", () => {
    document.getElementById("logout_form").submit();
})

const modal = document.getElementById("modal-box-container");
const open_btn =   document.getElementById("add-modal");
const exit_btn = document.getElementById("remove-modal");

open_btn.addEventListener("click", (e) => {
    modal.style.display = "block";
})

exit_btn.addEventListener("click", (e) => {
    modal.style.display = "none";
    console.log("yesss");
})

function initializeAutocomplete() {
    const address1Input = document.getElementById("address1");
    
  
    const autocomplete = new google.maps.places.Autocomplete(address1Input, {
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
  }

  const phoneInput = document.getElementById('phone_number');

phoneInput.addEventListener('input', (e) => {
    let input = e.target.value;
    console.log("hey")

    input = input.replace(/\D/g, '');

    if (input.length > 3 && input.length <= 6) {
        input = `${input.slice(0, 3)}-${input.slice(3)}`;
    } else if (input.length > 6) {
        input = `${input.slice(0, 3)}-${input.slice(3, 6)}-${input.slice(6, 10)}`;
    }
    e.target.value = input;
});

document.getElementById("delete_user_btn").addEventListener("click", () => {
    document.getElementById("delete_from").submit();
})

console.log('new world')
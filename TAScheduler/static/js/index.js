console.log("hoyyyy");


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

document.getElementById("logout_btn").addEventListener("click", () => {
    console.log("hey");
    document.getElementById("logout_form").submit();
})


document.getElementById("logout_btn").addEventListener("click", () => {
    document.getElementById("logout_form").submit();
});

//CREATE USER MODAL OPENING FUNCTIIONALITY
const addModal = document.getElementById("modal-box-container");
const open_btn =   document.getElementById("add-modal");
const exit_btn = document.getElementById("remove-modal");

open_btn.addEventListener("click", (e) => {
    addModal.style.display = "block";
})

exit_btn.addEventListener("click", (e) => {
    addModal.style.display = "none";
})

//EDIT USER MODAL OPENING FUNCTIIONALITY
const editModal = document.getElementById("modal-box-container1");
const exit_btn1 = document.getElementById("remove-modal1");

const fnameInput = document.getElementById("edit_fname")
const lnameInput = document.getElementById("edit_lname")
const emailInput = document.getElementById("edit_email")
const phone_numberInput = document.getElementById("edit_phone_number")
const address1Input = document.getElementById("edit_address1")
const address2Input = document.getElementById("edit_address2")
const roleInput = document.getElementById("edit_role")
const deptInput = document.getElementById("edit_dept")
const userIdInput = document.getElementById("custom_id_edit")
const oldRole = document.getElementById("old_role_data")

exit_btn1.addEventListener("click", (e) => {
    editModal.style.display = "none";
})

const editUser = (role, id, fname, lname, email, phone, address, dept) => {
    editModal.style.display = "block";
    const addrList = address.split("<TASCheduler_delimiter>") 

    fnameInput.value= fname;
    lnameInput.value= lname;
    emailInput.value= email;
    phone_numberInput.value= phone;
    address1Input.value= addrList[0] || '';
    address2Input.value= addrList[1] || '';
    roleInput.value= role;
    deptInput.value= dept;
    userIdInput.value = id;
    oldRole.value = role;
}

//Navbar Hovering
const default_nav_btn = document.querySelector(".btn-grad4")
const nav_btn = document.querySelectorAll(".nav-btn");

nav_btn.forEach(nav => {
    
    nav.addEventListener("mouseover", () => {
        const btn = document.querySelector(".btn-grad4")
        btn.classList.remove("btn-grad4");
        nav.classList.add("btn-grad4");
    })

    nav.addEventListener("mouseout", () =>{
        if(nav !== default_nav_btn && !default_nav_btn.classList.contains("btn-grad4")){
            nav.classList.remove("btn-grad4");
            default_nav_btn.classList.add("btn-grad4");
        }

    })
})

//DELETION CONFIRMATION MODAL
// Get modal elements
const modal = document.getElementById("deleteModal");
const deleteForms = document.querySelectorAll(".delete-confirm");
const cancelDelete = document.getElementById("cancelDelete");
const confirmDelete = document.getElementById("confirmDelete");

let current;
// Open modal
deleteForms.forEach((form, i) => {
    form.addEventListener("click", (e) => {
        e.preventDefault(); // Prevent default form submission
        current = i;
        modal.style.display = "block"; // Show the modal
    });
});

// Close modal when "Cancel" is clicked
cancelDelete.addEventListener("click", () => {
    modal.style.display = "none";
});

// Add confirmation functionality
confirmDelete.addEventListener("click", () => {
    modal.style.display = "none";
    if(current != null){
        deleteForms[current].closest('form').submit()
    }
});
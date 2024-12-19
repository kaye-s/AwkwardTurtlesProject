//FORM INPUT IN ACCOUNTS
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

//SEARCH BAR IN ACCOUNTS
const search_bar = document.querySelectorAll(".search-bar-input");

//3 TRANSPARENT ROLE GROUP CONTAINERS IN ACCOUNTS
const rg = document.querySelectorAll(".role-group");

//EMPTY SEARCH
const search_err_msg = document.querySelectorAll(".search-err");

const courses_card = document.querySelectorAll(".custom-card");
//CREATE USER MODAL OPENING FUNCTIIONALITY

const addModal = document.getElementById("modal-box-container");
const open_btn =   document.getElementById("add-modal");
const exit_btn = document.getElementById("remove-modal");

//EDIT USER MODAL OPENING FUNCTIIONALITY
const editModal = document.getElementById("modal-box-container1");
const exit_btn1 = document.getElementById("remove-modal1");

//DELETION CONFIRMATION MODAL
// Get modal elements
const modal = document.getElementById("deleteModal");
const deleteForms = document.querySelectorAll(".delete-confirm");
const cancelDelete = document.getElementById("cancelDelete");
const confirmDelete = document.getElementById("confirmDelete");

const mol = document.querySelector(".special-side-content");
const tooltip =  document.querySelector(".tooltip-aside");

document.getElementById("logout_btn").addEventListener("click", () => {
    document.getElementById("logout_form").submit();
});

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


if(open_btn){
    open_btn.addEventListener("click", (e) => {
        addModal.style.display = "block";
    })
}

if(exit_btn){
    exit_btn.addEventListener("click", (e) => {
        addModal.style.display = "none";
    })
}

if(exit_btn1){
    exit_btn1.addEventListener("click", (e) => {
        editModal.style.display = "none";
    })
}

// Open modal
let current;
if(deleteForms){
    deleteForms.forEach((form, i) => {
        form.addEventListener("click", (e) => {
            e.preventDefault(); // Prevent default form submission
            current = i;
            modal.style.display = "block"; // Show the modal
        });
    });
}

// Close modal when "Cancel" is clicked
if(cancelDelete){
    cancelDelete.addEventListener("click", () => {
        modal.style.display = "none";
    });
}

// Add confirmation functionality
if(confirmDelete){
    confirmDelete.addEventListener("click", () => {
        modal.style.display = "none";
        if(current != null){
            deleteForms[current].closest('form').submit()
        }
    });
}

//Search bar functionality
if(search_bar){
    search_bar.forEach((s, i) => {
        s.addEventListener("keydown", (e) => {
            role_grouping = rg[i];
            msg = search_err_msg[i];
            setTimeout(() => {
                role_grouping.childNodes.forEach(c => {
                    if(c.nodeName !== "#text"){
                        str = c.innerText.toLowerCase();
                        if(!str.match(s.value.toLowerCase().trimEnd("").trimStart(""))) c.style.display = "none"; //Main search done here := filters based on text string in the user card...email, first+last name and department
                        else c.style.display = "block";
                    }
                })
                //Empty search display error
                if(role_grouping.clientHeight === 0) msg.style.display = "block";
                else msg.style.display = "none";
            }, 200)
        })
    }) 
}

let courseIds = [];

if(courses_card){
    courses_card.forEach((course_card, i) => {
        courseIds[i] = course_card.querySelector(".deleteFormCourse").value;
        course_card.addEventListener("click", (e) => {
            document.getElementById("ol-sections").classList.remove("d-none"); 
            document.getElementById("sec-message").style.display = "none"; 
            document.getElementById("sections-content").childNodes.forEach(c => {

                if(c.style && c.querySelector(".course_class_for_section").value == courseIds[i]){
                    c.style.display = "block";
                } else if (c.style){
                    c.style.display = "none";
                }
            })
            document.getElementById("sectionsCourseId").value = courseIds[i];
            
            // setTimeout(() => {
            //     document.getElementById("ol-sections").classList.add("d-none"); 
            //     document.getElementById("sec-message").style.display = "block"; 
            // }, 2000)
        })
    })
}
const ta_group = rg[2];
const c = document.querySelector(".custom-container");
if(ta_group){
    ta_group.addEventListener("mouseenter", () => {
        const h = c.scrollHeight;
        setTimeout(() => {
            c.scrollBy({
                top:c.scrollHeight - h,
                behavior:"smooth"
            })
        }, 200)
    })
}


const openModal = (courseId = "", courseName = "", courseIdentifier = "", courseDept = "", courseCredits = "") => {
    document.getElementById("modalTitle").textContent = courseId ? "Edit Course" : "Create New Course";
    document.getElementById("courseFormAction").value = courseId  ? "editCourse" : "createCourse";
    document.getElementById("courseIdField").value = courseId;
    document.getElementById("courseNameField").value = courseName;
    document.getElementById("courseIdentifierField").value = courseIdentifier;
    document.getElementById("courseDeptField").value = courseDept;
    document.getElementById("courseCreditsField").value = courseCredits;
    document.getElementById("courseModal").style.display = "block";
  }

const closeModal = () => {
    document.getElementById("courseModal").style.display = "none";
}
nav_items = document.querySelectorAll(".aside-nav-list-item");
as0 = document.getElementById("aside-0");
as1 = document.getElementById("aside-1");
as2 = document.getElementById("aside-2");

nav_items.forEach((nav, i) => {
    nav.addEventListener("click", () => {
        tooltip.style.display = "none";
        document.getElementById("btn_side_nav").style.display = "block";
        mol.style.height = "100%";
        nav_items.forEach(item => item.classList.remove("active"));
        nav.classList.add("active");
        console.log(i);
        switch (i) {
            case 0:
                as0.style.display = "flex";
                as1.style.display = "none";
                as2.style.display = "none";
                break;
            case 1:
                as1.style.display = "flex";
                as0.style.display = "none";
                as2.style.display = "none";
                break;
            case 2:
                as2.style.display = "flex";
                as0.style.display = "none";
                as1.style.display = "none";
                break;
            default:
                break;
        }
    })

})

const remove_mol = () => {
    tooltip.style.display = "none";
    document.getElementById("btn_side_nav").style.display = "none";
    mol.style.height = "max-content";
    nav_items.forEach(item => item.classList.remove("active"));
    as0.style.display = "none";
    as1.style.display = "none";
    as2.style.display = "none";
}

const openSectionModal = (sectionId = "", sectionType = "", sectionNum = "", courseName = "", sectionDays = "", sectionStartTime = "", sectionEndTime = "", taId = "", instructorId = "") => {
    document.getElementById("modalTitle").textContent = sectionId ? "Edit Section" : "Create Section";
    document.getElementById("sectionIdField").value = sectionId;
    document.getElementById("sectionTypeField").value = sectionType;
    document.getElementById("sectionNumField").value = sectionNum;
    document.getElementById("sectionDaysField").value = sectionDays;
    document.getElementById("sectionStartTimeField").value = sectionStartTime;
    document.getElementById("sectionEndTimeField").value = sectionEndTime;
    document.getElementById("instructorIdField").value = instructorId;
    document.getElementById("sectionModal").style.display = "block";
  }
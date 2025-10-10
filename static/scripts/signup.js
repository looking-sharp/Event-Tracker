'use strict';


const usernameInput = document.getElementById("username");
const cPasswordInput = document.getElementById("c_password");
const passwordInput = document.getElementById("password");
const statusSpan = document.getElementById("username-status");
const passwordSpan = document.getElementById("password-status");
let typingTimer; // used for debounce
const debounceDelay = 300; // milliseconds

usernameInput.addEventListener("input", () => {
    clearTimeout(typingTimer);
    typingTimer = setTimeout(checkUsername, debounceDelay);
});

cPasswordInput.addEventListener("input", () => {
    clearTimeout(typingTimer);
    typingTimer = setTimeout(checkPassword, debounceDelay);
});

function checkUsername() {
  const username = usernameInput.value.trim();

  if (username == null || username.length == 0) {
    statusSpan.textContent = "";
    return;
  }
  
  fetch(`/check_username?username=${encodeURIComponent(username)}`)
    .then(response => response.json())
    .then(data => {
      if (data.exists) {
        statusSpan.textContent = "Username already taken";
        statusSpan.style.color = "red";
      } else {
        statusSpan.textContent = "Username available";
        statusSpan.style.color = "green";
      }
    })
    .catch(err => {
      console.error("Error checking username:", err);
      statusSpan.textContent = "Error checking username";
      statusSpan.style.color = "orange";
    });
}

function checkPassword() {
    const password = passwordInput.value.trim();
    const c_password= cPasswordInput.value.trim();
    if((password == null || password == "") || (c_password == null || c_password == "")) {
        passwordSpan.textContent= "";
        return;
    }

    if(password != c_password) {
        passwordSpan.innerHTML = "Passwords must match<br>"
        passwordSpan.style.color = "red";
    }
    else if(password == c_password) {
        passwordSpan.innerHTML = "Passwords matching<br>"
        passwordSpan.style.color = "green";
    }
}
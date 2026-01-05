function register() {
  const name = regName.value;
  const email = regEmail.value;
  const password = regPassword.value;

  if (!name || !email || !password) {
    alert("All fields required");
    return;
  }

  let users = JSON.parse(localStorage.getItem("users")) || [];

  if (users.find(u => u.email === email)) {
    alert("User already exists");
    return;
  }

  users.push({ name, email, password });
  localStorage.setItem("users", JSON.stringify(users));

  alert("Registration successful");
  window.location.href = "/login";
}

function login() {
  const email = loginEmail.value;
  const password = loginPassword.value;

  let users = JSON.parse(localStorage.getItem("users")) || [];
  let user = users.find(u => u.email === email && u.password === password);

  if (!user) {
    alert("Invalid login");
    return;
  }

  localStorage.setItem("loggedInUser", JSON.stringify(user));

  // ✅ LOGIN SUCCESS → HOME
  window.location.href = "/home";
}

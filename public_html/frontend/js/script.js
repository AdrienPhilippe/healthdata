function checklogin() {
    const user = sessionStorage.getItem("user");
    const password = sessionStorage.getItem("password");
    if (!user || !password){
      alert("You need to log in.")
      document.location.href = "login.html";
    }
    else{
      alert("Log")
      return 1;
    }
  };
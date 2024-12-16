// scripts.js
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("registration-form");

  form.addEventListener("submit", (event) => {
    event.preventDefault();

    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    const criteria = {
      length: password.length >= 8,
      numbers: (password.match(/\d/g) || []).length >= 2,
      special: /[!@#$%^&*(),.?":{}|<>]/.test(password),
      uppercase: /[A-Z]/.test(password),
      lowercase: /[a-z]/.test(password),
    };

    
    Object.keys(criteria).forEach((key) => {
      document.getElementById(key).style.color = criteria[key] ? 'green' : 'red';
    });

    if (password === confirmPassword && Object.values(criteria).every((value) => value)) {
      const formData = new FormData(form);

      fetch("/cadastro-cliente", {
        method: "POST",
        body: formData,
      })
        .then((response) => {
          if (response.ok) {
            window.location.href = "/login"; 
          } else {
            alert("Erro no cadastro. Verifique os dados e tente novamente.");
          }
        })
        .catch((error) => {
          console.error("Erro:", error);
          alert("Houve um erro ao processar o cadastro.");
        });
    } else {
      alert('Por favor, corrija os erros antes de continuar.');
    }
  });
});

  

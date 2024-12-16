  
function navigateTo(page) {
    const welcomeContainer = document.querySelector('.welcome-container');
    const loginContainer = document.querySelector('.login-container');
    
    if (page === 'login') {
      window.location.href = `/login`;
    } else if (page === 'cadastro-escolha') {
      window.location.href = '/cadastro-escolha'; // Redireciona para a página de cadastro
    } else if (page === 'cadastro-profissional') {
      window.location.href = '/cadastro-profissional'; // Redireciona para a página de cadastro
    } else if (page === 'cadastro-cliente') {
      window.location.href = '/cadastro-cliente'; // Redireciona para a página de cadastro
    }
  }
  
  function togglePassword() {
    const passwordInput = document.getElementById('password');
    const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordInput.setAttribute('type', type);
  }
  
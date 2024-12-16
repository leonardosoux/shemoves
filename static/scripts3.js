document.addEventListener("DOMContentLoaded", () => {
    // Gerenciar curtidas
    const likeButtons = document.querySelectorAll(".like-button");
    likeButtons.forEach((button) => {
      button.addEventListener("click", () => {
        const postId = button.getAttribute("data-post-id");
  
        fetch(`/like/${postId}`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.likes !== undefined) {
              const likesCount = document.getElementById(`likes-count-${postId}`);
              likesCount.textContent = `Likes: ${data.likes}`;
            } else {
              alert("Erro ao curtir a publicação.");
            }
          })
          .catch((error) => {
            console.error("Erro ao curtir:", error);
            alert("Houve um erro ao curtir a publicação.");
          });
      });
    });
  
    // Mostrar formulário de comentário
    const toggleCommentButtons = document.querySelectorAll(".toggle-comment-form");
    toggleCommentButtons.forEach((button) => {
      button.addEventListener("click", () => {
        const postId = button.getAttribute("data-post-id");
        const commentForm = document.getElementById(`comment-form-${postId}`);
        commentForm.style.display =
          commentForm.style.display === "none" || commentForm.style.display === "" ? "block" : "none";
      });
    });
  
    // Gerenciar envio de comentários
    const commentForms = document.querySelectorAll(".comment-form");
    commentForms.forEach((form) => {
      form.addEventListener("submit", (event) => {
        event.preventDefault();
  
        const postId = form.getAttribute("data-post-id");
        const formData = new FormData(form);
  
        fetch(`/comment/${postId}`, {
          method: "POST",
          body: formData,
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.comment) {
              const commentsSection = document.getElementById(`comments-${postId}`);
              const newComment = document.createElement("div");
              newComment.className = "comment";
              newComment.innerHTML = `<strong>${data.comment.user}:</strong> ${data.comment.content}`;
              commentsSection.appendChild(newComment);
  
              form.reset();
            } else {
              alert("Erro ao enviar o comentário.");
            }
          })
          .catch((error) => {
            console.error("Erro ao comentar:", error);
            alert("Houve um erro ao enviar o comentário.");
          });
      });
    });
  });
  
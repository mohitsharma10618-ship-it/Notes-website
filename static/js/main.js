document.addEventListener('DOMContentLoaded', () => {
  const burger = document.getElementById('burger');
  const links = document.getElementById('nav-links');
  if (burger) {
    burger.addEventListener('click', () => {
      links.classList.toggle('open');
    });
  }
});
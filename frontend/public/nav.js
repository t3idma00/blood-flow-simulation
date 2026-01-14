// public/nav.js

document.addEventListener("DOMContentLoaded", () => {
  const navHTML = `
    <nav class="navbar">
      <a href="/index.html" class="nav-logo">Blood Flow Simulation</a>
      <div class="nav-links">
        <a href="/simulations/sim3.html">Simulation 1</a>
        <a href="/simulations/sim1.html">Simulation 2</a>
        <a href="/simulations/sim2.html">Simulation 3</a>
        <a href="/simulations/sim4.html">Simulation 4</a>
      </div>
    </nav>
  `;

  document.body.insertAdjacentHTML("afterbegin", navHTML);
});

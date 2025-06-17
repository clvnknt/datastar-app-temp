import './style.css';
import '../node_modules/@starfederation/datastar/dist/bundles/datastar.js';

fetch('/src/components/navbar.html')
  .then(res => res.text())
  .then(html => {
    document.getElementById('navbar').innerHTML = html;
  });

fetch('/src/components/footer.html')
.then(res => res.text())
.then(html => {
  document.getElementById('footer').innerHTML = html;
});

fetch('/src/components/home/grid.html')
.then(res => res.text())
.then(html => {
  document.getElementById('grid').innerHTML = html;
});
sidebarMenu();

// let listItems = document.querySelectorAll ('#listUL li');

// listItems.forEach ((item, index) => {
//   item.addEventListener ('click', event => {
//     alert (`${event.currentTarget.id} item was click`);
//   });
// });

// let listItems = document.querySelectorAll ('#listUL li a span');

// listItems.forEach ((item, index) => {
//   item.addEventListener ('click', event => {
//     alert (`${event.currentTarget.innerText} item was click`);
//   });
// });

function sidebarMenu() {
   const el = document.getElementById("main-menu");

   const hiddenEl = document.getElementById("content-head");

   el.addEventListener("mouseover", function handleMouseOver() {
      hiddenEl.style.visibility = "visible";
      hiddenEl.style.transition = "0.3s";
   });

   el.addEventListener("mouseout", function handleMouseOut() {
      hiddenEl.style.visibility = "hidden";
      hiddenEl.style.transition = "0.3s";
   });
}

document.querySelectorAll("td").forEach(td => {
  td.setAttribute("title", td.textContent);
});
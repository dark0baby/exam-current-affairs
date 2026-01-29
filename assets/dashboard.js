fetch("index.json")
  .then(res => res.json())
  .then(data => {
    const daily = document.getElementById("daily-list");
    data.forEach(item => {
      const li = document.createElement("li");
      li.innerHTML = `<b>${item.topic}</b><br>
      <small>${item.mcq.question}</small>`;
      daily.appendChild(li);
    });
  })
  .catch(err => {
    console.error("Failed to load CA:", err);
  });

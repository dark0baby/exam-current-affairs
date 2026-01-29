// Dashboard JS
const dailyList = document.getElementById("daily-list");
const weeklyList = document.getElementById("weekly-list");
const monthlyList = document.getElementById("monthly-list");
const yearlyList = document.getElementById("yearly-list");
const contentDiv = document.getElementById("content");

let currentContent = "";

// Load index.json
fetch("index.json")
  .then(res => res.json())
  .then(index => {
    // DAILY
    index.daily.slice().reverse().forEach(date => {
      const li = document.createElement("li");
      li.innerHTML = `<a href="#" data-date="${date}">${date}</a>`;
      li.querySelector("a").addEventListener("click", e => {
        e.preventDefault();
        loadContent(date);
      });
      dailyList.appendChild(li);
    });

    // WEEKLY
    Object.keys(index.weekly).sort().reverse().forEach(week => {
      const li = document.createElement("li");
      li.innerHTML = `<a href="#" data-week="${week}">${week}</a>`;
      li.querySelector("a").addEventListener("click", e => {
        e.preventDefault();
        loadWeeklyContent(week, index.weekly[week]);
      });
      weeklyList.appendChild(li);
    });

    // MONTHLY
    Object.keys(index.monthly).sort().reverse().forEach(month => {
      const li = document.createElement("li");
      li.innerHTML = `<a href="#" data-month="${month}">${month}</a>`;
      li.querySelector("a").addEventListener("click", e => {
        e.preventDefault();
        loadMonthlyContent(month, index.monthly[month]);
      });
      monthlyList.appendChild(li);
    });

    // YEARLY
    Object.keys(index.yearly).sort().reverse().forEach(year => {
      const li = document.createElement("li");
      li.innerHTML = `<a href="#" data-year="${year}">${year}</a>`;
      li.querySelector("a").addEventListener("click", e => {
        e.preventDefault();
        loadYearlyContent(year, index.yearly[year]);
      });
      yearlyList.appendChild(li);
    });
  });

// Load single day content
function loadContent(date) {
  fetch(`https://raw.githubusercontent.com/dark0baby/exam-current-affairs/main/data/${date}/daily_brief.md`)
    .then(res => res.text())
    .then(md => {
      currentContent = md;
      contentDiv.innerHTML = marked.parse(md);
    });
}

// Load weekly content (array of dates)
function loadWeeklyContent(week, dates) {
  let promises = dates.map(d => fetch(`data/${d}/daily_brief.md`).then(res => res.text()));
  Promise.all(promises).then(contents => {
    currentContent = contents.join("\n\n");
    contentDiv.innerHTML = marked.parse(currentContent);
  });
}

// Load monthly content (array of week_ids)
function loadMonthlyContent(month, week_ids) {
  let weekPromises = week_ids.map(w => {
    return fetch(`index.json`).then(res => res.json()).then(index => {
      let dates = index.weekly[w] || [];
      return Promise.all(dates.map(d => fetch(`data/${d}/daily_brief.md`).then(r => r.text())));
    });
  });
  Promise.all(weekPromises).then(arr => {
    currentContent = arr.flat().join("\n\n");
    contentDiv.innerHTML = marked.parse(currentContent);
  });
}

// Load yearly content (array of months)
function loadYearlyContent(year, months) {
  let monthPromises = months.map(m => {
    return fetch(`index.json`).then(res => res.json()).then(index => {
      let week_ids = index.monthly[m] || [];
      let weekPromises = week_ids.map(w => {
        let dates = index.weekly[w] || [];
        return Promise.all(dates.map(d => fetch(`data/${d}/daily_brief.md`).then(r => r.text())));
      });
      return Promise.all(weekPromises).then(arr => arr.flat());
    });
  });
  Promise.all(monthPromises).then(arr => {
    currentContent = arr.flat().join("\n\n");
    contentDiv.innerHTML = marked.parse(currentContent);
  });
}

// PDF Download
document.getElementById("downloadPDF").addEventListener("click", () => {
  const { jsPDF } = window.jspdf;
  const doc = new jsPDF();
  const lines = currentContent.split("\n");
  let y = 10;
  lines.forEach(line => {
    doc.text(line, 10, y);
    y += 7;
  });
  doc.save("current_affairs.pdf");
});

// Word Download
document.getElementById("downloadWord").addEventListener("click", () => {
  const { Document, Packer, Paragraph, TextRun } = window.docx;
  const doc = new Document();
  currentContent.split("\n").forEach(line => {
    doc.addSection({
      children: [new Paragraph({ children: [new TextRun(line)] })],
    });
  });
  Packer.toBlob(doc).then(blob => {
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "current_affairs._

// Load JSON index
fetch('index.json')
.then(res => res.json())
.then(data => {
    // Daily
    const dailyList = document.getElementById('daily-list');
    data.daily.forEach(day => {
        let li = document.createElement('li');
        li.textContent = day;
        li.onclick = () => loadContent(day);
        dailyList.appendChild(li);
    });

    // Weekly
    const weeklyList = document.getElementById('weekly-list');
    for(let week in data.weekly){
        let li = document.createElement('li');
        li.textContent = week;
        li.onclick = () => showSubList(data.weekly[week]);
        weeklyList.appendChild(li);
    }

    // Monthly
    const monthlyList = document.getElementById('monthly-list');
    for(let month in data.monthly){
        let li = document.createElement('li');
        li.textContent = month;
        li.onclick = () => showSubList(data.monthly[month]);
        monthlyList.appendChild(li);
    }

    // Yearly
    const yearlyList = document.getElementById('yearly-list');
    for(let year in data.yearly){
        let li = document.createElement('li');
        li.textContent = year;
        li.onclick = () => showSubList(data.yearly[year]);
        yearlyList.appendChild(li);
    }
});

function showSubList(arr){
    const dailyList = document.getElementById('daily-list');
    dailyList.innerHTML = '';
    arr.forEach(item => {
        let li = document.createElement('li');
        li.textContent = item;
        li.onclick = () => loadContent(item);
        dailyList.appendChild(li);
    });
}

function loadContent(day){
    fetch(`data/${day}/daily_brief.md`)
    .then(res => res.text())
    .then(md => {
        document.getElementById('content').innerHTML = md.replace(/\n/g,'<br>');
    });
}

// Download buttons
document.getElementById('downloadPDF').onclick = () => {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    const content = document.getElementById('content').innerText;
    doc.text(content, 10, 10);
    doc.save('CurrentAffairs.pdf');
};

document.getElementById('downloadWord').onclick = () => {
    const { Document, Packer, Paragraph, TextRun } = window.docx;
    const doc = new Document({
        sections: [{
            properties: {},
            children: [
                new Paragraph({
                    children: [
                        new TextRun({ text: document.getElementById('content').innerText })
                    ]
                })
            ]
        }]
    });
    Packer.toBlob(doc).then(blob => {
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = "CurrentAffairs.docx";
        link.click();
    });
};

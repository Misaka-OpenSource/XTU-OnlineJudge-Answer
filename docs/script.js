fetch('answer/index.json')
    .then(response => response.json())
    .then(data => {
        const list = document.getElementById('list');

        data.sort((a, b) => {
            if (a.exam_id !== b.exam_id)
                return a.exam_id - b.exam_id;
            else
                return a.problem_id - b.problem_id;
        });

        data.forEach(item => {
            const li = document.createElement('li');
            const a = document.createElement('a');
            a.href = `https://YangRucheng.github.io/XTU-OnlineJudge-Answer/answer/${item.exam_id}/${item.problem_id}`
            a.textContent = `${item.exam_id}/${item.problem_id}`
            li.appendChild(a);
            list.appendChild(li);
        });
    })
    .catch(error => console.error(error));


const list = document.getElementById('list');

list.addEventListener('click', (event) => {
    const target = event.target;
    if (target.tagName === 'LI' && target.firstElementChild.tagName === 'A') {
        target.firstElementChild.click();
    }
});

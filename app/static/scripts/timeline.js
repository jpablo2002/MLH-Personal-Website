// Timeline Page Elements
const timelineContainer = document.getElementById('timeline');
const postForm = document.getElementById('postForm')
const [nameInput, emailInput] = document.querySelectorAll('form input')
const contentInput = document.querySelector('form textarea')
let currTimelinePosts;

// Rendering Timeline Posts

const renderAllPosts = function (timelinePosts) {
    let html = '';
    timelinePosts.forEach((post, i) => {
        html += `
        <div class="timeline-post-section ${i % 2 === 0 ? 'left' : 'right'}">
            <div class="timeline-post">
                <h2>${post['name']}</h2>
                <p>${post['content']}</p>
                <div class="timeline-post-footer">
                    <span>${post['email']}</span>
                    <span>${post['created_at']}</span>
                </div>
            </div>
        </div>
        `
    });
    timelineContainer.insertAdjacentHTML('afterbegin', html)

}

// Init Timeline Page

fetch("/api/timeline_post")
    .then(res => res.json())
    .then(({ timeline_posts }) => {
        currTimelinePosts = timeline_posts;
        renderAllPosts(timeline_posts)
    })
    .catch(err => {
        console.log(`Error: ${err}`);
    })

postForm.addEventListener('submit', (e) => {
    e.preventDefault();

    if (nameInput.value === '' || emailInput.value === '' || contentInput.value === '') {
        alert('Please complete all sections of the form before submitting!')
    } else {

        const formData = new FormData();
        formData.append('name', nameInput.value);
        formData.append('email', emailInput.value);
        formData.append('content', contentInput.value);

        fetch('/api/timeline_post', {
            method: 'post',
            body: formData
        })
            .then(res => res.json())
            .then(newPost => {
                currTimelinePosts.unshift(newPost);
                const i = currTimelinePosts.length;
                let html = `
        <div class="timeline-post-section ${i % 2 === 0 ? 'left' : 'right'}">
            <div class="timeline-post">
                <h2>${newPost['name']}</h2>
                <p>${newPost['content']}</p>
                <div class="timeline-post-footer">
                    <span>${newPost['email']}</span>
                    <span>${newPost['created_at']}</span>
                </div>
            </div>
        </div>
        `
                timelineContainer.insertAdjacentHTML('afterbegin', html)
                nameInput.value = '';
                emailInput.value = '';
                contentInput.value = '';
            })
            .catch(err => console.log(err))
    }
})

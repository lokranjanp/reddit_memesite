let countdownInterval;

function updateCountdown(seconds) {
    document.getElementById('countdown').textContent = seconds;
    if (countdownInterval) {
        clearInterval(countdownInterval);
    }
    countdownInterval = setInterval(function() {
        if (seconds > 0) {
            seconds--;
            document.getElementById('countdown').textContent = seconds;
        } else {
            clearInterval(countdownInterval);
            fetchNewMeme();
        }
    }, 1000);
}

document.addEventListener('DOMContentLoaded', function() {
    let initialCountdown = 30;

    const storedCategory = localStorage.getItem('selectedCategory');
    let selectedButton = document.querySelector('#categoryForm button.active');
    
    if (storedCategory) {
        document.querySelectorAll('#categoryForm button').forEach(button => {
            button.classList.remove('active');
            if (button.value === storedCategory) {
                button.classList.add('active');
            }
        });
        document.querySelector('.custom-category-input').value = storedCategory;
    } else if (!selectedButton) {
        selectedButton = document.querySelector('#categoryForm button');
        if (selectedButton) {
            selectedButton.classList.add('active');
        }
    }

    updateCountdown(initialCountdown);

    document.querySelectorAll('#categoryForm button').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelectorAll('#categoryForm button').forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            document.querySelector('.custom-category-input').value = '';
            localStorage.removeItem('selectedCategory');
            fetchNewMeme();
        });
    });

    document.querySelector('.custom-category-input').addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            const customCategory = event.target.value.trim();
            if (customCategory) {
                localStorage.setItem('selectedCategory', customCategory);
                fetchNewMeme();
            }
        }
    });

    fetchNewMeme();
});

function fetchNewMeme() {
    let selectedCategory = localStorage.getItem('selectedCategory');
    let selectedButton = document.querySelector('#categoryForm button.active');

    if (!selectedCategory && selectedButton) {
        selectedCategory = selectedButton.value;
    }

    if (!selectedCategory) {
        console.error('No active category button or custom category found');
        return;
    }

    document.getElementById('preloader').style.display = 'block';
    console.log("Fetching new meme for category:", selectedCategory);

    fetch(`/new_meme?category=${encodeURIComponent(selectedCategory)}`)
        .then(response => response.text())
        .then(html => {
            document.getElementById('meme-container').innerHTML = html;
            updateCountdown(30);
        })
        .finally(() => {
            document.getElementById('preloader').style.display = 'none';
        });
}

const loader = document.getElementById("preloader");

window.addEventListener("load", () => {
    loader.style.display = "none";
});

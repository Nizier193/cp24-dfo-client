document.addEventListener('DOMContentLoaded', () => {
    const userText = document.getElementById('user-text');
    const displayText = document.getElementById('display-text');
    const textType = document.getElementById('text-type');
    const userNumber = document.getElementById('user-number');

    userText.addEventListener('input', () => {
        displayText.textContent = userText.value;
        userText.style.height = 'auto';
        userText.style.height = userText.scrollHeight + 'px';
    });

    textType.addEventListener('change', () => {
        displayText.textContent = textType.value;
    });


    const sendDataToServer = (data) => {
        fetch('/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    };

    userText.addEventListener('blur', () => {
        sendDataToServer({ text: userText.value });
    });

    textType.addEventListener('change', () => {
        sendDataToServer({ type: textType.value });
    });


    userNumber.addEventListener('blur', () => {
        sendDataToServer({ number: userNumber.value });
    });
});




let images = [
    'img/2.jpg', 
    'img/1.jpg',
    'img/3.jpg', 
    'img/4.jpg',    
    'img/5.jpg', 
    'img/6.jpg'
];
let currentIndex = 0;

function updateImage() {
    const carouselImage = document.getElementById('carousel-image');
    carouselImage.src = images[currentIndex];
}

function prevImage() {
    currentIndex = (currentIndex - 1 + images.length) % images.length;
    updateImage();
}

function nextImage() {
    currentIndex = (currentIndex + 1) % images.length;
    updateImage();
}

function downloadImage() {
    const link = document.createElement('a');
    link.href = images[currentIndex];
    link.download = `image${currentIndex + 1}`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}


document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        window.location.href = 'end.html'; 
    }, 30000);
});

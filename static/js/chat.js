document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');

    const imageUpload = document.getElementById('image-upload');
    const uploadButton = document.querySelector('.upload-button');
    const imagePreview = document.getElementById('image-preview');
    const previewImg = document.getElementById('preview-img');
    const removeImage = document.getElementById('remove-image');
    let currentImage = null;

    // 图片上传处理
    uploadButton.addEventListener('click', () => imageUpload.click());

    imageUpload.addEventListener('change', function(e) {
        if (e.target.files.length > 0) {
            currentImage = e.target.files[0];
            const reader = new FileReader();
            reader.onload = function(event) {
                previewImg.src = event.target.result;
                imagePreview.style.display = 'flex';
            }
            reader.readAsDataURL(currentImage);
        }
    });

    // 移除图片
    removeImage.addEventListener('click', function() {
        currentImage = null;
        imagePreview.style.display = 'none';
        previewImg.src = '';
        imageUpload.value = '';
    });

    // 修改sendMessage函数以支持图片
    async function sendMessage() {
        const message = userInput.value.trim();
        if (message || currentImage) {
            // 创建FormData对象
            const formData = new FormData();
            if (message) formData.append('message', message);
            if (currentImage) formData.append('image', currentImage);

            // 显示用户消息（不显示图片，只显示文字）
            if (message) addMessage(message, true);
            if (currentImage) addMessage("[图片]", true);

            userInput.value = '';
            currentImage = null;
            imagePreview.style.display = 'none';
            previewImg.src = '';
            imageUpload.value = '';

            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    body: formData  // 不需要设置Content-Type，浏览器会自动设置
                });

                const data = await response.json();
                addMessage(data.reply, false);
            } catch (error) {
                addMessage('抱歉，暂时无法连接到AI服务', false);
                console.error('Error:', error);
            }
        }
    }

    function addMessage(text, isUser) {
        const messageDiv = document.createElement('div');
        messageDiv.className = isUser ? 'message user-message' : 'message bot-message';
        messageDiv.textContent = text;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
});
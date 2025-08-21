// Configuração da API
const API_BASE_URL = '/api';

let selectedBooks = [];
let allBooks = [];

// Função para fazer requisições à API
async function apiRequest(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Função para carregar livros do backend
async function loadBooks() {
    try {
        allBooks = await apiRequest('/books');
        renderBooks();
    } catch (error) {
        console.error('Erro ao carregar livros:', error);
        alert('Erro ao carregar livros. Tente novamente mais tarde.');
    }
}

// Função para formatar telefone
function formatPhone(value) {
    // Remove tudo que não é número
    const numbers = value.replace(/\D/g, '');
    
    // Aplica a formatação
    if (numbers.length <= 10) {
        // Formato: (11) 9999-9999
        return numbers.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
    } else {
        // Formato: (11) 99999-9999
        return numbers.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
    }
}

// Função para validar email
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Função para validar telefone
function isValidPhone(phone) {
    const numbers = phone.replace(/\D/g, '');
    return numbers.length >= 10 && numbers.length <= 11;
}

// Função para mostrar erro
function showError(fieldId, message) {
    const field = document.getElementById(fieldId);
    const errorDiv = document.getElementById(fieldId + '-error');
    
    field.classList.add('error');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
}

// Função para limpar erro
function clearError(fieldId) {
    const field = document.getElementById(fieldId);
    const errorDiv = document.getElementById(fieldId + '-error');
    
    field.classList.remove('error');
    errorDiv.style.display = 'none';
}

// Função para renderizar os livros na página
function renderBooks() {
    const bookList = document.getElementById("book-list");
    bookList.innerHTML = "";

    allBooks.forEach(book => {
        const bookCard = document.createElement("div");
        bookCard.className = "book-card";
        
        const isSelected = selectedBooks.includes(book.id);
        const isAvailable = book.available && !isSelected;
        
        const buttonClass = !book.available ? '' : isSelected ? 'remove-btn' : '';
        const buttonStyle = !book.available ? 'style="background: linear-gradient(135deg, #CBD5E0 0%, #A0AEC0 100%); cursor: not-allowed; transform: none; box-shadow: none;"' : '';
        
        bookCard.innerHTML = `
            <img src="${book.image}" alt="${book.title}" loading="lazy">
            <h3>${book.title}</h3>
            <p><strong>Autor:</strong> ${book.author}</p>
            <p>${book.description}</p>
            <button 
                class="${buttonClass}"
                onclick="${isSelected ? `removeBook(${book.id})` : `selectBook(${book.id})`}"
                ${!book.available ? 'disabled' : ''}
                ${buttonStyle}
            >
                ${!book.available ? "Indisponível" : isSelected ? "Remover Seleção" : "Selecionar"}
            </button>
        `;
        
        bookList.appendChild(bookCard);
    });
}

// Função para selecionar um livro
function selectBook(bookId) {
    if (!selectedBooks.includes(bookId)) {
        selectedBooks.push(bookId);
        updateReservationForm();
        renderBooks();
    }
}

// Função para remover um livro da seleção
function removeBook(bookId) {
    selectedBooks = selectedBooks.filter(id => id !== bookId);
    updateReservationForm();
    renderBooks();
}

// Função para atualizar o formulário de reserva
function updateReservationForm() {
    const reservationForm = document.getElementById("reservation-form");
    const selectedBooksSummary = document.getElementById("selected-books-summary");
    
    if (selectedBooks.length > 0) {
        reservationForm.style.display = "block";
        
        const selectedBooksInfo = selectedBooks.map(id => {
            const book = allBooks.find(b => b.id === id);
            return `<li>${book.title} - ${book.author}</li>`;
        }).join("");
        
        selectedBooksSummary.innerHTML = `
            <h3>Livros Selecionados:</h3>
            <ul>${selectedBooksInfo}</ul>
            <p><strong>Importante:</strong> O custo do frete será por sua conta. Após confirmar a reserva, entraremos em contato para combinar o envio.</p>
        `;
        
        // Scroll suave para o formulário
        reservationForm.scrollIntoView({ behavior: 'smooth', block: 'start' });
    } else {
        reservationForm.style.display = "none";
    }
}

// Função para validar formulário
function validateForm() {
    let isValid = true;
    
    // Limpar erros anteriores
    ['name', 'email', 'address', 'phone'].forEach(clearError);
    
    // Validar nome
    const name = document.getElementById('name').value.trim();
    if (!name || name.length < 2) {
        showError('name', 'Por favor, informe seu nome completo.');
        isValid = false;
    }
    
    // Validar email
    const email = document.getElementById('email').value.trim();
    if (!email || !isValidEmail(email)) {
        showError('email', 'Por favor, informe um email válido.');
        isValid = false;
    }
    
    // Validar endereço
    const address = document.getElementById('address').value.trim();
    if (!address || address.length < 10) {
        showError('address', 'Por favor, informe seu endereço completo.');
        isValid = false;
    }
    
    // Validar telefone
    const phone = document.getElementById('phone').value.trim();
    if (!phone || !isValidPhone(phone)) {
        showError('phone', 'Por favor, informe um telefone válido.');
        isValid = false;
    }
    
    return isValid;
}

// Função para processar o formulário de reserva
async function handleReservation(event) {
    event.preventDefault();
    
    if (!validateForm()) {
        return;
    }
    
    const submitButton = event.target.querySelector('button[type="submit"]');
    const originalText = submitButton.textContent;
    
    try {
        // Desabilitar botão e mostrar loading
        submitButton.disabled = true;
        submitButton.textContent = 'Processando...';
        
        const formData = new FormData(event.target);
        const reservationData = {
            name: formData.get("name"),
            email: formData.get("email"),
            address: formData.get("address"),
            phone: formData.get("phone"),
            selectedBooks: selectedBooks.map(id => {
                const book = allBooks.find(b => b.id === id);
                return { id: book.id, title: book.title, author: book.author };
            })
        };
        
        // Enviar reserva para o backend
        await apiRequest('/reservations', {
            method: 'POST',
            body: JSON.stringify(reservationData)
        });
        
        // Recarregar livros para atualizar disponibilidade
        await loadBooks();
        
        // Limpar seleção
        selectedBooks = [];
        updateReservationForm();
        
        // Mostrar mensagem de sucesso
        alert(`Obrigado, ${reservationData.name}! Sua reserva foi confirmada. Entraremos em contato em breve para combinar o envio dos livros.`);
        
        // Limpar formulário
        event.target.reset();
        
        // Scroll para o topo
        window.scrollTo({ top: 0, behavior: 'smooth' });
        
    } catch (error) {
        console.error('Erro ao criar reserva:', error);
        alert('Erro ao processar sua reserva. Tente novamente mais tarde.');
    } finally {
        // Reabilitar botão
        submitButton.disabled = false;
        submitButton.textContent = originalText;
    }
}

// Inicializar a página
document.addEventListener("DOMContentLoaded", function() {
    // Carregar livros do backend
    loadBooks();
    
    // Adicionar event listener ao formulário
    document.getElementById("book-reservation-form").addEventListener("submit", handleReservation);
    
    // Adicionar formatação automática ao telefone
    const phoneInput = document.getElementById('phone');
    phoneInput.addEventListener('input', function(e) {
        const formatted = formatPhone(e.target.value);
        e.target.value = formatted;
        
        // Limpar erro se o telefone ficar válido
        if (isValidPhone(formatted)) {
            clearError('phone');
        }
    });
    
    // Adicionar validação em tempo real para outros campos
    document.getElementById('name').addEventListener('blur', function(e) {
        if (e.target.value.trim().length >= 2) {
            clearError('name');
        }
    });
    
    document.getElementById('email').addEventListener('blur', function(e) {
        if (isValidEmail(e.target.value.trim())) {
            clearError('email');
        }
    });
    
    document.getElementById('address').addEventListener('blur', function(e) {
        if (e.target.value.trim().length >= 10) {
            clearError('address');
        }
    });
});


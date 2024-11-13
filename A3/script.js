// document.getElementById('categoria-form').addEventListener('submit', async function (e) {
//     e.preventDefault();

//     const nome = document.getElementById('categoria-nome').value;
//     const descricao = document.getElementById('categoria-descricao').value;

//     const response = await fetch('/categoria', {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify({ nome, descricao }),
//     });

//     if (response.ok) {
//         alert('Categoria cadastrada com sucesso!');
//         this.reset();
//     } else {
//         alert('Erro ao cadastrar categoria.');
//     }
// });

// document.getElementById('produto-form').addEventListener('submit', async function (e) {
//     e.preventDefault();

//     const nome = document.getElementById('produto-nome').value;
//     const descricao = document.getElementById('produto-descricao').value;
//     const preco = document.getElementById('produto-preco').value;
//     const quantidade = document.getElementById('produto-quantidade').value;

//     const response = await fetch('/produto', {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify({ nome, descricao, preco, quantidade }),
//     });

//     if (response.ok) {
//         alert('Produto cadastrado com sucesso!');
//         this.reset();
//     } else {
//         alert('Erro ao cadastrar produto.');
//     }
// });

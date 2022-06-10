function deleteBook(bookId){
    fetch('/delete-book', {
        method: 'POST',
        body: JSON.stringify({bookId: bookId})
    }).then((_res) =>{
        window.location.href = "/"; // reload window after response
    });
}
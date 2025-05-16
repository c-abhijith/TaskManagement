document.addEventListener('DOMContentLoaded', function () {
    const usersButton = document.getElementById('usersButton');
    const adminButton = document.getElementById('adminButton');
    const usersList = document.getElementById('usersList');
    const adminList = document.getElementById('adminList');

    if (usersButton && adminButton && usersList && adminList) {
        usersButton.addEventListener('click', function (e) {
            e.preventDefault();
            usersList.style.display = 'block';
            adminList.style.display = 'none';
        });

        adminButton.addEventListener('click', function (e) {
            e.preventDefault();
            adminList.style.display = 'block';
            usersList.style.display = 'none';
        });
    }
});

const modalButtons = document.querySelectorAll('.modal-button')
const modalBody = document.querySelector('#modal-body-confirm')
const startButton = document.querySelector('#start-button')

const modalBtnsArray = [...modalButtons]
const url = window.location.href

function concatStrings(...args) {
    return args.reduce((acc, val) => {
        return `${acc}${val}`
    })
}

modalBtnsArray.forEach(function(modalBtn) {
    modalBtn.addEventListener('click', () => {
        const pk = modalBtn.getAttribute('data-pk')
        const name = modalBtn.getAttribute('data-quiz')
        const numOfQuestions = modalBtn.getAttribute('data-questions')
        const difficulty = modalBtn.getAttribute('data-difficulty')
        const pass_score = modalBtn.getAttribute('data-pass')
        const time = modalBtn.getAttribute('data-time')

        modalBody.innerHTML = `
            <div class="h5 mb-3">
                <p>Are you sure you want to begin "<strong>${name}</strong>"?</p>
            </div>
            <div class="text-muted">
                <ul>
                    <li>Difficulty <strong>${difficulty}</strong></li>
                    <li>Number of Question <strong>${numOfQuestions}</strong></li>
                    <li>Score to pass <strong>${pass_score}%</strong></li>
                    <li>Time <strong>${time}</strong></li>
                </ul>
            </div>
        `

        startButton.addEventListener('click', () => {
            window.location.href = concatStrings(url, pk)
        })
    })
})
